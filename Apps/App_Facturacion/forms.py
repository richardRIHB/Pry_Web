from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime
from django.forms import *

from Apps.App_Facturacion.models import Cliente, Producto, Venta, Abono, Pedido, Marca, Galeria, Bloque, Proveedor, \
    Compra, Abono_Compra, Devolucion_Compra, Empresa, Inventario, Devolucion, Gestion_Inventario
from tempus_dominus.widgets import DateTimePicker

class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

class cliente_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']
        widgets = {
            'ruc': TextInput(
                attrs={
                    'autofocus': "autofocus",
                    'placeholder': 'Ingrese el ruc'
                }
            ),
            'ubicacion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la ubicacion del mapa',
                }
            ),
            'ubicacion_link': TextInput(
                attrs={
                    'placeholder': 'Ingrese el link de la ubicacion',
                }
            ),
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese los nombres',
                }
            ),
            'apellido': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la direccion',
                }
            ),
            'ciudad': TextInput(
                attrs={
                    'placeholder': 'Ingrese la ciudad',
                }
            ),
            'c_i': TextInput(
                attrs={
                    'placeholder': 'Ingrese la cedula de identidad',
                }
            ),
            'celular': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero de celular',
                }
            ),
            'correo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el correo electronico o email',
                }
            ),
        }

    def clean_ruc(self):
        ruc = self.cleaned_data['ruc']
        mensaje = 'Introduzca un Ruc valido.'
        try:
            if ruc:
                print(ruc)
                convertidor = int(ruc)
                longitud = len(ruc)
                if ruc.isdigit() == False:
                    raise ValidationError(mensaje)
                elif longitud != 13:
                    mensaje = 'Asegúrate de que el Ruc tenga 13 digitos.'
                    raise ValidationError(mensaje)
        except:
            raise ValidationError(mensaje)
        return ruc

    def clean_c_i(self):
        c_i = self.cleaned_data['c_i']
        mensaje = 'Introduzca una Cédula de Identidad valido.'
        try:
            convertidor = int(c_i)
            longitud = len(c_i)
            if c_i.isdigit() == False:
                raise ValidationError(mensaje)
            elif longitud != 10:
                mensaje = 'Asegúrate de que la Cédula de Identidad tenga 10 digitos.'
                raise ValidationError(mensaje)
        except:
            raise ValidationError(mensaje)
        return c_i

    def clean_celular(self):
        celular = self.cleaned_data['celular']
        mensaje = 'Introduzca un Numero de Celular valido.'
        try:
            if celular:
                convertidor = int(celular)
                longitud = len(celular)
                if celular.isdigit() == False:
                    raise ValidationError(mensaje)
                elif longitud != 10:
                    mensaje = 'Asegúrate de que el Numero de Celular tenga 10 digitos.'
                    raise ValidationError(mensaje)
        except:
            raise ValidationError(mensaje)
        return celular

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str("e")
        return data

class producto_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Producto
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del producto',
                }
            ),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese la descripcion',
                    'rows': 3,
                    'cols': 4
                }
            ),
            'marca': Select(
                attrs={
                    'class': "form-control select2",
                    'style': 'width: 100%',
                }
            ),
            'bloque': Select(
                attrs={
                    'class': "form-control select2",
                    'style': 'width: 100%',
                }
            ),
            'seccion': Select(
                attrs={
                    'class': "form-control select2",
                    'style': 'width: 100%',
                }
            ),
            'posicion': Select(
                attrs={
                    'class': "form-control select2",
                    'style': 'width: 100%',
                }
            ),
            'imagen': FileInput(
                attrs={
                    'class': 'nuestroinput',
                    'for': 'nuestroinput',
                    'onchange': 'return validarInputFile()'
                }
            ),
            'precio_bruto': TextInput(
                attrs={
                    'onchange': 'return calcularPVP()',
                }
            ),
            'porcentaje_ganancia': TextInput(
                attrs={
                    'onchange': 'return calcularPVP()',
                }
            ),
            'stock': TextInput(
                attrs={
                }
            ),
            'stock_minimo': TextInput(
                attrs={
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class venta_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Venta
        fields = '__all__'
        widgets = {
            'cliente': Select(attrs={
                'readonly': True,
                'class': 'custom-select select2',
            }),
            'fecha': DateInput(
                format='%d/%m/%Y %I:%M %p',
                attrs={
                    'value': datetime.now().strftime('%d/%m/%Y %I:%M %p'),
                    'autocomplete': 'off',
                    'class': 'form-control',
                    'readonly': True,
                }
            ),
            'iva': TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'metodo_pago': CheckboxInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }

class abonos_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Abono
        fields = '__all__'
        exclude = ['user_updated', 'user_creation', 'estado']
        widgets = {

            'fecha': DateInput(
                #format='%d/%m/%Y %I:%M',
                attrs={
                    #'value': datetime.now().strftime('%d/%m/%Y %I:%M '),
                    'autocomplete': 'off',
                    #'class': 'form-control datetimepicker-input',
                    'id': 'fecha',
                    #'data-target': '#fecha',
                    'class': 'form-control',
                    'readonly': 'on',
                    #'data-toggle': 'datetimepicker',
                }
            ),

            'valor': TextInput(
                attrs={
                    'class': 'form-control',

                }
            ),
            'cuentas': TextInput(
                attrs={
                    'class': 'form-control',
                    'hidden': 'on',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class pedido_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['direccion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Pedido
        fields = '__all__'
        exclude = ['user_updated', 'user_creation', 'estado', 'fecha']
        widgets = {
            'fecha_entrega': DateInput(
                # format='%d/%m/%Y %I:%M %p',
                attrs={
                    'value': datetime.now().strftime('%d/%m/%Y %I:%M %p'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'id_fecha_entrega',
                    'data-target': '#id_fecha_entrega',
                    'data-toggle': 'datetimepicker',
                }
            ),
            'venta': TextInput(
                attrs={
                    'class': 'form-control',
                    'hidden': 'on',
                }
            ),
            'ubicacion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la ubicacion del mapa',
                }
            ),
            'ubicacion_link': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el link de la ubicacion',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'total': TextInput(
                attrs={
                    'class': 'form-control',

                }
            ),
            'descripcion': Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'cols': 4
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class devolucion_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Devolucion
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']
        widgets = {
            'venta': TextInput(
                attrs={
                'class': "form-control",
                'readonly': True,
                }
            ),
            'fecha': DateInput(
                format='%d/%m/%Y %I:%M %p',
                attrs={
                    'value': datetime.now().strftime('%d/%m/%Y %I:%M %p'),
                    'autocomplete': 'off',
                    'class': 'form-control',
                    'readonly': True,
                }
            ),
            'iva': TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
        }

# funcion para añadir validaciones
# def clean(self):
#     cleaned = super().clean()
#     if len(cleaned['nombre']) <= 50:
#         raise forms.ValidationError('Validacion xxx')
#         #self.add_error('nombre', 'Le faltan caracteres')
#     return cleaned


class MarcaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Marca
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre',
                }
            ),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese la descripcion',
                    'rows': 4,
                    'cols': 4
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str("e")
        return data

class GaleriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Galeria
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre',
                }
            ),
            'producto': Select(
                attrs={
                    'class': "form-control select2",
                    'style': 'width: 100%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str("e")
        return data

class UbicacionForm(ModelForm):
    class Meta:
        model = Bloque
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre',
                }
            ),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese la descripcion',
                    'rows': 4,
                    'cols': 4
                }
            ),
        }

class proveedor_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Proveedor
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']
        widgets = {
            'ruc': TextInput(
                attrs={
                    'autofocus': "autofocus",
                    'placeholder': 'Ingrese el ruc',
                    'required': 'True'
                }
            ),
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese los nombres',
                }
            ),
            'apellido': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                }
            ),
            'empresa': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre de la empresa',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la direccion',
                }
            ),
            'ciudad': TextInput(
                attrs={
                    'placeholder': 'Ingrese la ciudad',
                }
            ),
            'c_i': TextInput(
                attrs={
                    'placeholder': 'Ingrese la cedula de identidad',
                }
            ),
            'celular': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero celular',
                }
            ),
            'correo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el correo electronico o email',
                }
            ),
        }

    def clean_ruc(self):
        ruc = self.cleaned_data['ruc']
        mensaje = 'Introduzca un Ruc valido.'
        try:
            convertidor = int(ruc)
            longitud = len(ruc)
            if ruc.isdigit() == False:
                raise ValidationError(mensaje)
            elif longitud != 13:
                mensaje = 'Asegúrate de que el Ruc tenga 13 digitos.'
                raise ValidationError(mensaje)
        except:
            raise ValidationError(mensaje)
        return ruc

    def clean_c_i(self):
        c_i = self.cleaned_data['c_i']
        mensaje = 'Introduzca una Cédula de Identidad valido.'
        try:
            convertidor = int(c_i)
            longitud = len(c_i)
            if c_i.isdigit() == False:
                raise ValidationError(mensaje)
            elif longitud != 10:
                mensaje = 'Asegúrate de que la Cédula de Identidad tenga 10 digitos.'
                raise ValidationError(mensaje)
        except:
            raise ValidationError(mensaje)
        return c_i

    def clean_celular(self):
        celular = self.cleaned_data['celular']
        mensaje = 'Introduzca un Numero de Celular valido.'
        try:
            if celular:
                convertidor = int(celular)
                longitud = len(celular)
                if celular.isdigit() == False:
                    raise ValidationError(mensaje)
                elif longitud != 10:
                    mensaje = 'Asegúrate de que el Numero de Celular tenga 10 digitos.'
                    raise ValidationError(mensaje)
        except:
            raise ValidationError(mensaje)
        return celular

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str("e")
        return data

class compra_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Compra
        fields = '__all__'
        exclude = ['user_updated', 'user_creation', 'estado']
        widgets = {
            'proveedor': Select(
                attrs={
                    'class': "form-control select2",
                    'style': 'width: 100%',
                    'required': 'True'
                }
            ),
            'fecha': DateInput(format='%Y-%m-%d',
                               attrs={
                                   'value': datetime.now().strftime('%Y-%m-%d'),
                                   'autocomplete': 'off',
                                   'class': 'form-control datetimepicker-input',
                                   'id': 'fecha',
                                   'data-target': '#fecha',
                                   'data-toggle': 'datetimepicker',
                               }),
            'iva': TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'metodo_pago': CheckboxInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }

class abonos_compra_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Abono_Compra
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']
        widgets = {

            'fecha': DateInput(
                #format='%d/%m/%Y %I:%M %p',
                attrs={
                    #'value': datetime.now().strftime('%d/%m/%Y %I:%M %p'),
                    'autocomplete': 'off',
                    #'class': 'form-control datetimepicker-input',
                    'class': 'form-control',
                    'id': 'fecha',
                    #'data-target': '#fecha',
                    #'data-toggle': 'datetimepicker',
                    'readonly': True,
                }
            ),

            'valor': TextInput(
                attrs={
                    'class': 'form-control',

                }
            ),
            'cuentas_compra': TextInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                }
            ),
        }

class devolucion_compra_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Devolucion_Compra
        fields = '__all__'
        exclude = ['user_updated', 'user_creation', 'estado']
        widgets = {
            'compra': TextInput(
                attrs={
                    'class': "form-control",
                    'required': 'True',
                    'readonly': True,
                }
            ),
            'fecha': DateInput(format='%Y-%m-%d',
                               attrs={
                                   'value': datetime.now().strftime('%Y-%m-%d'),
                                   'autocomplete': 'off',
                                   'class': 'form-control datetimepicker-input',
                                   'id': 'fecha',
                                   'data-target': '#fecha',
                                   'data-toggle': 'datetimepicker',
                                   'readonly': True,
                               }),
            'iva': TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }

class empresa_form(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Empresa
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']
        widgets = {
            'nombre': TextInput(
                attrs={
                    'autofocus': "autofocus",
                    'placeholder': 'Ingrese el nombre de la empresa',
                }
            ),
            'ruc': TextInput(
                attrs={
                    'placeholder': 'Ingrese el ruc',
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numeor de telefono',
                }
            ),
            'correo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el correo electronico o email',
                }
            ),
            'ciudad': TextInput(
                attrs={
                    'placeholder': 'Ingrese la ciudad',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la direccion',
                }
            ),
            'sitio_web': TextInput(
                attrs={
                    'placeholder': 'Ingrese la direccion del sitio web',
                }
            ),
            'iva': TextInput(
                attrs={
                    'placeholder': 'Ingrese el iva',
                }
            ),
        }

    def clean_ruc(self):
        ruc = self.cleaned_data['ruc']
        mensaje = 'Introduzca un Ruc valido.'
        try:
            convertidor = int(ruc)
            longitud = len(ruc)
            if ruc.isdigit() == False:
                raise ValidationError(mensaje)
            elif longitud != 13:
                mensaje = 'Asegúrate de que el Ruc tenga 13 digitos.'
                raise ValidationError(mensaje)
        except:
            raise ValidationError(mensaje)
        return ruc

    def clean_telefono(self):
        celular = self.cleaned_data['telefono']
        mensaje = 'Introduzca un Numero de Telefono valido.'
        try:
            if celular:
                convertidor = int(celular)
                longitud = len(celular)
                if celular.isdigit() == False:
                    raise ValidationError(mensaje)
                elif longitud != 10:
                    mensaje = 'Asegúrate de que el Numero de Telefono tenga 10 digitos.'
                    raise ValidationError(mensaje)
        except:
            raise ValidationError(mensaje)
        return celular

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str("e")
        return data

class inventario_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Inventario
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']
        widgets = {
            'producto': Select(
                attrs={
                    'class': "form-control select2",
                    'style': 'width: 100%',
                }
            ),
            'medida': TextInput(
                attrs={
                    'placeholder': 'Ingrese la medida del producto',
                }
            ),
            'equivalencia': TextInput(
                attrs={
                    'onchange': 'return calcularPVP()',
                }
            ),
            'pvp_medida': NumberInput(
                attrs={
                    'readonly': True,
                }
            ),
            'porcentaje_conversion': TextInput(
                attrs={
                    'onchange': 'return calcularPVP()',
                }
            ),
            'tipo_conversion': Select(
                attrs={
                    'class': "form-control select2",
                    'style': 'width: 100%',
                }
            ),
            'conversion_stock': TextInput(
                attrs={
                    'readonly': True,
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class gestion_inventario_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Gestion_Inventario
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']
        widgets = {
            'inventario': Select(
                attrs={
                    'class': "form-control select2",
                    'style': 'width: 100%',
                }
            ),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese la descripcion',
                    'class': 'form-control',
                    'rows': 5,
                    'cols': 4
                }
            ),
            'fecha': DateInput(
                attrs={
                    'autocomplete': 'off',
                    'class': 'form-control',
                    'readonly': True,
                }
            ),
            'precio': NumberInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control',
                }
            ),
            'cantidad': TextInput(
                attrs={
                    'onchange': 'return calcularPVP()',
                    'class': 'form-control',
                }
            ),
            'total': NumberInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control',
                }
            ),
            'tipo_problema': Select(
                attrs={
                    'class': "form-control select2",
                    'style': 'width: 100%',

                }
            ),
        }