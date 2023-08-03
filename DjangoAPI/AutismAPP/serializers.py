from rest_framework import serializers
from AutismAPP.models import Parents,Enfants,TestsAutisme

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = ( 'ParentId',
                  'ParentName',
                  'ParentMail',
                  'ParentPwd',
                  'ParentTel',
                  'ParentVille',
                  'ParentRegion' )
        


class EnfantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfants
        fields = ( 'EnfantId',
                  'EnfantAge',
                  'EnfantName',
                  'EnfantSexe',
                  'EnfantParentId',
                  'EnfantEthmicity',
                  'EnfantJaundice',
                  'EnfantFamelyMsd')
        

class TestAutismeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestsAutisme
        fields = ( 'TestsAutismeId',
                  'TestIdEnfant',
                  'TestQ1',
                  'TestQ2',
                  'TestQ3',
                  'TestQ4',
                  'TestQ5',
                  'TestQ6',
                  'TestQ7',
                  'TestQ8',              
                  'TestQ9',
                  'TestQ10',
                  'TestScore')