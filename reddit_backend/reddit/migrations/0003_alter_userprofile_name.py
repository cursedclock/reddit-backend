# Generated by Django 3.2.8 on 2022-01-25 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0002_auto_20220125_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]