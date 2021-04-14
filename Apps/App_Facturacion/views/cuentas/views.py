from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.utils import timezone
from datetime import datetime

from django.template.loader import get_template

from Apps.App_Facturacion.forms import abonos_form
from Apps.App_Facturacion.models import Cuentas, Abono, Empresa
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from xhtml2pdf import pisa
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import os


class cuentas_list_view(ListView):
    model = Cuentas
    template_name = 'cuentas/list.html'

    # def get_queryset(self):

    # return Cliente.objects.all()
    # return Cliente.objects.filter(nombre__startswith='p')
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
                for i in Cuentas.objects.all().order_by(Coalesce('venta','valor').desc()):
                    data.append(i.toJSON())
            elif action == 'add':
                abono = Abono()
                abono.valor = request.POST['valor']
                abono.cuentas_id = request.POST['cuentas']
                abono.fecha = datetime.now()
                abono.save()
                cuenta = Cuentas.objects.get(id=request.POST['cuentas'])
                cuenta.saldo = float(cuenta.saldo) - float(abono.valor)
                if cuenta.saldo == 0:
                    cuenta.estado = True
                cuenta.save()

            elif action == 'search_abono':
                data = []
                for i in Abono.objects.filter(cuentas_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'anular_abono':
                abono = Abono.objects.get(pk=request.POST['id_abono'])
                abono.estado = False
                abono.save()
                cuentas = Cuentas.objects.get(pk=abono.cuentas_id)
                cuentas.saldo += abono.valor
                cuentas.estado = False
                cuentas.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cuentas Pendientes'
        context['create_url'] = reverse_lazy('App_Facturacion:cliente_create')
        context['list_url'] = reverse_lazy('App_Facturacion:cuentas_list')
        context['entity'] = 'Cuentas'
        context['form'] = abonos_form
        context['date_now'] = datetime.now
        return context


class cuentas_recibo_view(View):
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
            template = get_template('cuentas/recibo.html')
            cuentas=Cuentas.objects.get(pk=self.kwargs['pk'])
            abonos_list = cuentas.abono_set.filter(estado=True).order_by('fecha')
            total_abonado=cuentas.abono_set.filter(estado=True).aggregate(Sum('valor'))
            ima = 'logo.png'
            emp = Empresa.objects.get(pk=1)

            if emp.imagen:
                ima = emp.imagen
            context = {
                'cuenta': Cuentas.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': emp.nombre, 'ruc': emp.ruc, 'correo': emp.correo,
                         'address': emp.ciudad, 'ubicacion': emp.direccion, 'telefono': emp.telefono},
                'icon': '{}{}'.format(settings.MEDIA_URL, ima),
                'total_abonado': total_abonado,
                'abonos_list' : abonos_list,

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
        return HttpResponseRedirect(reverse_lazy('App_Facturacion:cuentas_list'))
