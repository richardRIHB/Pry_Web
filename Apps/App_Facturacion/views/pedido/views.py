from Apps.App_Facturacion.models import Producto, Pedido, Detalle_Venta, Venta, Empresa, Cuentas
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.conf import settings
from datetime import datetime
from xhtml2pdf import pisa
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
import os

class pedido_list_view(ListView):
    model = Pedido
    template_name = 'pedido/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Pedido.objects.all():
                    data.append(i.toJSON())
            elif action == 'anular':
                pedido = Pedido.objects.get(id=request.POST['id'])
                pedido.estado = False
                pedido.save(update_fields=["estado"])
            elif action == 'confirmar':
                pedido = Pedido.objects.get(id=request.POST['id'])
                pedido.estado_entrega = True
                pedido.save(update_fields=["estado_entrega"])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Pedidos'
        context['create_url'] = reverse_lazy('App_Facturacion:pedido_list')
        context['list_url'] = reverse_lazy('App_Facturacion:pedido_list')
        context['entity'] = 'Pedidos'
        context['date_now'] = datetime.now
        return context

class pedido_recibo_view(View):
    def link_callback(self, uri, rel):
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
            template = get_template('pedido/recibo.html')
            pedido=Pedido.objects.get(pk=self.kwargs['pk'])
            detalle_list = Detalle_Venta.objects.filter(venta_id=pedido.venta_id)
            venta = Venta.objects.get(pk=pedido.venta_id)
            estado = 'CANCELADO'
            ima = 'logo.png'
            emp = Empresa.objects.get(pk=1)
            if emp.imagen:
                ima = emp.imagen
            if venta.metodo_pago:
                cuent = Cuentas.objects.get(venta_id=venta.id)
                if cuent.estado:
                    estado = 'CANCELADO'
                else:
                    estado = 'POR COBRA'
            estado_pedido = 'PENDIENTE'
            if pedido.estado_entrega:
                estado_pedido = 'ENTREGADO'
            context = {
                'pedido': pedido,
                'estado': estado,
                'estado_pedido': estado_pedido,
                'comp': {'name': emp.nombre, 'ruc': emp.ruc, 'correo': emp.correo,
                         'address': emp.ciudad, 'ubicacion': emp.direccion, 'telefono': emp.telefono},
                'icon': '{}{}'.format(settings.MEDIA_URL, ima),
                'venta': venta,
                'detalle_list': detalle_list,
                'total': venta.total + pedido.total,
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
        return HttpResponseRedirect(reverse_lazy('App_Facturacion:pedido_list'))
