# Generated by Django 3.2.9 on 2022-07-18 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0004_auto_20220708_2114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='product',
        ),
        migrations.AddField(
            model_name='inventory',
            name='material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material_inventory', to='planning.material'),
        ),
    ]
