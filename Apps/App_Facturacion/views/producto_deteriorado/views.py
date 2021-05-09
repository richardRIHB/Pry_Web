from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q

from Apps.App_Facturacion.forms import gestion_inventario_form
from Apps.App_Facturacion.models import Inventario, Gestion_Inventario, Producto
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from datetime import datetime

class gestion_inventario_list_view(LoginRequiredMixin, TemplateView):
    template_name = 'producto_deteriorado/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Gestion_Inventario.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_inventario':
                data = []
                prods = Inventario.objects.filter(Q(producto__nombre__icontains=request.POST['term']) | Q(producto__descripcion__icontains=request.POST['term']) | Q(producto__marca__nombre__icontains=request.POST['term']))
                for i in prods[0:10]:
                    item = i.toJSON()
                    item['text'] = i.producto.nombre +' '+ i.producto.marca.nombre +' '+ i.medida
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    gestion = Gestion_Inventario()
                    gestion.inventario_id = request.POST['inventario']
                    gestion.descripcion = request.POST['descripcion']
                    gestion.precio = request.POST['precio']
                    gestion.cantidad = request.POST['cantidad']
                    gestion.total = request.POST['total']
                    gestion.tipo_problema = request.POST['tipo_problema']
                    gestion.tipo_gestion = request.POST['tipo_gestion']
                    gestion.estado = request.POST['estado_valor'].capitalize()
                    gestion.save()

                    prod = Producto.objects.get(pk=gestion.inventario.producto.pk)
                    stock_real = float(gestion.inventario.conversion_stock) * float(gestion.cantidad)
                    if gestion.tipo_gestion == 'True':
                        prod.stock = float(prod.stock) + float(stock_real)
                    else:
                        if (float(stock_real)) > float(prod.stock):
                            raise Exception("Stock insuficiente: "+prod.nombre +' '+ prod.marca.nombre +' '+ gestion.inventario.medida)
                        prod.stock = float(prod.stock) - float(stock_real)
                    prod.save(update_fields=["stock"])
            elif action == 'delete':
                with transaction.atomic():
                    gestion= Gestion_Inventario.objects.get(pk=request.POST['id'])
                    gestion.estado = False
                    prod = Producto.objects.get(pk=gestion.inventario.producto.pk)
                    stock_real = float(gestion.inventario.conversion_stock) * float(gestion.cantidad)
                    if gestion.tipo_gestion:
                        prod.stock = float(prod.stock) - float(stock_real)
                    else:
                        if (float(stock_real)) > float(prod.stock):
                            raise Exception("Stock insuficiente: "+prod.nombre +' '+ prod.marca.nombre +' '+ gestion.inventario.medida)
                        prod.stock = float(prod.stock) + float(stock_real)
                    prod.save(update_fields=["stock"])
                    gestion.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Gestion  Inventario'
        context['list_url'] = reverse_lazy('App_Facturacion:gestion_inventario_list')
        context['entity'] = 'Gestion'
        context['date_now'] = datetime.now
        context['form'] = gestion_inventario_form()
        return context

