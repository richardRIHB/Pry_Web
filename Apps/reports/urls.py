from django.urls import path

from Apps.reports.views.compra.views import report_compra_view, reporte_compra_pdf_view
from Apps.reports.views.cuentas_compra.views import report_cuentas_compra_view, reporte_cuentas_compra_pdf_view
from Apps.reports.views.cuentas_venta.views import report_cuentas_venta_view, reporte_cuentas_venta_pdf_view
from Apps.reports.views.inventario.views import reporte_inventario_view, reporte_inventario_pdf_view
from Apps.reports.views.producto.views import reporte_producto_view, reporte_producto_pdf_view
from Apps.reports.views.venta.views import report_venta_view, reporte_venta_pdf_view
app_name = 'reports'
urlpatterns = [
    # reports
    path('venta/', report_venta_view.as_view(), name='venta_report'),
    path('venta/pdf/<fecha_ini>/<fecha_fin>/<pk>/', reporte_venta_pdf_view.as_view(), name='venta_report_pdf'),
    path('producto/', reporte_producto_view.as_view(), name='producto_report'),
    path('producto/pdf/<filtro>/<pk>/', reporte_producto_pdf_view.as_view(), name='producto_report_pdf'),
    path('compra/', report_compra_view.as_view(), name='compra_report'),
    path('compra/pdf/<fecha_ini>/<fecha_fin>/<pk>/', reporte_compra_pdf_view.as_view(), name='compra_report_pdf'),
    path('cuentas/compra/', report_cuentas_compra_view.as_view(), name='cuentas_compra_report'),
    path('cuentas/compra/pdf/<filtro>/<pk>/', reporte_cuentas_compra_pdf_view.as_view(), name='cuentas_compra_report_pdf'),
    path('cuentas/venta/', report_cuentas_venta_view.as_view(), name='cuentas_venta_report'),
    path('cuentas/venta/pdf/<filtro>/<pk>/', reporte_cuentas_venta_pdf_view.as_view(), name='cuentas_venta_report_pdf'),
    path('inventario/', reporte_inventario_view.as_view(), name='inventario_report'),
    path('inventario/pdf/<filtro>/<pk>/', reporte_inventario_pdf_view.as_view(), name='inventario_report_pdf'),
]