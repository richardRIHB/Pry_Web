# Generated by Django 3.1.4 on 2021-04-10 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Facturacion', '0005_auto_20210323_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentas',
            name='estado_venta',
            field=models.BooleanField(default=False),
        ),
    ]
