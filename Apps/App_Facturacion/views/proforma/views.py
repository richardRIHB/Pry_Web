import json
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView
from xhtml2pdf import pisa
from datetime import datetime
from Apps.App_Facturacion.forms import venta_form
from Apps.App_Facturacion.models import Venta, Detalle_Venta, Cliente, Empresa, Inventario
from django.views.generic import View
from django.conf import settings


class proforma_list_view(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'proforma/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Venta.objects.filter(tipo_documento=True).order_by('-id'):
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in Detalle_Venta.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proforma de Ventas'
        context['create_url'] = reverse_lazy('App_Facturacion:proforma_create')
        context['list_url'] = reverse_lazy('App_Facturacion:proforma_list')
        context['entity'] = 'Proforma'
        context['date_now'] = datetime.now
        return context

class proforma_create_view(LoginRequiredMixin, CreateView):
    model = Venta
    form_class = venta_form
    template_name = 'proforma/create.html'
    success_url = reverse_lazy('App_Facturacion:proforma_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                list_invt = Inventario.objects.filter(Q(producto__nombre__icontains=request.POST['term'])|Q(producto__descripcion__icontains=request.POST['term'])|Q(producto__marca__nombre__icontains=request.POST['term']))[0:10]
                for i in list_invt:
                    item = i.toJSON()
                    item['value'] = i.producto.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    venta = Venta()
                    venta.cliente_id = vents['cliente']
                    venta.subtotal = float(vents['subtotal'])
                    venta.iva = float(vents['iva'])
                    venta.total = float(vents['total'])
                    venta.tipo_documento = bool(vents['tipo_documento'])
                    venta.iva_base = float(request.POST['iva_base'])
                    venta.save()
                    for i in vents['products']:
                        det = Detalle_Venta()
                        det.venta_id = venta.id
                        det.inventario_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['pvp_medida'])
                        det.total = float(i['subtotal'])
                        det.descuento = float(i['descuento'])
                        det.save()
                    data = {'id': venta.id}
            elif action == 'search_clientes':
                data = []
                list_cli = Cliente.objects.filter(
                    Q(nombre__icontains=request.POST['term']) | Q(apellido__icontains=request.POST['term']) | Q(
                        c_i__icontains=request.POST['term']))[0:10]
                for i in list_cli:
                    cli = i.toJSON()
                    cli['text'] = i.get_full_name()
                    data.append(cli)
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
        context['title'] = 'Creación de una Proforma'
        context['entity'] = 'Proforma'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['iva'] = self.get_iva_empresa()
        context['det'] = []
        return context

class proforma_update_view(LoginRequiredMixin, UpdateView):
    model = Venta
    form_class = venta_form
    template_name = 'proforma/create.html'
    success_url = reverse_lazy('App_Facturacion:proforma_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                list_invt = Inventario.objects.filter(Q(producto__nombre__icontains=request.POST['term'])|Q(producto__descripcion__icontains=request.POST['term'])|Q(producto__marca__nombre__icontains=request.POST['term']))[0:10]
                for i in list_invt:
                    item = i.toJSON()
                    item['value'] = i.producto.nombre
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    venta = self.get_object()
                    venta.cliente_id = vents['cliente']
                    venta.subtotal = float(vents['subtotal'])
                    venta.iva = float(vents['iva'])
                    venta.total = float(vents['total'])
                    venta.tipo_documento = bool(vents['tipo_documento'])
                    venta.iva_base = float(request.POST['iva_base'])
                    venta.fecha = datetime.now()
                    venta.save()

                    venta.detalle_venta_set.all().delete()

                    for i in vents['products']:
                        det = Detalle_Venta()
                        det.venta_id = venta.id
                        det.inventario_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['pvp_medida'])
                        det.total = float(i['subtotal'])
                        det.descuento = float(i['descuento'])
                        det.save()
                    data = {'id': venta.id}
            elif action == 'search_clientes':
                data = []
                list_cli = Cliente.objects.filter(
                    Q(nombre__icontains=request.POST['term']) | Q(apellido__icontains=request.POST['term']) | Q(
                        c_i__icontains=request.POST['term']))[0:10]
                for i in list_cli:
                    cli = i.toJSON()
                    cli['text'] = i.get_full_name()
                    data.append(cli)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in Detalle_Venta.objects.filter(venta_id=self.get_object().id):
                item = i.inventario.toJSON()
                prod_stock = int(i.inventario.producto.stock)
                invetario_stock = int(prod_stock / i.inventario.conversion_stock)
                if i.cantidad <= invetario_stock:
                    item['cantidad'] = i.cantidad
                else:
                    item['cantidad'] = invetario_stock
                item['descuento'] = format(i.descuento, '.2f')
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
        context['title'] = 'Edición de una Proforma'
        context['entity'] = 'Proforma'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['iva'] = self.get_iva_empresa()
        context['det'] = json.dumps(self.get_details_product())
        return context

class proforma_factura_view(View):
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
            template = get_template('proforma/factura.html')
            ima = 'logo.png'
            emp = Empresa.objects.get(pk=1)
            if emp.imagen:
                ima = emp.imagen
            context = {
                'venta': Venta.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': emp.nombre, 'ruc': emp.ruc, 'correo': emp.correo,
                         'address': emp.ciudad, 'ubicacion': emp.direccion, 'telefono': emp.telefono},
                'icon': '{}{}'.format(settings.MEDIA_URL, ima)
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('App_Facturacion:proforma_list'))

