from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from Apps.App_Facturacion.models import Cliente, Producto, Venta, Marca, Proveedor, Compra, Cuentas_Compra, \
    Devolucion_Compra, Detalle_Compra, Inventario, Empresa, Pedido
from django.utils.translation import get_language, activate
from datetime import datetime
from django.template.defaultfilters import date
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from Apps.App_Facturacion.models import Venta, Producto, Detalle_Venta
from Apps.User.models import User

class dashboard_view(LoginRequiredMixin, TemplateView):
    template_name = 'App_Facturacion/dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = []
        try:
            activate('es')
            action = request.POST['action']
            if action == 'get_graph_sales_year_month':
                data.append({
                    'name': 'Ventas Facturadas',
                    'data': self.get_graph_sales_year_month()
                })
                data.append({
                    'name': 'Ventas a Credito',
                    'data': self.get_graph_venta_metodo_pago()
                })
                data.append({
                    'name': 'Ventas Entregadas',
                    'data': self.get_graph_venta_estado_entrega()
                })
                data.append({
                    'name': 'Proformas',
                    'data': self.get_graph_venta_tipo_documento()
                })
            elif action == 'get_graph_sales_products_year_month':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.get_graph_sales_products_year_month(),
                }
            elif action == 'grafico_compra_producto_por_mes':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.grafico_compra_producto_por_mes(),
                }
            elif action == 'get_graph_online':
                data = {'y': self.grafico_venta_producto_por_hora()}
            else:
                data['error'] = 'Ha ocurrido un error'


        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Venta.objects.filter(fecha__year=year, fecha__month=m, estado=True,tipo_documento=False).aggregate(
                    r=Coalesce(Sum('total'), 0)).get('r')
                data.append(float(total))
        except:
            pass
        return data

    def get_graph_venta_metodo_pago(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Venta.objects.filter(fecha__year=year, fecha__month=m, metodo_pago=True,estado=True).aggregate(
                    r=Coalesce(Sum('total'), 0)).get('r')
                data.append(float(total))
        except:
            pass
        return data

    def get_graph_venta_estado_entrega(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Pedido.objects.filter(fecha__year=year, fecha__month=m, estado=True,estado_entrega=True).aggregate(
                    r=Coalesce(Sum('total'), 0)).get('r')
                data.append(float(total))
        except:
            pass
        return data

    def get_graph_venta_tipo_documento(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Venta.objects.filter(fecha__year=year, fecha__month=m, tipo_documento=True).aggregate(
                    r=Coalesce(Sum('total'), 0)).get('r')
                data.append(float(total))
        except:
            pass
        return data

    def get_graph_sales_products_year_month(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for p in Producto.objects.all():
                total = Detalle_Venta.objects.filter(venta__fecha__year=year, venta__fecha__month=month,
                                                     inventario__producto_id=p.id).aggregate(
                    r=Coalesce(Sum('total'), 0)).get('r')
                if total > 0:
                    data.append({
                        'name': p.nombre,
                        'y': float(total)
                    })
        except:
            pass
        return data

    def grafico_compra_producto_por_mes(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for p in Producto.objects.all():
                total = Detalle_Compra.objects.filter(compra__fecha__year=year, compra__fecha__month=month,
                                                     producto_id=p.id).aggregate(
                    r=Coalesce(Sum('subtotal'), 0)).get('r')
                if total > 0:
                    data.append({
                        'name': p.nombre,
                        'y': float(total)
                    })
        except:
            pass
        return data

    def grafico_venta_producto_por_hora(self):
        year = datetime.now().year
        month = datetime.now().month
        dia = datetime.now().day
        total = 0
        try:
            total = Detalle_Venta.objects.filter(venta__fecha__year=year, venta__fecha__month=month,
                                                 venta__fecha__day=dia).aggregate(
                r=Coalesce(Sum('total'), 0)).get('r')
            total = float(total)
        except:
            pass
        return total

    def get_empresa(self):
        data = ''
        try:
            emp = Empresa.objects.get(pk=1)
            data = emp.id
        except:
            data = 'null'
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['count_cliente'] = Cliente.objects.count()
        context['count_producto'] = Producto.objects.count()
        context['count_venta'] = Venta.objects.count()
        context['count_proveedor'] = Proveedor.objects.count()
        context['count_compra'] = Compra.objects.count()
        context['count_proforma_compra'] = Compra.objects.filter(tipo_documento=True).count()
        context['count_cuentas_compra'] = Cuentas_Compra.objects.filter(estado=False).count()
        context['count_devolucion_compra'] = Devolucion_Compra.objects.filter(estado=True).count()
        context['count_usuario'] = User.objects.all().count()
        context['count_inventario'] = Inventario.objects.all().count()
        context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        context['year_actual'] = datetime.now().year
        context['emp_id'] = self.get_empresa()
        today = datetime.now()
        context['mes_actual'] = date(today, 'F')
        return context
