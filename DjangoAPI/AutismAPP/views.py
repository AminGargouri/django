
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import pandas as pd

from AutismAPP.models import Parents,Enfants,TestsAutisme
from AutismAPP.serializers import ParentSerializer,EnfantSerializer,TestAutismeSerializer

from django.shortcuts import render
import joblib
import os
import pandas as pd
from .models import Enfants, TestsAutisme
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import scipy.stats as st

# def merge_enfants_testautism():
#     # Récupérer tous les enregistrements des modèles Enfants et TestsAutisme
#     enfants_records = Enfants.objects.all().values('EnfantId', 'EnfantAge', 'EnfantName', 'EnfantSexe', 'EnfantParentId', 'EnfantEthmicity', 'EnfantJaundice', 'EnfantFamelyMsd')
#     testautism_records = TestsAutisme.objects.all().values('TestIdEnfant', 'TestQ1', 'TestQ2', 'TestQ3', 'TestQ4', 'TestQ5', 'TestQ6', 'TestQ7', 'TestQ8', 'TestQ9', 'TestQ10', 'TestScore')

#     # Créer des DataFrames à partir des enregistrements récupérés
#     df_enfants = pd.DataFrame.from_records(enfants_records)
#     df_testautism = pd.DataFrame.from_records(testautism_records)

#     # Renommer la colonne TestIdEnfant en EnfantId dans le DataFrame df_testautism
#     df_testautism = df_testautism.rename(columns={"TestIdEnfant":"EnfantId"})

#     # Fusionner les DataFrames enfants et testautism sur la colonne EnfantId
#     df_merged = pd.merge(df_enfants, df_testautism, on="EnfantId")

#     return df_merged
# def merge_enfants_testautism():
#     try:
#         # Récupérer tous les enregistrements des modèles Enfants et TestsAutisme
#         enfants_records = Enfants.objects.all().values('EnfantId', 'EnfantAge', 'EnfantName', 'EnfantSexe', 'EnfantParentId', 'EnfantEthmicity', 'EnfantJaundice', 'EnfantFamelyMsd')
#         testautism_records = TestsAutisme.objects.all().values('TestIdEnfant', 'TestQ1', 'TestQ2', 'TestQ3', 'TestQ4', 'TestQ5', 'TestQ6', 'TestQ7', 'TestQ8', 'TestQ9', 'TestQ10', 'TestScore')

#         # Créer des DataFrames à partir des enregistrements récupérés
#         df_enfants = pd.DataFrame.from_records(enfants_records)
#         df_testautism = pd.DataFrame.from_records(testautism_records)

#         # Renommer la colonne TestIdEnfant en EnfantId dans le DataFrame df_testautism
#         df_testautism = df_testautism.rename(columns={"TestIdEnfant": "EnfantId"})
#         print("les noms des colonnes ",df_testautism.columns)

#         # Vérifier si 'EnfantId' est présent dans les DataFrames
#         if 'EnfantId' not in df_enfants.columns or 'EnfantId' not in df_testautism.columns:
#             raise KeyError("The column 'EnfantId' is missing in one or both DataFrames.")

#         # Fusionner les DataFrames enfants et testautism sur la colonne EnfantId
#         #df_merged = pd.merge(df_enfants, df_testautism, on="EnfantId")
#         #print(df_merged)

#         return df_merged
#     except Exception as e:
#         # Handle the error
#         print("An error occurred:", e)
#         return None
    


# Utilisation de la fonction pour fusionner les DataFrames enfants et testautism
#df_merged = merge_enfants_testautism()

# Afficher le DataFrame df_merged résultant
#print(df_merged)







model_path = 'best_svc_model.pkl'
model = joblib.load(model_path)
print('model :',model)


def prediction_view(request):
    if request.method == 'POST':
        # Récupérer les nouvelles données de la requête POST (assurez-vous de les prétraiter comme vous l'avez fait lors de l'entraînement du modèle)
        request_data=JSONParser().parse(request)
        newdata = {
            'A1': [request_data["TestQ1"]],
            'A2': [request_data["TestQ2"]],
            'A3': [request_data["TestQ3"]],
            'A4': [request_data["TestQ4"]],
            'A5': [request_data["TestQ5"]],
            'A6': [request_data["TestQ6"]],
            'A7': [request_data["TestQ7"]],
            'A8': [request_data["TestQ8"]],
            'A9': [request_data["TestQ9"]],
            'A10': [request_data["TestQ10"]],
            'AgeMons': [request_data["EnfantAge"]],
            'Sex': [request_data["EnfantSexe"]],
            'Ethnicity': [request_data["EnfantEthmicity"]],
            'Jaundice': [request_data["EnfantJaundice"]],
            'Family_mem_with_ASD': [request_data["EnfantFamelyMsd"]]}
        Score=newdata['A1']+newdata['A2']+newdata['A3']+newdata['A4']+newdata['A5']+newdata['A6']+newdata['A7']+newdata['A8']+newdata['A9']+newdata['A10']
        print('score=',Score)
        newdata = pd.DataFrame(newdata)
        print(newdata)  
        
        # Vérifier si la colonne Age suit une loi normale ou non
        age_column = newdata["Age_Mons"]
        statistic, p_value = st.shapiro(age_column)
        print("Valeur P du test :", p_value)
        alpha = 0.05
        if p_value > alpha:
            print("La colonne Age suit une distribution normale")
        else:
            print("La colonne Age ne suit pas une distribution normale")

        # Liste des colonnes numériques à standardiser
        numeric_cols = ["Age_Mons"]

        # Créer un objet MinMaxScaler
        scaler = MinMaxScaler()

        # Appliquer MinMaxScaler sur les colonnes numériques
        newdata[numeric_cols] = scaler.fit_transform(newdata[numeric_cols])

        # Encoder les colonnes Sex, Jaundice, Family_mem_with_ASD
        categorical_columns = ['Sex', 'Jaundice', 'Family_mem_with_ASD']
        label_encoder = LabelEncoder()
        for col in categorical_columns:
            newdata[col] = label_encoder.fit_transform(newdata[col])

        # Appliquer OneHotEncoder sur la colonne 'Ethnicity'
        ct = ColumnTransformer([("Ethnicity", OneHotEncoder(), [12])], remainder='passthrough')
        newdata = ct.transform(newdata)
        newdata = newdata[:, 1:]
        newdata = pd.DataFrame(newdata)     
       
        # Faire des prédictions avec le modèle chargé
        predictions = model.predict(newdata)
       
        # Par exemple, renvoyer les prédictions sous forme de texte dans une page de modèle "predictions.html"
        return render(request, 'predictions.html', {'predictions': predictions})
    else:
        # Si la méthode n'est pas POST, simplement afficher le formulaire (vous pouvez créer un formulaire HTML ici)
        return render(request, 'votre_formulaire.html')





# Create your views here.
@csrf_exempt
def parentAPI(request , id=0):
    if request.method == 'GET':
      
        ids = Parents.objects.values_list('ParentId', flat=True)

        if id != 0:
            if int(id) in ids:
            
                parent = Parents.objects.get(ParentId=id)
                parent_serializer = ParentSerializer(parent)
                return JsonResponse(parent_serializer.data, safe=False)
            else:                
                return JsonResponse(" parent inexiste",safe=False)
        
        parents = Parents.objects.all()
        parents_serializer = ParentSerializer(parents, many=True)
        return JsonResponse(parents_serializer.data, safe=False) 
    
    elif request.method == 'POST':
        
        parent_data=JSONParser().parse(request)
        #print(parent_data)

        parentMailToIN= parent_data["ParentMail"]
        parentMails = Parents.objects.values_list('ParentMail', flat=True)
        if parentMailToIN in parentMails :
            return JsonResponse("Failed to add parent because this Mail is already exist ", safe=False)
        else :
            #print("department_data est : ",department_data)
            #print("adresse mail valide")
            parent_serializer = ParentSerializer(data = parent_data)
            #print("parent_serializer est : ",parent_serializer)
            #print(parent_serializer.error_messages)
            if parent_serializer.is_valid():
                parent_serializer.save()
                return JsonResponse("Added successfully ", safe=False)
            else:
                return JsonResponse("Failed to add ", safe=False)
    
    elif request.method == 'PUT':
        parent_data=JSONParser().parse(request)
        parent=Parents.objects.get(ParentId=parent_data['ParentId'])
        parent_serializer = ParentSerializer(parent , data = parent_data)
        if parent_serializer.is_valid():
            parent_serializer.save()
            return JsonResponse("Updated successfully ", safe=False)
        return JsonResponse("Failed to Update ", safe=False)
    

    
@csrf_exempt 
def enfantAPI(request , id=0,idParent=0):

    if request.method == 'GET':
        print("avant test", idParent)
        if idParent == 0:
            if id==0:
                enfants = Enfants.objects.all()
                enfants_serializer = EnfantSerializer(enfants, many=True)
                return JsonResponse(enfants_serializer.data, safe=False) 
            else:
                print("boucle else")
                # enfant_data=JSONParser().parse(request)
                enfant=Enfants.objects.get(EnfantId=id) 
                enfant_serializer = EnfantSerializer(enfant)
                return JsonResponse(enfant_serializer.data, safe=False) 
        else:

            try:
                enfants = Enfants.objects.get(EnfantParentId=idParent)
                print(enfants)
                enfants_serializer = EnfantSerializer(enfants, many=True)
            except Enfants.DoesNotExist:
                return JsonResponse(enfants_serializer.data, safe=False)             
    
    elif request.method == 'POST':
        enfant_data=JSONParser().parse(request)
        enfants_serializer = EnfantSerializer(data = enfant_data)
        if enfants_serializer.is_valid():
            enfants_serializer.save()
            return JsonResponse("Added successfully ", safe=False)
        return JsonResponse("Failed to add ", safe=False)
    
    elif request.method == 'PUT':
        enfant_data=JSONParser().parse(request)
        enfant=Enfants.objects.get(EnfantId=enfant_data['EnfantId']) 
        enfant_serializer = EnfantSerializer(enfant , data = enfant_data)
        if enfant_serializer.is_valid():
            enfant_serializer.save()
            return JsonResponse("Updated successfully ", safe=False)
        return JsonResponse("Failed to Update ", safe=False)
    
    elif request.method =='DELETE':
        enfant=Enfants.objects.get(EnfantId=id)
        enfant.delete()
        return JsonResponse("Deleted sucessfully ", safe=False)
    

@csrf_exempt 
def testsAutismeAPI(request , id=0,):

    if request.method == 'GET':
        if id == 0:
            testAtismes = TestsAutisme.objects.all()
            testAtismes_serializer = TestAutismeSerializer(testAtismes, many=True)
            return JsonResponse(testAtismes_serializer.data, safe=False)
        else:
            testAtisme = TestsAutisme.objects.get(TestsAutismeId=id) # TestsAutismeId
            testAtisme_serializer = TestAutismeSerializer(testAtisme, many=True)
            return JsonResponse(testAtisme_serializer.data, safe=False)        
              
    elif request.method == 'POST':
        testAtisme=JSONParser().parse(request)
        testAtisme_serializer = TestAutismeSerializer(data = testAtisme)
        if testAtisme_serializer.is_valid():
            testAtisme_serializer.save()
            return JsonResponse("Added successfully ", safe=False)
        return JsonResponse("Failed to add ", safe=False)
    
    elif request.method == 'PUT':
        testAtisme_data=JSONParser().parse(request)
        testAtisme=TestsAutisme.objects.get(TestsAutismeId=testAtisme_data['TestsAutismeId']) 
        testAtisme_serializer = TestAutismeSerializer(testAtisme , data = testAtisme_data)
        if testAtisme_serializer.is_valid():
            testAtisme_serializer.save()
            return JsonResponse("Updated successfully ", safe=False)
        return JsonResponse("Failed to Update ", safe=False)
    
    elif request.method =='DELETE':
        testAtisme=TestsAutisme.objects.get(TestsAutismeId=id)
        testAtisme.delete()
        return JsonResponse("Deleted sucessfully ", safe=False)
    

