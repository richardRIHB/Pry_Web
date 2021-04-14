from django.forms import *

class report_form(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    cliente = CharField(widget=Select(attrs={
        'class': 'form-control select2',
        'autocomplete': 'off',
        'style': 'width: 80%',
        'required': 'True'
    }))

class reporte_producto_form(Form):
    proveedor = CharField(widget=Select(attrs={
        'class': 'form-control select2',
        'autocomplete': 'off',
        'style': 'width: 100%',
        'required': 'True'
    }))

class report_compra_form(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    proveedor = CharField(widget=Select(attrs={
        'class': 'form-control select2',
        'autocomplete': 'off',
        'style': 'width: 80%',
        'required': 'True'
    }))

class report_cuentas_compra_form(Form):
    proveedor = CharField(widget=Select(attrs={
        'class': 'form-control select2',
        'autocomplete': 'off',
        'style': 'width: 100%',
        'required': 'True'
    }))

class report_cuentas_venta_form(Form):
    cliente = CharField(widget=Select(attrs={
        'class': 'form-control select2',
        'autocomplete': 'off',
        'style': 'width: 100%',
        'required': 'True'
    }))

class report_inventario_form(Form):
    producto = CharField(widget=Select(attrs={
        'class': 'form-control select2',
        'autocomplete': 'off',
        'style': 'width: 90%',
        'required': 'True'
    }))

