from django.db import models

# Create your models here.
class Parents(models.Model):
    ParentId = models.AutoField(primary_key=True)
    ParentName = models.CharField(max_length = 100)
    ParentMail = models.EmailField()
    ParentPwd = models.CharField(max_length =20)
    ParentTel = models.CharField(max_length =20)
    ParentVille = models.CharField(max_length =20)
    ParentRegion = models.CharField(max_length =20)

class Enfants(models.Model):
    EnfantId=models.AutoField(primary_key=True)
    EnfantAge = models.CharField(max_length=2)
    EnfantName = models.CharField(max_length=100)
    EnfantSexe = models.CharField(max_length=100)
    EnfantParentId = models.CharField(max_length=100)
    EnfantEthmicity = models.CharField(max_length=100,default="black")
    EnfantJaundice = models.CharField(max_length=100,default="Yes")
    EnfantFamelyMsd = models.CharField(max_length=100,default="False")

class TestsAutisme(models.Model):
    TestsAutismeId = models.AutoField(primary_key=True)
    TestIdEnfant = models.CharField(max_length=100,default="0")
    TestQ1=models.CharField(max_length=10)
    TestQ2=models.CharField(max_length=2)
    TestQ3=models.CharField(max_length=2)
    TestQ4=models.CharField(max_length=2)
    TestQ5=models.CharField(max_length=2)
    TestQ6=models.CharField(max_length=2)
    TestQ7=models.CharField(max_length=2)
    TestQ8=models.CharField(max_length=2)
    TestQ9=models.CharField(max_length=2)
    TestQ10=models.CharField(max_length=2)
    TestScore=models.CharField(max_length=100,default="0")
