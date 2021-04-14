# Generated by Django 3.1.4 on 2021-04-10 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_Facturacion', '0006_cuentas_estado_venta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalle_venta',
            name='producto',
        ),
        migrations.AddField(
            model_name='detalle_venta',
            name='inventario',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.PROTECT, to='App_Facturacion.inventario'),
            preserve_default=False,
        ),
    ]
