# Generated by Django 3.1.4 on 2021-05-08 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Facturacion', '0026_auto_20210508_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gestion_inventario',
            name='tipo_problema',
            field=models.IntegerField(),
        ),
    ]
