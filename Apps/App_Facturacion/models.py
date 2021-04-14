from crum import get_current_user
from django.db import models
from datetime import datetime
from Apps.models import base_model
from Pry_Web.settings import MEDIA_URL, STATIC_URL
from django.forms import model_to_dict
from django.conf import settings


class Cliente(models.Model):
    ruc = models.CharField(max_length=13, blank=True, null=True, unique=True)
    ubicacion = models.CharField(max_length=500, blank=True, null=True)
    ubicacion_link = models.CharField(max_length=100, blank=True, null=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(default="Milagro", max_length=50, blank=True, null=True)
    c_i = models.CharField(max_length=10, verbose_name="Cedula de Identidad", unique=True)
    celular = models.CharField(max_length=10, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    estado = models.BooleanField(default=True)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='cliente_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='cliente_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        db_table = 'cliente'
        ordering = ['id']

    def get_full_name(self):
        return '{} {}'.format(self.nombre, self.apellido)

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.__str__()
        item['full_name'] = self.get_full_name()
        return item

    def __str__(self):
        return self.nombre + ' ' + self.apellido


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=datetime.now)
    iva_base = models.DecimalField(default=0.12, max_digits=3, decimal_places=2)
    iva = models.DecimalField(default=0.12, max_digits=5, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    metodo_pago = models.BooleanField(default=False)
    tipo_documento = models.BooleanField(default=False)
    estado = models.BooleanField(default=True)
    estado_pedido = models.BooleanField(default=False)
    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='venta_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='venta_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        db_table = 'venta'
        ordering = ['id']

    def __str__(self):
        return self.cliente.nombre

    def toJSON(self):
        det = []
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['iva_base']=format(self.iva_base, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha'] = self.fecha.strftime('%x <span class="bg-blue btn-xs">%I:%M %p</span>')
        for i in self.detalle_venta_set.all():
            det.append(i.toJSON())
        item['det'] = det
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Venta, self).save()

class Pedido(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=datetime.now)
    fecha_entrega = models.DateTimeField(default=datetime.now)
    ubicacion = models.CharField(max_length=500, blank=True, null=True)
    ubicacion_link = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True, max_length=150)
    estado = models.BooleanField(default=True)
    estado_entrega = models.BooleanField(default=False)
    total = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='pedido_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='pedido_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        db_table = 'pedido'
        ordering = ['id']

    def __str__(self):
        return self.venta.cliente.nombre + ' ' + self.venta.cliente.apellido

    def toJSON(self):
        item = model_to_dict(self)
        item['venta'] = self.venta.toJSON()
        item['total'] = format(self.total, '.2f')
        item['fecha'] = self.fecha.strftime('%x <span class="bg-blue btn-xs">%H:%M %p</span>')
        item['fecha_entrega'] = self.fecha_entrega.strftime('%x <span class="bg-blue btn-xs">%H:%M %p</span>')

        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Pedido, self).save()


class Cuentas(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=datetime.now)
    descripcion = models.TextField(blank=False, null=False)
    valor = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    saldo = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    estado = models.BooleanField(default=False)
    estado_venta = models.BooleanField(default=True)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='cuentas_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='cuentas_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def toJSON(self):
        cuentas = model_to_dict(self)
        cuentas['venta'] = self.venta.toJSON()
        cuentas['fecha'] = self.fecha.strftime('%x <span class="bg-blue btn-xs">%H:%M %p</span>')
        return cuentas


class Abono(models.Model):
    cuentas = models.ForeignKey(Cuentas, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=datetime.now)
    valor = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    estado = models.BooleanField(default=True)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='abono_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='abono_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def toJSON(self):
        abono = model_to_dict(self)
        abono['cuentas'] = self.cuentas.toJSON()
        abono['fecha'] = self.fecha.strftime('%x <span class="bg-blue btn-xs">%H:%M %p</span>')
        return abono

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user

        super(Abono, self).save()


class Marca(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(max_length=200, blank=True, null=True)
    estado = models.BooleanField(default=True)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='marca_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='marca_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        db_table = 'marca'
        ordering = ['id']

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['user_creation', 'user_updated'])
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Marca, self).save()


# Bloque, Seccion y Posicion pertenecen a un mismo Modulo - Modulo Ubicacion
class Bloque(models.Model):
    nombre = models.CharField(max_length=1)
    descripcion = models.TextField(max_length=200, blank=True, null=True)
    estado = models.BooleanField(default=True)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='bloque_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='bloque_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Bloque"
        verbose_name_plural = "Bloques"
        db_table = 'bloque'
        ordering = ['id']

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['user_creation', 'user_updated'])
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Bloque, self).save()


class Seccion(models.Model):
    nombre = models.CharField(max_length=1)
    descripcion = models.TextField(max_length=200, blank=True, null=True)
    estado = models.BooleanField(default=True)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='seccion_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='seccion_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Seccion"
        verbose_name_plural = "Secciones"
        db_table = 'seccion'
        ordering = ['id']

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['user_creation', 'user_updated'])
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Seccion, self).save()


class Posicion(models.Model):
    nombre = models.CharField(max_length=1)
    descripcion = models.TextField(max_length=200, blank=True, null=True)
    estado = models.BooleanField(default=True)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='posicion_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='posicion_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Posicion"
        verbose_name_plural = "Posiciones"
        db_table = 'posicion'
        ordering = ['id']

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['user_creation', 'user_updated'])
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Posicion, self).save()


class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(max_length=200)
    precio = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name='PVP')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    bloque = models.ForeignKey(Bloque, on_delete=models.CASCADE)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    posicion = models.ForeignKey(Posicion, on_delete=models.CASCADE)
    stock = models.DecimalField(default=0.00, max_digits=9, decimal_places=4)
    stock_minimo = models.IntegerField(default=0)
    estado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='producto/%Y/%m/%d',
                               null=True, blank=True, verbose_name='Imagen')
    iva = models.DecimalField(default=0.12, max_digits=3, decimal_places=2)
    porcentaje_ganancia = models.DecimalField(default=0.00, max_digits=5, decimal_places=2,
                                              verbose_name='Porcentaje de Ganancia')
    precio_bruto = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name='Precio Base')

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='producto_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='producto_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        db_table = 'producto'
        ordering = ['id']

    def __str__(self):
        return self.nombre

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['user_creation', 'user_updated'])
        item['marca'] = self.marca.toJSON()
        item['bloque'] = self.bloque.toJSON()
        item['seccion'] = self.seccion.toJSON()
        item['posicion'] = self.posicion.toJSON()
        item['stock'] = format(self.stock, '.4f')
        item['imagen'] = self.get_image()
        item['precio'] = format(self.precio, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['precio_bruto'] = format(self.precio_bruto, '.2f')
        item['porcentaje_ganancia'] = format(self.porcentaje_ganancia, '.2f')
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Producto, self).save()

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    medida = models.CharField(max_length=30)
    equivalencia = models.DecimalField(default=0.00, max_digits=7, decimal_places=3)
    pvp_medida = models.DecimalField(default=0.00, max_digits=8, decimal_places=4)
    porcentaje_conversion = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    tipo_conversion = models.BooleanField(default=True)
    conversion_stock = models.DecimalField(default=0.00, max_digits=8, decimal_places=4)
    estado = models.BooleanField(default=True)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='inventario_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='inventario_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventario"
        db_table = 'inventario'
        ordering = ['id']

    def __str__(self):
        return self.producto.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['user_creation', 'user_updated'])
        item['producto'] = self.producto.toJSON()
        item['equivalencia'] = format(self.equivalencia, '.3f')
        item['pvp_medida'] = format(self.pvp_medida, '.4f')
        item['porcentaje_conversion'] = format(self.porcentaje_conversion, '.2f')
        item['conversion_stock'] = format(self.conversion_stock, '.4f')
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Inventario, self).save()


class Galeria(models.Model):
    nombre = models.CharField(max_length=30)
    ruta = models.ImageField(upload_to='galeia/%Y/%m/%d', null=True, blank=True, verbose_name='Galería')
    estado = models.BooleanField(default=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='galeria_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='galeria_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Galeria"
        verbose_name_plural = "Galerias"
        db_table = 'galeria'
        ordering = ['id']

    def __str__(self):
        return self.nombre

    def get_image(self):
        if self.ruta:
            return '{}{}'.format(MEDIA_URL, self.ruta)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['user_creation', 'user_updated'])
        item['producto'] = self.producto.toJSON()
        item['ruta'] = self.get_image()
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Galeria, self).save()


class Detalle_Venta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    inventario = models.ForeignKey(Inventario, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    descuento = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='detalle_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='detalle_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        db_table = 'detalle_venta'
        ordering = ['id']

    def __str__(self):
        return self.inventario.producto.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['venta'])
        item['inventario'] = self.inventario.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.total, '.2f')
        return item


class Proveedor(models.Model):
    ruc = models.CharField(max_length=13, blank=True, null=True, unique=True, verbose_name='Ruc de la Empresa')
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    empresa = models.CharField(max_length=30)
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(default="Milagro", max_length=50, blank=True, null=True)
    c_i = models.CharField(max_length=10, verbose_name="Cedula de Identidad", unique=True)
    celular = models.CharField(max_length=10, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    imagen = models.ImageField(upload_to='proveedor/%Y/%m/%d', null=True, blank=True,
                               verbose_name='Logotipo de la Empresa')
    estado = models.BooleanField(default=True)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='proveedor_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='proveedor_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        db_table = 'proveedor'
        ordering = ['id']

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['proveedor'] = self.__str__()
        item['imagen'] = self.get_image()
        return item

    def __str__(self):
        return self.nombre + ' ' + self.apellido


class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    iva_base = models.DecimalField(max_digits=3, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    tipo_documento = models.BooleanField(default=False)
    metodo_pago = models.BooleanField(default=False)
    estado = models.BooleanField(default=True)
    estado_devolucion_c = models.BooleanField(default=False)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='compra_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='compra_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.proveedor.nombre

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        db_table = 'compra'
        ordering = ['id']

    def toJSON(self):
        item = model_to_dict(self)
        item['proveedor'] = self.proveedor.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva_base'] = format(self.iva_base, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha'] = self.fecha.strftime('%d/%m/%Y')
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Compra, self).save()


class Detalle_Compra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)  # Precio bruto de Compra
    precio_antiguo = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)  # Precio bruto antiguo
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='detalle_compra_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='detalle_compra_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.producto.nombre

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compras'
        db_table = 'detalle_compra'
        ordering = ['id']

    def toJSON(self):
        item = model_to_dict(self, exclude=['compra'])
        item['producto'] = self.producto.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['cantidad'] = format(self.cantidad, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Detalle_Compra, self).save()


class Cuentas_Compra(models.Model):
    compra = models.OneToOneField(Compra, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=datetime.now)
    descripcion = models.TextField(blank=False, null=False)
    valor = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    saldo = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    estado = models.BooleanField(default=False)
    estado_compra = models.BooleanField(default=True)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='cuentas_compra_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='cuentas_compra_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Cuenta de Compra'
        verbose_name_plural = 'Cuenta de Compras'
        db_table = 'cuentas_compra'
        ordering = ['id']

    def toJSON(self):
        cuentas = model_to_dict(self)
        cuentas['compra'] = self.compra.toJSON()
        self.fecha.strftime('%d/%m/%Y')
        cuentas['fecha'] = self.fecha.strftime('%d/%m/%Y <span class="bg-blue btn-xs">%H:%M %p</span>')
        return cuentas

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Cuentas_Compra, self).save()


class Abono_Compra(models.Model):
    cuentas_compra = models.ForeignKey(Cuentas_Compra, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=datetime.now)
    valor = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    estado = models.BooleanField(default=True)
    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='abono_compra_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='abono_compra_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Abono de Compra'
        verbose_name_plural = 'Abono de Compras'
        db_table = 'abono_compra'
        ordering = ['id']

    def toJSON(self):
        abono = model_to_dict(self)
        abono['cuentas_compra'] = self.cuentas_compra.toJSON()
        abono['fecha'] = self.fecha.strftime('%x <span class="bg-blue btn-xs">%H:%M %p</span>')
        return abono

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user

        super(Abono_Compra, self).save()


class Devolucion_Compra(models.Model):
    compra = models.OneToOneField(Compra, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.BooleanField(default=True)

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='devolucion_compra_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='devolucion_compra_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.compra.proveedor.nombre

    class Meta:
        verbose_name = 'Devolucion de Compra'
        verbose_name_plural = 'Devolucion de Compras'
        db_table = 'devolucion_compra'
        ordering = ['id']

    def toJSON(self):
        item = model_to_dict(self)
        item['compra'] = self.compra.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha'] = self.fecha.strftime('%d/%m/%Y')
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Devolucion_Compra, self).save()


class Devolucion_Detalle_Compra(models.Model):
    devolucion_compra = models.ForeignKey(Devolucion_Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    precio_antiguo_ddc = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='devolucion_detalle_compra_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='devolucion_detalle_compra_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.producto.nombre

    class Meta:
        verbose_name = 'Devolucion de Detalle de Compra'
        verbose_name_plural = 'Devolucion de Detalle de Compras'
        db_table = 'devolucion_detalle_compra'
        ordering = ['id']

    def toJSON(self):
        item = model_to_dict(self, exclude=['devolucion_compra'])
        item['producto'] = self.producto.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['cantidad'] = format(self.cantidad, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Devolucion_Detalle_Compra, self).save()


class Empresa(models.Model):
    nombre = models.CharField(max_length=35, verbose_name='Nombre de la Empresa')
    ruc = models.CharField(max_length=13, unique=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    correo = models.EmailField(max_length=35, blank=True, null=True)
    ciudad = models.CharField(default="Milagro", max_length=30)
    direccion = models.CharField(max_length=45)
    sitio_web = models.CharField(max_length=35)
    iva = models.DecimalField(default=0.12, max_digits=3, decimal_places=2)
    imagen = models.ImageField(upload_to='empresa/%Y/%m/%d', null=True, blank=True,
                               verbose_name='Logotipo de la Empresa')
    logo_login = models.ImageField(upload_to='logo_login/%Y/%m/%d', null=True, blank=True,
                                   verbose_name='Logo del login')

    # Auditoria
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='empresa_user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='empresa_user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresa"
        db_table = 'empresa'

    def __str__(self):
        return self.nombre

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/logo.png')

    def get_image_login(self):
        if self.logo_login:
            return '{}{}'.format(MEDIA_URL, self.logo_login)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['user_creation', 'user_updated'])
        item['imagen'] = self.get_image()
        item['iva'] = format(self.iva, '.2f')
        item['logo_login'] = self.get_image_login()
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Empresa, self).save()


