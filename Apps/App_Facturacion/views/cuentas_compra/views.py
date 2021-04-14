from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from datetime import datetime
from Apps.App_Facturacion.forms import abonos_compra_form
from Apps.App_Facturacion.models import Cuentas_Compra, Abono_Compra, Empresa
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.db.models.functions import Coalesce
from django.db.models import Sum
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class cuentas_compra_list_view(LoginRequiredMixin, ListView):
    model = Cuentas_Compra
    template_name = 'cuentas_compra/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Cuentas_Compra.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                with transaction.atomic():
                    abono = Abono_Compra()
                    abono.cuentas_compra_id = request.POST['id']
                    abono.valor = request.POST['valor']
                    abono.save()
                    cuenta = Cuentas_Compra.objects.get(id=request.POST['id'])
                    cuenta.saldo = float(cuenta.saldo)-float(abono.valor)
                    if cuenta.saldo == 0:
                        cuenta.estado = True
                    cuenta.save()
            elif action == 'search_abono':
                data = []
                for i in Abono_Compra.objects.filter(cuentas_compra_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'delete_abono':
                with transaction.atomic():
                    abono = Abono_Compra.objects.get(pk=request.POST['id_eliminar_abono'])
                    abono.estado = False
                    abono.save()
                    cuentas_com = Cuentas_Compra.objects.get(pk=abono.cuentas_compra_id)
                    cuentas_com.saldo += abono.valor
                    cuentas_com.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cuentas de Compra'
        context['list_url'] = reverse_lazy('App_Facturacion:cuentas_compra_list')
        context['entity'] = 'Cuentas_Compra'
        context['date_now'] = datetime.now
        context['form'] = abonos_compra_form
        return context

class cuentas_compra_pfd_view(LoginRequiredMixin, View):

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
            template = get_template('cuentas_compra/pdf.html')
            abono_c = Abono_Compra.objects.filter(cuentas_compra=self.kwargs['pk'])
            abono_c = abono_c.filter(estado=True)
            ima = 'logo.png'
            emp = Empresa.objects.get(pk=1)
            if emp.imagen:
                ima = emp.imagen
            context = {
                'compra': Cuentas_Compra.objects.get(pk=self.kwargs['pk']),
                'sub_total': abono_c.aggregate(r=Coalesce(Sum('valor'), 0)).get('r'),
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
        return HttpResponseRedirect(reverse_lazy('App_Facturacion:cuentas_compra_list'))
