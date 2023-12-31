# Generated by Django 4.2.3 on 2023-07-28 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enfants',
            fields=[
                ('EnfantId', models.AutoField(primary_key=True, serialize=False)),
                ('EnfantAge', models.CharField(max_length=2)),
                ('EnfantName', models.CharField(max_length=100)),
                ('EnfantSexe', models.CharField(max_length=100)),
                ('EnfantParentId', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Parents',
            fields=[
                ('ParentId', models.AutoField(primary_key=True, serialize=False)),
                ('ParentName', models.CharField(max_length=100)),
                ('ParentMail', models.EmailField(max_length=254)),
                ('ParentPwd', models.CharField(max_length=20)),
                ('ParentTel', models.CharField(max_length=20)),
                ('ParentVille', models.CharField(max_length=20)),
                ('ParentRegion', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TestsAutisme',
            fields=[
                ('TestsAutismeId', models.AutoField(primary_key=True, serialize=False)),
                ('TestQ1', models.CharField(max_length=2)),
                ('TestQ2', models.CharField(max_length=2)),
                ('TestQ3', models.CharField(max_length=2)),
                ('TestQ4', models.CharField(max_length=2)),
                ('TestQ5', models.CharField(max_length=2)),
                ('TestQ6', models.CharField(max_length=2)),
                ('TestQ7', models.CharField(max_length=2)),
                ('TestQ8', models.CharField(max_length=2)),
                ('TestQ9', models.CharField(max_length=2)),
                ('TestQ10', models.CharField(max_length=2)),
            ],
        ),
    ]
