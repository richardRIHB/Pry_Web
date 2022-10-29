from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from django.contrib import admin
from Apps.App_Facturacion.models import Cliente, Producto, Venta, Detalle_Venta, Pedido, Marca, Bloque, Seccion, Posicion, Galeria, Compra, Detalle_Compra, Proveedor,Inventario
from import_export import resources

# CLASES PARA AGREGAR LA FUNCION DE IMPORTAR Y EXPORTAR EN EL ADMINISTRADOR

class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente

class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto

class VentaResource(resources.ModelResource):
    class Meta:
        model = Venta

class MarcaResource(resources.ModelResource):
    class Meta:
        model = Marca

class BloqueResource(resources.ModelResource):
    class Meta:
        model = Bloque

class SeccionResource(resources.ModelResource):
    class Meta:
        model = Seccion

class PosicionResource(resources.ModelResource):
    class Meta:
        model = Posicion

class GaleriaResource(resources.ModelResource):
    class Meta:
        model = Galeria

class CompraResource(resources.ModelResource):
    class Meta:
        model = Compra

class ProveedorResource(resources.ModelResource):
    class Meta:
        model = Proveedor

class InventarioResource(resources.ModelResource):
    class Meta:
        model = Inventario

# CLASES PARA VISUALIZAR LAS FUNCIONES

class Cliente_Admin(ImportExportModelAdmin):
    list_display = ("nombre","apellido","ruc","c_i","direccion","ciudad","celular","correo","estado",
                    "user_creation","date_creation","user_updated","date_updated")
    search_fields = ("nombre",'apellido','c_i')
    resource_class = ClienteResource

class Producto_Admin(ImportExportModelAdmin):
    list_filter=("estado","user_creation","date_creation","user_updated","date_updated")
    list_display = ("nombre", "descripcion", "precio", "stock", "estado", "imagen",
                    "user_creation", "date_creation", "user_updated", "date_updated")
    resource_class = ProductoResource

class Venta_Admin(ImportExportModelAdmin):
    list_display=("id","fecha","total","estado",
                  "user_creation","date_creation","user_updated","date_updated")
    list_filter=("fecha","estado")
    date_hierarchy="fecha"
    resource_class = VentaResource

class Marca_Admin(ImportExportModelAdmin):
    list_filter= ["estado"]
    list_display = ("nombre","descripcion","estado")
    resource_class = MarcaResource

class Bloque_Admin(ImportExportModelAdmin):
    list_filter = ["estado"]
    list_display = ("nombre", "descripcion", "estado")
    resource_class = BloqueResource

class Seccion_Admin(ImportExportModelAdmin):
    list_filter= ["estado"]
    list_display = ("nombre","descripcion","estado")
    resource_class = SeccionResource

class Posicion_Admin(ImportExportModelAdmin):
    list_filter= ["estado"]
    list_display = ("nombre","descripcion","estado")
    resource_class = PosicionResource

class Galeria_Admin(ImportExportModelAdmin):
    list_filter= ["estado"]
    list_display = ("nombre","ruta","estado")
    resource_class = GaleriaResource

class Compra_Admin(ImportExportModelAdmin):
    list_display=("id","fecha","total","estado")
    list_filter=("fecha","estado")
    date_hierarchy="fecha"
    resource_class = CompraResource

class Proveedor_Admin(ImportExportModelAdmin):
    list_display = ("nombre","apellido","ruc","c_i","empresa","direccion","ciudad","celular","correo","estado")
    search_fields = ("nombre",'apellido','c_i')
    resource_class = ProveedorResource

class Inventario_Admin(ImportExportModelAdmin):
    list_filter = ("estado", "user_creation", "date_creation", "user_updated", "date_updated")
    list_display = ( "producto","medida", "equivalencia", "pvp_medida", "porcentaje_conversion", "tipo_conversion",
                    "conversion_stock", "estado", "user_updated", "date_updated")
    resource_class = InventarioResource

class Detalle_Compra_Admin(ImportExportModelAdmin):
    list_filter = ( "user_creation", "date_creation", "user_updated", "date_updated")
    list_display = ( "compra","producto", "precio", "precio_antiguo", "cantidad", "subtotal",
                     "user_updated", "date_updated")
    resource_class = InventarioResource





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
admin.site.register(Detalle_Compra,Detalle_Compra_Admin)
admin.site.register(Inventario,Inventario_Admin)