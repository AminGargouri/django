
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
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
import scipy.stats as st

model_path = 'AutismAPP\\best_svc_model.pkl'
model = joblib.load(model_path)
# print('model :',model)

@csrf_exempt
def predictionAPI(request):
    if request.method == 'POST':
        # Récupérer les nouvelles données de la requête POST (assurez-vous de les prétraiter comme vous l'avez fait lors de l'entraînement du modèle)
        request_data=JSONParser().parse(request)
        newdata = {
            'A1': [int(request_data["TestQ1"])],
            'A2': [int(request_data["TestQ2"])],
            'A3': [int(request_data["TestQ3"])],
            'A4': [int(request_data["TestQ4"])],
            'A5': [int(request_data["TestQ5"])],
            'A6': [int(request_data["TestQ6"])],
            'A7': [int(request_data["TestQ7"])],
            'A8': [int(request_data["TestQ8"])],
            'A9': [int(request_data["TestQ9"])],
            'A10': [int(request_data["TestQ10"])],
            'Age_Mons': [float(request_data["EnfantAge"])],
            'Sex': [request_data["EnfantSexe"]],
            'Ethnicity': [request_data["EnfantEthmicity"]],
            'Jaundice': [request_data["EnfantJaundice"]],
            'Family_mem_with_ASD': [request_data["EnfantFamelyMsd"]]}
        # print(" le type est ", type(newdata['A1']))
        
        newdata_df = pd.DataFrame(newdata)

        #score = int(newdata_df.iloc[:, :10].sum(axis=1))
        score = int(newdata_df.iloc[:, :10].sum(axis=1).iloc[0])
        # print(" le type de score est ", type(score))
        print('score=', score)
        print(newdata_df)  
        
        # # Vérifier si la colonne Age suit une loi normale ou non
        # age_column = newdata["Age_Mons"]
        # statistic, p_value = st.shapiro(age_column)
        # print("Valeur P du test :", p_value)
        # alpha = 0.05
        # if p_value > alpha:
        #     print("La colonne Age suit une distribution normale")
        # else:
        #     print("La colonne Age ne suit pas une distribution normale")

    
        numeric_cols = ["Age_Mons"]
        scaler = MinMaxScaler()
        newdata_df[numeric_cols] = scaler.fit_transform(newdata_df[numeric_cols].values.reshape(-1, 1))
        # print(newdata_df) 
        
        
        newdata_df['Sex'] = newdata_df['Sex'].map({'m': 1, 'f': 0})
        newdata_df['Jaundice'] = newdata_df['Jaundice'].map({'yes': 1, 'no': 0})
        newdata_df['Family_mem_with_ASD'] = newdata_df['Family_mem_with_ASD'].map({'yes': 1, 'no': 0})
        # print(newdata_df)
        
        
        dset = pd.read_csv("AutismAPP\Toddler Autism dataset July 2018.csv")
        dset =dset.drop(['Who completed the test', 'Class/ASD Traits ', 'Case_No','Qchat-10-Score'] , axis = 1)
        # print(dset)
      
        ct=ColumnTransformer([("Ethnicity",OneHotEncoder(),[12])],remainder='passthrough')

        dset=ct.fit_transform(dset)

        newdata_df = ct.transform(newdata_df)

        # print("after changing ct \n\n\n\n\n" , newdata_df)
        # print("after changing ct  shape \n\n\n\n\n" , newdata_df.shape)
        newdata_df = newdata_df[:,1:]
        # print("after changing ct  shape \n\n\n\n\n" , newdata_df.shape)
        
        # # a_df=a_df[:,1:]
        # # a_df=pd.DataFrame(a_df)
        # # print("a=",a_df)

        # # a_df.columns = a_df.columns.astype(str)
        # # newdata_df.drop(columns=['Ethnicity'], inplace=True)
        # # result_df = pd.concat([a_df, newdata_df], axis=1)
        # # print(result_df)


        # ethnecityCol = newdata_df["Ethnicity"]
        # print("test ethnecityCol \n\n\n\n" , ethnecityCol)
        # newdata_df.drop("Ethnicity" , axis=1)
        # ct=ColumnTransformer([("Ethnicity",OneHotEncoder(),[0])],remainder='passthrough')
        # ethnecityCol = ct.fit_transform(ethnecityCol)
        # print("print test  after transform\n\n\n" , ethnecityCol)       

        
    

         # Faire des prédictions avec le modèle chargé


        predictions = model.predict(newdata_df) # JsonResponse("Deleted sucessfully ", safe=False)
        print("prediction = " ,predictions)
        #return render(request, 'Questionnaire.html', {'predictions': predictions})
        return JsonResponse("Test effectuer avec succe ", safe=False)
    else:
        return JsonResponse("methode get ", safe=False)




    #      # Par exemple, renvoyer les prédictions sous forme de texte dans une page de modèle "predictions.html"
    #     return render(request, 'predictions.html', {'predictions': predictions})
    # else:
    #      # Si la méthode n'est pas POST, simplement afficher le formulaire (vous pouvez créer un formulaire HTML ici)
    #     return render(request, 'votre_formulaire.html')





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

        parentMailToIN= parent_data["ParentMail"]
        parentMails = Parents.objects.values_list('ParentMail', flat=True)
        if parentMailToIN in parentMails :
            return JsonResponse("Failed to add parent because this Mail is already exist ", safe=False)
        else :
        
            parent_serializer = ParentSerializer(data = parent_data)
     
            if parent_serializer.is_valid():
                parent_serializer.save()
                return JsonResponse("Parent Added successfully ", safe=False)
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
            return JsonResponse("Test Added successfully ", safe=False)
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
    

from django.http import JsonResponse

def children_by_parent_view(request, parent_id):
    enfants = Enfants.objects.filter(EnfantParentId=parent_id)

    data = {
        'enfants': [
            {
                'EnfantId': child.EnfantId,
                'EnfantAge': child.EnfantAge,
                'EnfantName': child.EnfantName,
                'EnfantSexe': child.EnfantSexe,
                'EnfantParentId': child.EnfantParentId,
                'EnfantEthmicity': child.EnfantEthmicity,
                "EnfantJaundice": child.EnfantJaundice,
                'EnfantFamelyMsd': child.EnfantFamelyMsd,
                'EnfantAutiste': child.EnfantAutiste,
            }
            for child in enfants
        ],
    }
    # print(data)
    return JsonResponse(data)