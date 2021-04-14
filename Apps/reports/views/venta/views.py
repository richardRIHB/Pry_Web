from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.db.models import Q

from Apps.App_Facturacion.models import Venta, Cliente, Empresa
from Apps.reports.forms import report_form

from django.db.models.functions import Coalesce
from django.db.models import Sum

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class report_venta_view(LoginRequiredMixin, TemplateView):
    template_name = 'venta/report.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                separador = "-"
                separado = end_date.split(separador)
                end_date = datetime(int(separado[0]), int(separado[1]), int(separado[2]), 23, 59, 0)
                cliente = request.POST.get('cliente', '')
                search = ''
                if start_date and end_date and cliente == '':
                    search = Venta.objects.all()
                    search = search.filter(fecha__range=[start_date, end_date])
                    search = search.filter(estado=True)
                    for s in search:
                        data.append([
                            s.id,
                            s.cliente.nombre + ' ' + s.cliente.apellido,
                            s.fecha.strftime('%Y-%m-%d'),
                            format(s.subtotal, '.2f'),
                            format(s.iva, '.2f'),
                            format(s.total, '.2f'),
                        ])
                elif start_date and end_date and cliente:
                    search = Venta.objects.filter(cliente_id=cliente)
                    search = search.filter(fecha__range=[start_date, end_date])
                    search = search.filter(estado=True)
                    for s in search:
                        data.append([
                            s.id,
                            s.cliente.nombre + ' ' + s.cliente.apellido,
                            s.fecha.strftime('%Y-%m-%d'),
                            format(s.subtotal, '.2f'),
                            format(s.iva, '.2f'),
                            format(s.total, '.2f'),
                        ])
                subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
                iva = search.aggregate(r=Coalesce(Sum('iva'), 0)).get('r')
                total = search.aggregate(r=Coalesce(Sum('total'), 0)).get('r')

                data.append([
                    '---',
                    '---',
                    '---',
                    format(subtotal, '.2f'),
                    format(iva, '.2f'),
                    format(total, '.2f'),
                ])
            elif action == 'search_clientes':
                data = []
                list_cli = Cliente.objects.filter(Q(nombre__icontains=request.POST['term']) | Q(apellido__icontains=request.POST['term']) | Q(c_i__icontains=request.POST['term']))[0:10]
                for i in list_cli:
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
        context['title'] = 'Reporte de Ventas'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('reports:venta_report')
        context['list_cuentas_venta'] = reverse_lazy('reports:cuentas_venta_report')
        context['form'] = report_form()
        return context

class reporte_venta_pdf_view(LoginRequiredMixin, View):

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
            template = get_template('venta/pdf_repor.html')
            fecha_ini = self.kwargs['fecha_ini']
            fecha_fin = self.kwargs['fecha_fin']
            fecha_fin_normal = fecha_fin
            separador = "-"
            separado = fecha_fin.split(separador)
            fecha_fin = datetime(int(separado[0]), int(separado[1]), int(separado[2]), 23, 59, 0)
            clien = self.kwargs['pk']
            cliente = []
            data = []
            search = ''
            if fecha_ini and fecha_fin and clien == 'null':
                search = Venta.objects.all()
                search = search.filter(fecha__range=[fecha_ini, fecha_fin])
                search = search.filter(estado=True)
                for s in search:
                    data.append([
                        s.id,
                        s.cliente.nombre + ' ' + s.cliente.apellido,
                        s.fecha.strftime('%Y-%m-%d'),
                        format(s.subtotal, '.2f'),
                        format(s.iva, '.2f'),
                        format(s.total, '.2f'),
                    ])
                cliente = {'cliente': '------------------', 'reporte': 'Reporte de Ventas', 'cedula': '------------------', 'fecha': fecha_ini + ' - ' + fecha_fin_normal}
            elif fecha_ini and fecha_fin and clien != 'null':
                search = Venta.objects.filter(cliente_id=clien)
                search = search.filter(fecha__range=[fecha_ini, fecha_fin])
                search = search.filter(estado=True)
                for s in search:
                    data.append([
                        s.id,
                        s.cliente.nombre + ' ' + s.cliente.apellido,
                        s.fecha.strftime('%Y-%m-%d'),
                        format(s.subtotal, '.2f'),
                        format(s.iva, '.2f'),
                        format(s.total, '.2f'),
                    ])
                cli = Cliente.objects.get(pk=clien)
                cliente = {'cliente': cli, 'reporte': 'Reporte de Ventas', 'cedula': cli.c_i, 'fecha': fecha_ini + ' - ' + fecha_fin_normal}
            data_sum = []
            subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
            iva = search.aggregate(r=Coalesce(Sum('iva'), 0)).get('r')
            total = search.aggregate(r=Coalesce(Sum('total'), 0)).get('r')

            data_sum.append([
                '---',
                '---',
                '',
                format(subtotal, '.2f'),
                format(iva, '.2f'),
                format(total, '.2f'),
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
        return HttpResponseRedirect(reverse_lazy('reports:venta_report'))
