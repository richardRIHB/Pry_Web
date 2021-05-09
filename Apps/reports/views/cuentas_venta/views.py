from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.db.models import Q
from Apps.App_Facturacion.models import Cuentas, Cliente, Empresa
from Apps.reports.forms import report_cuentas_venta_form

from django.db.models.functions import Coalesce
from django.db.models import Sum
from datetime import datetime

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class report_cuentas_venta_view(LoginRequiredMixin, TemplateView):
    template_name = 'cuentas_venta/report.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                fil = request.POST.get('filtro', '')
                clien = request.POST.get('clien', '')
                search = ''
                if fil and clien == '':
                    search = Cuentas.objects.all()
                    search = search.filter(estado_venta=True)
                    if fil == 'valores_pendientes':
                        search = search.filter(estado=False)
                    elif fil == 'pagado':
                        search = search.filter(estado=True)
                    for s in search:
                        data.append([
                            s.venta.pk,
                            s.venta.cliente.nombre + ' ' + s.venta.cliente.apellido,
                            s.fecha.strftime('%d-%m-%Y'),
                            format(s.valor, '.2f'),
                            format(s.saldo, '.2f'),
                        ])
                elif fil and clien:
                    search = Cuentas.objects.filter(venta__cliente_id=clien)
                    search = search.filter(estado_venta=True)
                    if fil == 'valores_pendientes':
                        search = search.filter(estado=False)
                    elif fil == 'pagado':
                        search = search.filter(estado=True)
                    for s in search:
                        data.append([
                            s.venta.pk,
                            s.venta.cliente.nombre + ' ' + s.venta.cliente.apellido,
                            s.fecha.strftime('%d-%m-%Y'),
                            format(s.valor, '.2f'),
                            format(s.saldo, '.2f'),
                        ])
                total_valor = search.aggregate(r=Coalesce(Sum('valor'), 0)).get('r')
                total_saldo = search.aggregate(r=Coalesce(Sum('saldo'), 0)).get('r')
                data.append([
                    '---',
                    '---',
                    '---',
                    format(total_valor, '.2f'),
                    format(total_saldo, '.2f'),
                ])
            elif action == 'search_cliente':
                data = []
                cli = Cliente.objects.filter(Q(nombre__icontains=request.POST['term']) | Q(apellido__icontains=request.POST['term']) | Q(c_i__icontains=request.POST['term']))[0:10]
                for i in cli:
                    item = i.toJSON()
                    item['text'] = i.nombre + ' ' + i.apellido
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Cuentas de Venta'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('reports:cuentas_venta_report')
        context['form'] = report_cuentas_venta_form()
        return context

class reporte_cuentas_venta_pdf_view(LoginRequiredMixin, View):

    def link_callback(self, uri, rel):
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('cuentas_venta/pdf_repor.html')
            fil = self.kwargs['filtro']
            clien = self.kwargs['pk']
            fitro_text = 'Reporte de Todas las Cuentas de Venta'
            cliente = []
            data = []
            search = ''
            if fil and clien == 'null':
                search = Cuentas.objects.all()
                search = search.filter(estado_venta=True)
                if fil == 'valores_pendientes':
                    search = search.filter(estado=False)
                    fitro_text = 'Reporte de Cuentas de Venta con Valores Pendientes'
                elif fil == 'pagado':
                    search = search.filter(estado=True)
                    fitro_text = 'Reporte de Cuentas de Venta con Valores Cancelados'
                for s in search:
                    data.append([
                        s.venta.pk,
                        s.venta.cliente.nombre + ' ' + s.venta.cliente.apellido,
                        s.fecha.strftime('%d-%m-%Y'),
                        format(s.valor, '.2f'),
                        format(s.saldo, '.2f'),
                    ])
                cliente = {'cliente': '------------------', 'reporte': fitro_text, 'cedula': '------------------', 'fecha': datetime.now}
            elif fil and clien != 'null':
                search = Cuentas.objects.filter(venta__cliente_id=clien)
                search = search.filter(estado_venta=True)
                if fil == 'valores_pendientes':
                    search = search.filter(estado=False)
                    fitro_text = 'Reporte de Cuentas de Venta con Valores Pendientes'
                elif fil == 'pagado':
                    search = search.filter(estado=True)
                    fitro_text = 'Reporte de Cuentas de Venta con Valores Cancelados'
                for s in search:
                    data.append([
                        s.venta.pk,
                        s.venta.cliente.nombre + ' ' + s.venta.cliente.apellido,
                        s.fecha.strftime('%d-%m-%Y'),
                        format(s.valor, '.2f'),
                        format(s.saldo, '.2f'),
                    ])
                cli = Cliente.objects.get(pk=clien)
                cliente = {'cliente': cli, 'reporte': fitro_text, 'cedula': cli.c_i, 'fecha': datetime.now}
            data_sum = []
            total_valor = search.aggregate(r=Coalesce(Sum('valor'), 0)).get('r')
            total_saldo = search.aggregate(r=Coalesce(Sum('saldo'), 0)).get('r')
            data_sum.append([
                '---',
                '---',
                '',
                format(total_valor, '.2f'),
                format(total_saldo, '.2f'),
            ])

            ima = 'logo.png'
            emp = Empresa.objects.get(pk=1)
            if emp.imagen:
                ima = emp.imagen
            context = {
                'cliente': cliente,
                'productos': data,
                'sumFinal': data_sum,
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
        return HttpResponseRedirect(reverse_lazy('reports:cuentas_venta_report'))
