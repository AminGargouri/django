# Generated by Django 4.2.3 on 2023-08-05 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutismAPP', '0003_enfants_enfantautiste_alter_testsautisme_testq1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enfants',
            name='EnfantAutiste',
            field=models.CharField(default='no', max_length=100),
        ),
    ]
