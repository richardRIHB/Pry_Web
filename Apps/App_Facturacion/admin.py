from django.contrib import admin

# Register your models here.
from django.contrib import admin
from Apps.App_Facturacion.models import Cliente, Producto, Venta, Detalle_Venta, Pedido, Marca, Bloque, Seccion, Posicion, Galeria, Compra, Detalle_Compra, Proveedor


class Cliente_Admin(admin.ModelAdmin):
    list_display = ("nombre","apellido","ruc","c_i","direccion","ciudad","celular","correo","estado",
                    "user_creation","date_creation","user_updated","date_updated")
    search_fields = ("nombre",'apellido','c_i')

class Producto_Admin((admin.ModelAdmin)):
    list_filter=("nombre","descripcion","precio","estado",
                 "user_creation","date_creation","user_updated","date_updated")
    list_display = ("nombre", "descripcion", "precio", "stock", "estado", "imagen",
                    "user_creation", "date_creation", "user_updated", "date_updated")

class Venta_Admin((admin.ModelAdmin)):
    list_display=("id","fecha","total","estado",
                  "user_creation","date_creation","user_updated","date_updated")
    list_filter=("fecha","estado")
    date_hierarchy="fecha"

class Marca_Admin(admin.ModelAdmin):
    list_filter= ["estado"]
    list_display = ("nombre","descripcion","estado")


class Bloque_Admin(admin.ModelAdmin):
    list_filter = ["estado"]
    list_display = ("nombre", "descripcion", "estado")

class Seccion_Admin(admin.ModelAdmin):
    list_filter= ["estado"]
    list_display = ("nombre","descripcion","estado")

class Posicion_Admin(admin.ModelAdmin):
    list_filter= ["estado"]
    list_display = ("nombre","descripcion","estado")

class Galeria_Admin(admin.ModelAdmin):
    list_filter= ["estado"]
    list_display = ("nombre","ruta","estado")

class Compra_Admin((admin.ModelAdmin)):
    list_display=("id","fecha","total","estado")
    list_filter=("fecha","estado")
    date_hierarchy="fecha"

class Proveedor_Admin(admin.ModelAdmin):
    list_display = ("nombre","apellido","ruc","c_i","empresa","direccion","ciudad","celular","correo","estado")
    search_fields = ("nombre",'apellido','c_i')

admin.site.register(Cliente, Cliente_Admin)
admin.site.register(Producto,Producto_Admin)
admin.site.register(Venta,Venta_Admin)
admin.site.register(Detalle_Venta)
admin.site.register(Pedido)
admin.site.register(Marca, Marca_Admin)
admin.site.register(Bloque, Bloque_Admin)
admin.site.register(Seccion, Seccion_Admin)
admin.site.register(Posicion, Posicion_Admin)
admin.site.register(Galeria, Galeria_Admin)
admin.site.register(Proveedor, Proveedor_Admin)
admin.site.register(Compra,Compra_Admin)
admin.site.register(Detalle_Compra)