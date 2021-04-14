from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from Apps.App_Facturacion.forms import producto_form
from Apps.App_Facturacion.models import Producto, Galeria, Marca, Seccion, Bloque, Posicion, Empresa, Inventario
from django.views.generic import DetailView, TemplateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from datetime import datetime

class producto_view(LoginRequiredMixin, TemplateView):
    template_name = 'producto/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Producto.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_marca':
                data = []
                mar = Marca.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in mar:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'search_bloque':
                data = []
                mar = Bloque.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in mar:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'search_seccion':
                data = []
                mar = Seccion.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in mar:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'search_posicion':
                data = []
                mar = Posicion.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in mar:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    prod = Producto()
                    prod.nombre = request.POST['nombre']
                    prod.descripcion = request.POST['descripcion']
                    prod.precio = request.POST['precio']
                    prod.marca_id = request.POST['marca']
                    prod.bloque_id = request.POST['bloque']
                    prod.seccion_id = request.POST['seccion']
                    prod.posicion_id = request.POST['posicion']
                    prod.stock = request.POST['stock']
                    prod.stock_minimo = request.POST['stock_minimo']
                    prod.iva = request.POST['iva']
                    prod.porcentaje_ganancia = request.POST['porcentaje_ganancia']
                    prod.precio_bruto = request.POST['precio_bruto']
                    if request.FILES:
                        prod.imagen = request.FILES['imagen']
                    else:
                        prod.imagen = ""
                    estad = request.POST['estado_valor']
                    prod.estado = estad.capitalize()
                    prod.save()
            elif action == 'edit':
                with transaction.atomic():
                    prod = Producto.objects.get(pk=request.POST['id'])
                    prod.nombre = request.POST['nombre']
                    prod.descripcion = request.POST['descripcion']
                    prod.precio = request.POST['precio']
                    prod.marca_id = request.POST['marca']
                    prod.bloque_id = request.POST['bloque']
                    prod.seccion_id = request.POST['seccion']
                    prod.posicion_id = request.POST['posicion']
                    prod.stock = request.POST['stock']
                    prod.stock_minimo = request.POST['stock_minimo']
                    prod.iva = request.POST['iva']
                    prod.porcentaje_ganancia = request.POST['porcentaje_ganancia']
                    prod.precio_bruto = request.POST['precio_bruto']
                    if request.FILES:
                        prod.imagen = request.FILES['imagen']
                    estad = request.POST['estado_valor']
                    prod.estado = estad.capitalize()
                    prod.save()
                    for a in Inventario.objects.filter(producto_id=prod.pk):
                        inv = Inventario.objects.get(pk=a.id)
                        if inv.tipo_conversion == True:
                            pvp_medida = float(inv.producto.precio) * float(inv.equivalencia)
                            pvp_medida = pvp_medida - ((float(inv.porcentaje_conversion) / 100) * pvp_medida)
                            inv.pvp_medida = pvp_medida
                        else:
                            pvp_medida = float(inv.producto.precio) / float(inv.equivalencia)
                            pvp_medida = ((float(inv.porcentaje_conversion) / 100) + 1) * pvp_medida
                            inv.pvp_medida = pvp_medida
                        inv.save()
            elif action == 'delete':
                with transaction.atomic():
                    prod = Producto.objects.get(pk=request.POST['id'])
                    prod.estado = False
                    prod.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_iva_empresa(self):
        data = ''
        try:
            emp = Empresa.objects.get(pk=1)
            data = emp.iva
        except:
            data = '0'
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['list_url'] = reverse_lazy('App_Facturacion:producto_list')
        context['list_inventario_url'] = reverse_lazy('App_Facturacion:inventario_list')
        context['entity'] = 'Productos'
        context['count_marca'] = Marca.objects.filter(estado='True').count()
        context['count_ubicacion'] = Bloque.objects.count() + Seccion.objects.count() + Posicion.objects.count()
        context['count_galeria'] = Galeria.objects.count()
        context['iva_base'] = self.get_iva_empresa()
        context['date_now'] = datetime.now
        context['form'] = producto_form()
        return context

class producto_show_view(DetailView):
    model = Producto
    template_name = 'producto/show.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        galeria_list = []
        gale = Galeria.objects.filter(producto=self.object.id)
        gale = gale.filter(estado='True')
        for i in gale:
            galeria_list.append(i.toJSON())
        context['galeria'] = galeria_list
        context['title'] = 'Información'
        context['entity'] = 'Producto'
        context['date_now'] = datetime.now
        context['count_marca'] = Marca.objects.filter(estado='True').count()
        context['count_ubicacion'] = Bloque.objects.count() + Seccion.objects.count() + Posicion.objects.count()
        context['count_galeria'] = Galeria.objects.count()
        return context
