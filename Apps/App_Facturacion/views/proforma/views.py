import json
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from reportlab.lib import colors
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import cm
from reportlab.platypus import TableStyle, Table
from xhtml2pdf import pisa

from Apps.App_Facturacion.forms import venta_form
from Apps.App_Facturacion.models import Venta, Producto, Detalle_Venta, Cliente
from reportlab.pdfgen import canvas
from django.views.generic import View
from django.conf import settings
from io import BytesIO


class proforma_list_view(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'proforma/list.html'

    # permission_required = 'erp.view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Venta.objects.filter(tipo_documento=True).order_by(Coalesce('id', 'cliente').desc()):
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
        context['title'] = 'Listado de Proformas'
        context['create_url'] = reverse_lazy('App_Facturacion:proforma_create')
        context['list_url'] = reverse_lazy('App_Facturacion:proforma_list')
        context['entity'] = 'Proforma'
        return context

class proforma_create_view(LoginRequiredMixin, CreateView):
    model = Venta
    form_class = venta_form
    template_name = 'proforma/create.html'
    success_url = reverse_lazy('App_Facturacion:proforma_list')
    # permission_required = 'erp.add_sale'
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
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    venta = Venta()
                    venta.fecha = vents['fecha']
                    venta.cliente_id = vents['cliente']
                    venta.subtotal = float(vents['subtotal'])
                    venta.iva = float(vents['iva'])
                    venta.total = float(vents['total'])
                    venta.tipo_documento = bool(vents['tipo_documento'])
                    venta.save()
                    for i in vents['products']:
                        det = Detalle_Venta()
                        det.venta_id = venta.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precio'])
                        det.total = float(i['subtotal'])
                        det.save()

                    data = {'id': venta.id}
            elif action == 'search_clientes':
                data = []
                list_cli = Cliente.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in list_cli:
                    cli = i.toJSON()
                    data.append(cli)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Proforma'
        context['entity'] = 'Proforma'
        context['list_url'] = self.success_url
        context['action'] = 'add'
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
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    # venta = Sale.objects.get(pk=self.get_object().id)
                    venta = self.get_object()
                    venta.fecha = vents['fecha']
                    venta.cliente_id = vents['cliente']
                    venta.subtotal = float(vents['subtotal'])
                    venta.iva = float(vents['iva'])
                    venta.total = float(vents['total'])
                    venta.tipo_documento = bool(vents['tipo_documento'])
                    venta.save()

                    venta.detalle_venta_set.all().delete()

                    for i in vents['products']:
                        det = Detalle_Venta()
                        det.venta_id = venta.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['precio'])
                        det.total = float(i['subtotal'])
                        det.save()

                    data = {'id': venta.id}
            elif action == 'search_clientes':
                data = []
                list_cli = Cliente.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in list_cli:
                    cli = i.toJSON()
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
                item = i.producto.toJSON()
                item['cantidad'] = i.cantidad
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Proforma'
        context['entity'] = 'Proforma'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product())
        return context

class proforma_factura_view(View):
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
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
            context = {
                'venta': Venta.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'ALGORISOFT S.A.', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('App_Facturacion:proforma_list'))

