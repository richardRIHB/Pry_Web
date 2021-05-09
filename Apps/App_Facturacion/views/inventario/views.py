from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q

from Apps.App_Facturacion.forms import inventario_form
from Apps.App_Facturacion.models import Producto, Inventario
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from datetime import datetime

class inventario_view(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Inventario.objects.all():
                    data.append(i.toJSON())
                # for i in Producto.objects.all():
                #     inv = Inventario()
                #     inv.producto_id = i.pk
                #     inv.medida = 'UND'
                #     inv.equivalencia = 1
                #     inv.pvp_medida = i.precio
                #     inv.porcentaje_conversion = 0
                #     inv.tipo_conversion = True
                #     inv.conversion_stock = 1
                #     inv.estado = True
                #     inv.save()
            elif action == 'search_producto':
                data = []
                prods = Producto.objects.filter(Q(nombre__icontains=request.POST['term']) | Q(descripcion__icontains=request.POST['term']) | Q(marca__nombre__icontains=request.POST['term']))
                for i in prods:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    inv = Inventario()
                    inv.producto_id = request.POST['producto']
                    inv.medida = request.POST['medida']
                    inv.equivalencia = request.POST['equivalencia']
                    inv.pvp_medida = request.POST['pvp_medida']
                    inv.porcentaje_conversion = request.POST['porcentaje_conversion']
                    inv.tipo_conversion = request.POST['tipo_conversion']
                    inv.conversion_stock = request.POST['conversion_stock']
                    inv.estado = request.POST['estado_valor'].capitalize()
                    inv.save()
            elif action == 'edit':
                with transaction.atomic():
                    inv = Inventario.objects.get(pk=request.POST['id'])
                    inv.producto_id = request.POST['producto']
                    inv.medida = request.POST['medida']
                    inv.equivalencia = request.POST['equivalencia']
                    inv.pvp_medida = request.POST['pvp_medida']
                    inv.porcentaje_conversion = request.POST['porcentaje_conversion']
                    inv.tipo_conversion = request.POST['tipo_conversion']
                    inv.conversion_stock = request.POST['conversion_stock']
                    inv.estado = request.POST['estado_valor'].capitalize()
                    inv.save()
            elif action == 'delete':
                with transaction.atomic():
                    inv = Inventario.objects.get(pk=request.POST['id'])
                    inv.estado = False
                    inv.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Inventario'
        context['list_url'] = reverse_lazy('App_Facturacion:inventario_list')
        context['list_producto_url'] = reverse_lazy('App_Facturacion:producto_list')
        context['list_gestion_inventario__url'] = reverse_lazy('App_Facturacion:gestion_inventario_list')
        context['entity'] = 'Inventario'
        context['date_now'] = datetime.now
        context['form'] = inventario_form()
        return context

