# Generated by Django 3.2.2 on 2022-10-18 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0018_delete_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='reorderingplan',
            name='production_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='planning.productionplan'),
        ),
    ]
