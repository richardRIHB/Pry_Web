import json
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView
from xhtml2pdf import pisa
from datetime import datetime
from Apps.App_Facturacion.forms import devolucion_form
from Apps.App_Facturacion.models import Venta, Detalle_Venta, Empresa, Devolucion, Devolucion_Detalle_Venta, Producto
from django.views.generic import View
from django.conf import settings


class devolucion_list_view(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'devolucion/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Devolucion.objects.filter().order_by('-id'):
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in Devolucion_Detalle_Venta.objects.filter(devolucion_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'delete':
                with transaction.atomic():
                    devolucion = Devolucion.objects.get(pk=request.POST['id'])
                    devolucion.estado = False
                    devolucion.save()
                    for i in devolucion.devolucion_detalle_venta_set.all():
                        pro = Producto.objects.get(id=i.inventario.producto.id)
                        pro.stock = float(pro.stock) - (float(i.cantidad) * float(i.inventario.conversion_stock))
                        pro.save(update_fields=["stock"])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Devolucion de Ventas'
        context['create_url'] = reverse_lazy('App_Facturacion:devolucion_create')
        context['list_url'] = reverse_lazy('App_Facturacion:devolucion_list')
        context['entity'] = 'Devolucion'
        context['date_now'] = datetime.now
        return context


class devolucion_create_view(LoginRequiredMixin, CreateView):
    model = Devolucion
    form_class = devolucion_form
    template_name = 'devolucion/create.html'
    success_url = reverse_lazy('App_Facturacion:devolucion_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_venta':
                data = []
                item = ''
                prod = []
                if request.POST['term'].isdigit() == True:
                    if Venta.objects.filter(pk=request.POST['term']).exists():
                        vent = Venta.objects.filter(pk=request.POST['term'])[0:10]
                        for i in vent:
                            item = i.toJSON()
                            item['text'] = i.id
                            for a in Detalle_Venta.objects.filter(venta_id=i.id):
                                pro = a.inventario.toJSON()
                                pro['cantidad'] = a.cantidad
                                pro['precio'] = format(a.precio, '.2f')
                                pro['descuento'] = format(a.descuento, '.2f')
                                pro['estado_devolucion'] = False
                                pro['cantidad_inicial'] = "0"
                                pro['subtotal'] = "0.00"
                                prod.append(pro)
                        item['produc'] = prod
                        data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    devolucion = Devolucion()
                    devolucion.venta_id = vents['venta']
                    devolucion.iva = float(vents['iva'])
                    devolucion.subtotal = float(vents['subtotal'])
                    devolucion.total = float(vents['total'])
                    devolucion.save()
                    vent = Venta.objects.get(pk=vents['venta'])
                    vent.estado_devolucion = True
                    vent.save()
                    for i in vents['products']:
                        det = Devolucion_Detalle_Venta()
                        if int(i['cantidad_inicial']) > 0:
                            det.devolucion_id = devolucion.id
                            det.inventario_id = i['id']
                            det.cantidad = int(i['cantidad_inicial'])
                            det.descuento = float(i['descuento'])
                            det.precio = float(i['precio'])
                            det.subtotal = float(i['subtotal'])
                            det.save()
                            pro = i['producto']
                            pro = Producto.objects.get(id=pro['id'])
                            pro.stock = float(pro.stock) + (float(i['conversion_stock']) * det.cantidad)
                            pro.save(update_fields=["stock"])
                    data = {'id': devolucion.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Devolución de Venta'
        context['entity'] = 'Devolucion'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        return context


class devolucion_factura_view(View):
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
            template = get_template('devolucion/factura.html')
            ima = 'logo.png'
            emp = Empresa.objects.get(pk=1)
            if emp.imagen:
                ima = emp.imagen
            context = {
                'venta': Devolucion.objects.get(pk=self.kwargs['pk']),
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
        return HttpResponseRedirect(reverse_lazy('App_Facturacion:devolucion_list'))
