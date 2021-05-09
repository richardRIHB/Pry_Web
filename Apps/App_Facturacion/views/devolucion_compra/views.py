import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, View

from Apps.App_Facturacion.forms import devolucion_compra_form
from Apps.App_Facturacion.models import Compra, Producto, Detalle_Compra, Devolucion_Compra, Devolucion_Detalle_Compra, \
    Empresa, Inventario
from datetime import datetime

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class devolucion_compra_list_view(LoginRequiredMixin, TemplateView):
    template_name = 'devolucion_compra/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Devolucion_Compra.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_detalle_producto':
                data = []
                for i in Devolucion_Detalle_Compra.objects.filter(devolucion_compra_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'delete':
                with transaction.atomic():
                    devolu_comp = Devolucion_Compra.objects.get(pk=request.POST['id'])
                    comp = Compra.objects.get(pk=devolu_comp.compra.pk)
                    comp.subtotal = float(comp.subtotal) + float(devolu_comp.subtotal)
                    comp.iva = float(comp.iva) + float(devolu_comp.iva)
                    comp.total = float(comp.total) + float(devolu_comp.total)
                    comp.save()
                    for i in devolu_comp.devolucion_detalle_compra_set.all():
                        prod = Producto.objects.get(pk=i.producto.id)
                        precio_base_actual = float(prod.stock) * float(prod.precio_bruto)
                        precio_base_compra = i.cantidad * float(i.precio)
                        precio_base_acumulado = precio_base_actual + precio_base_compra
                        stock_acumulado = float(prod.stock) + i.cantidad
                        precio_actualizado = precio_base_acumulado / stock_acumulado
                        prod.precio_bruto = precio_actualizado
                        prod.stock += i.cantidad
                        calculo_iva = float(prod.precio_bruto) * (float(prod.iva) + 1)
                        calculo_ganancia = calculo_iva * ((float(prod.porcentaje_ganancia) / 100) + 1)
                        prod.precio = calculo_ganancia
                        prod.save()

                        for a in Inventario.objects.filter(producto_id=prod.pk):
                            inv = Inventario.objects.get(pk=a.id)
                            if inv.tipo_conversion == True:
                                pvp_medida = float(inv.producto.precio) * float(inv.equivalencia)
                                pvp_medida = pvp_medida - (
                                        (float(inv.porcentaje_conversion) / 100) * pvp_medida)
                                inv.pvp_medida = pvp_medida
                            else:
                                pvp_medida = float(inv.producto.precio) / float(inv.equivalencia)
                                pvp_medida = ((float(inv.porcentaje_conversion) / 100) + 1) * pvp_medida
                                inv.pvp_medida = pvp_medida
                            inv.save()

                        detalle_com = Detalle_Compra.objects.get(Q(compra_id=comp.pk) & Q(producto_id=i.producto.id))
                        detalle_com.cantidad += i.cantidad
                        detalle_com.subtotal = detalle_com.cantidad * float(detalle_com.precio)
                        detalle_com.save()
                    devolu_comp.estado = False
                    devolu_comp.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['title'] = 'Listado de Devolución de Compras'
        context['list_url'] = reverse_lazy('App_Facturacion:devolucion_compra_list')
        context['create_url'] = reverse_lazy('App_Facturacion:devolucion_compra_create')
        context['entity'] = 'DevolucionCompras'
        context['date_now'] = datetime.now
        return context

class devolucion_compra_create_view(LoginRequiredMixin, CreateView):
    model = Devolucion_Compra
    form_class = devolucion_compra_form
    template_name = 'devolucion_compra/create.html'
    success_url = reverse_lazy('App_Facturacion:devolucion_compra_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_compra':
                data = []
                item = ''
                prod = []
                if request.POST['term'].isdigit() == True:
                    if Compra.objects.filter(pk=request.POST['term']).exists():
                        comp = Compra.objects.filter(pk=request.POST['term'])[0:10]
                        for i in comp:
                            item = i.toJSON()
                            item['text'] = i.id
                            for a in Detalle_Compra.objects.filter(compra_id=i.id):
                                pro = a.producto.toJSON()
                                pro['cantidad'] = a.cantidad
                                pro['precio_new'] = format(a.precio, '.3f')
                                pro['precio_antiguo'] = format(a.precio_antiguo, '.2f')
                                pro['estado_devolucion'] = False
                                pro['cantidad_inicial'] = "0"
                                pro['subtotal'] = "0.00"
                                prod.append(pro)
                        item['produc'] = prod
                        data.append(item)
            elif action == 'add':
                compra_diccionario = json.loads(request.POST['compra_diccionario'])
                contador = 0
                for i in compra_diccionario['productos']:
                    if int(i['cantidad_inicial']) > 0:
                        prod = Producto.objects.get(pk=i['id'])
                        if i['cantidad_inicial'] > prod.stock:
                            contador = 1
                if contador == 0:
                    with transaction.atomic():
                        devolucion_c = Devolucion_Compra()
                        devolucion_c.compra_id = compra_diccionario['compra']
                        devolucion_c.subtotal = compra_diccionario['subtotal']
                        devolucion_c.iva = compra_diccionario['iva']
                        devolucion_c.total = compra_diccionario['total']
                        devolucion_c.save()
                        comp = Compra.objects.get(pk=compra_diccionario['compra'])
                        comp.subtotal = float(comp.subtotal) - float(compra_diccionario['subtotal'])
                        comp.iva = float(comp.iva) - float(compra_diccionario['iva'])
                        comp.total = float(comp.total) - float(compra_diccionario['total'])
                        comp.estado_devolucion_c = True
                        comp.save()
                        comp.detalle_compra_set.all().delete()
                        for i in compra_diccionario['productos']:
                            devolucion_dc = Devolucion_Detalle_Compra()
                            if int(i['cantidad_inicial']) > 0:
                                devolucion_dc.devolucion_compra_id = devolucion_c.id
                                devolucion_dc.producto_id = i['id']
                                devolucion_dc.precio = float(i['precio_new'])
                                devolucion_dc.cantidad = i['cantidad_inicial']
                                devolucion_dc.subtotal = float(i['subtotal'])
                                devolucion_dc.save()

                                prod = Producto.objects.get(pk=i['id'])
                                precio_base_actual = float(prod.stock) * float(prod.precio_bruto)
                                precio_base_compra = i['cantidad_inicial'] * float(i['precio_new'])
                                precio_base_acumulado = precio_base_actual - precio_base_compra
                                stock_acumulado = float(prod.stock) - i['cantidad_inicial']
                                precio_actualizado = precio_base_acumulado / stock_acumulado
                                prod.precio_bruto = precio_actualizado
                                prod.stock -= i['cantidad_inicial']
                                calculo_iva = float(prod.precio_bruto) * (float(prod.iva) + 1)
                                calculo_ganancia = calculo_iva * ((float(prod.porcentaje_ganancia)/100) + 1)
                                prod.precio = calculo_ganancia
                                prod.save()

                                for a in Inventario.objects.filter(producto_id=prod.pk):
                                    inv = Inventario.objects.get(pk=a.id)
                                    if inv.tipo_conversion == True:
                                        pvp_medida = float(inv.producto.precio) * float(inv.equivalencia)
                                        pvp_medida = pvp_medida - (
                                                    (float(inv.porcentaje_conversion) / 100) * pvp_medida)
                                        inv.pvp_medida = pvp_medida
                                    else:
                                        pvp_medida = float(inv.producto.precio) / float(inv.equivalencia)
                                        pvp_medida = ((float(inv.porcentaje_conversion) / 100) + 1) * pvp_medida
                                        inv.pvp_medida = pvp_medida
                                    inv.save()
                            detalle = Detalle_Compra()
                            detalle.compra_id = comp.id
                            detalle.producto_id = i['id']
                            detalle.cantidad = i['cantidad'] - int(i['cantidad_inicial'])
                            detalle.precio = float(i['precio_new'])
                            detalle.subtotal = detalle.cantidad * float(detalle.precio)
                            detalle.save()
                        data = {'id': devolucion_c.id}
                else:
                    data['error'] = 'La cantidad de productos es inferior al stock actual'
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Devolución de Compra'
        context['entity'] = 'Devolución Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['detalle_pro'] = []
        return context

class devolucion_compra_pdf_view(LoginRequiredMixin, View):

    def link_callback(self, uri, rel):

        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('devolucion_compra/pdf.html')
            ima = 'logo.png'
            emp = Empresa.objects.get(pk=1)
            if emp.imagen:
                ima = emp.imagen
            context = {
                'devolucion_compra': Devolucion_Compra.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': emp.nombre, 'ruc': emp.ruc, 'correo': emp.correo,
                         'address': emp.ciudad, 'ubicacion': emp.direccion, 'telefono': emp.telefono},
                'icon': '{}{}'.format(settings.MEDIA_URL, ima)
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('App_Facturacion:devolucion_compra_list'))

