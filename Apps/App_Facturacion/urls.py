from django.urls import path

from Apps.App_Facturacion.views.compra.views import CompraCreateView, compra_view, CompraUpdateView, CompraPdfView
from Apps.App_Facturacion.views.cuentas_compra.views import cuentas_compra_list_view, cuentas_compra_pfd_view
from Apps.App_Facturacion.views.devolucion.views import devolucion_create_view, devolucion_list_view, devolucion_factura_view
from Apps.App_Facturacion.views.devolucion_compra.views import devolucion_compra_list_view, devolucion_compra_create_view, devolucion_compra_pdf_view
from Apps.App_Facturacion.views.empresa.views import empresa_view
from Apps.App_Facturacion.views.galeria.views import galeria_view, galeria_show_view
from Apps.App_Facturacion.views.inventario.views import inventario_view
from Apps.App_Facturacion.views.marca.views import marca_show_view, marca_view
from Apps.App_Facturacion.views.pedido.views import pedido_list_view, pedido_recibo_view
from Apps.App_Facturacion.views.producto.views import producto_view, producto_show_view
from Apps.App_Facturacion.views.producto_deteriorado.views import gestion_inventario_list_view
from Apps.App_Facturacion.views.proforma.views import proforma_list_view, proforma_create_view, proforma_update_view, \
    proforma_factura_view
from Apps.App_Facturacion.views.proforma_compra.views import proforma_compra_list_view, proforma_compra_create_view, proforma_compra_update_view, proforma_compra_pdf_view
from Apps.App_Facturacion.views.proveedor.views import proveedor_view, proveedor_show_view
from Apps.App_Facturacion.views.ubicacion.views import ubicacion_view
from Apps.App_Facturacion.views.venta.views import venta_list_view, venta_create_view, \
    venta_update_view, venta_factura_view
from Apps.App_Facturacion.views.views import *
from Apps.App_Facturacion.views.dashboard.views import dashboard_view
from Apps.App_Facturacion.views.cuentas.views import cuentas_list_view, cuentas_recibo_view

app_name = 'App_Facturacion'

urlpatterns = [
    path('cliente/list/', cliente_view.as_view(), name='cliente_list'),
    path('cliente/show/<int:pk>/', cliente_show_view.as_view(), name='cliente_show'),
    path('dashboard/', dashboard_view.as_view(), name='dashboard'),
    path('venta/list/', venta_list_view.as_view(), name='venta_list'),
    path('venta/add/', venta_create_view.as_view(), name='venta_create'),
    path('venta/update/<int:pk>/', venta_update_view.as_view(), name='venta_update'),
    path('venta/factura/pdf/<int:pk>/', venta_factura_view.as_view(), name='venta_factura'),
    path('cuentas/list/', cuentas_list_view.as_view(), name='cuentas_list'),
    path('cuentas/recibo/<int:pk>/', cuentas_recibo_view.as_view(), name='cuentas_recibo'),
    path('proforma/list/', proforma_list_view.as_view(), name='proforma_list'),
    path('proforma/create/', proforma_create_view.as_view(), name='proforma_create'),
    path('proforma/update/<int:pk>/', proforma_update_view.as_view(), name='proforma_update'),
    path('proforma/factura/pdf/<int:pk>/', proforma_factura_view.as_view(), name='proforma_factura'),
    path('pedido/list/', pedido_list_view.as_view(), name='pedido_list'),
    path('pedido/recibo/<int:pk>/', pedido_recibo_view.as_view(), name='pedido_recibo'),
    #Devolucion
    path('devolucion/add/', devolucion_create_view.as_view(), name='devolucion_create'),
    path('devolucion/list/', devolucion_list_view.as_view(), name='devolucion_list'),
    path('devolucion/factura/pdf/<int:pk>/', devolucion_factura_view.as_view(), name='devolucion_factura_pdf'),
    #Producto
    path('producto/list/', producto_view.as_view(), name='producto_list'),
    path('producto/show/<int:pk>/', producto_show_view.as_view(), name='producto_show'),
    path('marca/list/', marca_view.as_view(), name='marca_list'),
    path('marca/show/<int:pk>/', marca_show_view.as_view(), name='marca_show'),
    path('galeria/list/', galeria_view.as_view(), name='galeria_list'),
    path('galeria/show/<int:pk>/', galeria_show_view.as_view(), name='galeria_show'),
    path('ubicacion/list/', ubicacion_view.as_view(), name='ubicacion_list'),
    #Gestion inventario
    path('gestion/inventario/list/', gestion_inventario_list_view.as_view(), name='gestion_inventario_list'),
    #Proveedor
    path('proveedor/list/', proveedor_view.as_view(), name='proveedor_list'),
    path('proveedor/show/<int:pk>/', proveedor_show_view.as_view(), name='proveedor_show'),
    #Compra
    path('compra/add/', CompraCreateView.as_view(), name='compra_create'),
    path('compra/list/', compra_view.as_view(), name='compra_list'),
    path('compra/update/<int:pk>/', CompraUpdateView.as_view(), name='compra_update'),
    path('compra/pdf/<int:pk>/', CompraPdfView.as_view(), name='compra_pdf'),
    #Proforma Compra
    path('proforma/compra/add/', proforma_compra_create_view.as_view(), name='proforma_compra_create'),
    path('proforma/compra/list/', proforma_compra_list_view.as_view(), name='proforma_compra_list'),
    path('proforma/compra/update/<int:pk>/', proforma_compra_update_view.as_view(), name='proforma_compra_update'),
    path('proforma/compra/pdf/<int:pk>/', proforma_compra_pdf_view.as_view(), name='proforma_compra_pdf'),
    #Cuentas de compra
    path('cuentas/compra/list/', cuentas_compra_list_view.as_view(), name='cuentas_compra_list'),
    path('cuentas/compra/pdf/<int:pk>/', cuentas_compra_pfd_view.as_view(), name='cuentas_compra_pdf'),
    #Devolucion de compra
    path('devolucion/compra/add/', devolucion_compra_create_view.as_view(), name='devolucion_compra_create'),
    path('devolucion/compra/list/', devolucion_compra_list_view.as_view(), name='devolucion_compra_list'),
    path('devolucion/compra/pdf/<int:pk>/', devolucion_compra_pdf_view.as_view(), name='devolucion_compra_pdf'),
    #empresa
    path('empresa/', empresa_view.as_view(), name='empresa'),
    #inventario
    path('inventario/list/', inventario_view.as_view(), name='inventario_list'),

]
