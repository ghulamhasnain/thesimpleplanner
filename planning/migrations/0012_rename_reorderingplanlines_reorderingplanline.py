# Generated by Django 3.2.9 on 2022-07-24 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0011_auto_20220724_1004'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReorderingPlanLines',
            new_name='ReorderingPlanLine',
        ),
    ]
