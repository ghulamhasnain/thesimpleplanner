# Generated by Django 3.2.2 on 2022-07-31 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0013_reorderingplan_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
