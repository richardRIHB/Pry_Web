import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, UpdateView, View
from django.db.models import Q

from Apps.App_Facturacion.forms import compra_form
from Apps.App_Facturacion.models import Compra, Producto, Detalle_Compra, Proveedor, Empresa
from datetime import datetime

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class proforma_compra_list_view(LoginRequiredMixin, TemplateView):
    template_name = 'proforma_compra/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Compra.objects.filter(tipo_documento=True):
                    data.append(i.toJSON())
            elif action == 'search_detalle_producto':
                data = []
                for i in Detalle_Compra.objects.filter(compra_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proforma de Compras'
        context['list_url'] = reverse_lazy('App_Facturacion:proforma_compra_list')
        context['create_url'] = reverse_lazy('App_Facturacion:proforma_compra_create')
        context['entity'] = 'Compras'
        context['date_now'] = datetime.now
        return context

class proforma_compra_create_view(LoginRequiredMixin, CreateView):
    model = Compra
    form_class = compra_form
    template_name = 'proforma_compra/create.html'
    success_url = reverse_lazy('App_Facturacion:proforma_compra_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_productos':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                prods = Producto.objects.filter(Q(nombre__icontains=request.POST['term']) | Q(descripcion__icontains=request.POST['term']) | Q(marca__nombre__icontains=request.POST['term']))
                for i in prods.exclude(pk__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'search_proveedor':
                data = []
                prove = Proveedor.objects.filter(Q(nombre__icontains=request.POST['term']) | Q(apellido__icontains=request.POST['term']) | Q(empresa__icontains=request.POST['term']))[0:10]
                for i in prove:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    compra_diccionario = json.loads(request.POST['compra_diccionario'])
                    comp = Compra()
                    comp.proveedor_id = compra_diccionario['proveedor']
                    fecha_entrega = datetime.strptime(compra_diccionario['fecha'], '%d-%m-%Y')
                    comp.fecha = datetime.strftime(fecha_entrega, '%Y-%m-%d')
                    comp.subtotal = compra_diccionario['subtotal']
                    comp.iva_base = compra_diccionario['iva_base']
                    comp.iva = compra_diccionario['iva']
                    comp.total = compra_diccionario['total']
                    comp.tipo_documento = True
                    comp.save()
                    for i in compra_diccionario['productos']:
                        detalle = Detalle_Compra()
                        detalle.compra_id = comp.id
                        detalle.producto_id = i['id']
                        detalle.cantidad = i['cantidad']
                        detalle.precio = float(i['precio_bruto'])
                        detalle.subtotal = float(i['subtotal'])
                        detalle.save()
                    data = {'id': comp.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
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
        context['title'] = 'Creación de una Proforma de Compra'
        context['entity'] = 'Proforma'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['detalle_pro'] = []
        context['iva_base'] = self.get_iva_empresa()
        return context

class proforma_compra_update_view(LoginRequiredMixin, UpdateView):
    model = Compra
    form_class = compra_form
    template_name = 'proforma_compra/create.html'
    success_url = reverse_lazy('App_Facturacion:proforma_compra_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_productos':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                prods = Producto.objects.filter(Q(nombre__icontains=request.POST['term']) | Q(descripcion__icontains=request.POST['term']) | Q(marca__nombre__icontains=request.POST['term']))
                for i in prods.exclude(pk__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'search_proveedor':
                data = []
                prove = Proveedor.objects.filter(Q(nombre__icontains=request.POST['term']) | Q(apellido__icontains=request.POST['term']) | Q(empresa__icontains=request.POST['term']))[0:10]
                for i in prove:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    compra_diccionario = json.loads(request.POST['compra_diccionario'])
                    comp = Compra.objects.get(pk=self.get_object().id)
                    comp.proveedor_id = compra_diccionario['proveedor']
                    fecha_entrega = datetime.strptime(compra_diccionario['fecha'], '%d-%m-%Y')
                    comp.fecha = datetime.strftime(fecha_entrega, '%Y-%m-%d')
                    comp.subtotal = compra_diccionario['subtotal']
                    comp.iva_base = compra_diccionario['iva_base']
                    comp.iva = compra_diccionario['iva']
                    comp.total = compra_diccionario['total']
                    comp.save()
                    # Eliminamos el detalle anterior para poder actulaizar
                    comp.detalle_compra_set.all().delete()
                    for i in compra_diccionario['productos']:
                        detalle = Detalle_Compra()
                        detalle.compra_id = comp.id
                        detalle.producto_id = i['id']
                        detalle.cantidad = i['cantidad']
                        detalle.precio = float(i['precio_bruto'])
                        detalle.subtotal = float(i['subtotal'])
                        detalle.save()
                    data = {'id': comp.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_detalle_productos(self):
        data = []
        try:
            for i in Detalle_Compra.objects.filter(compra_id=self.get_object().id):
                item = i.producto.toJSON()
                item['cantidad'] = i.cantidad
                data.append(item)
        except:
            pass
        return data

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
        context['title'] = 'Edicion de una Proforma de Compra'
        context['entity'] = 'Proforma'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['detalle_pro'] = json.dumps(self.get_detalle_productos())
        context['iva_base'] = self.get_iva_empresa()
        return context

class proforma_compra_pdf_view(LoginRequiredMixin, View):

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
            template = get_template('proforma_compra/pdf.html')
            ima = 'logo.png'
            emp = Empresa.objects.get(pk=1)
            if emp.imagen:
                ima = emp.imagen
            context = {
                'compra': Compra.objects.get(pk=self.kwargs['pk']),
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
        return HttpResponseRedirect(reverse_lazy('App_Facturacion:proforma_compra_list'))
