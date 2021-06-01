from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.db.models import Q
from Apps.App_Facturacion.models import Producto, Empresa, Inventario
from Apps.reports.forms import report_inventario_form
from datetime import datetime

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class reporte_inventario_view(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/reporte.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                produc = request.POST.get('produc', '')
                t_estado = request.POST.get('t_estado')
                prod_inv = ''
                if produc:
                    prod_inv = Inventario.objects.filter(producto_id=produc)
                    if t_estado == 'btnActivo':
                        prod_inv = prod_inv.filter(estado=True)
                    elif t_estado == 'btnBloqueado':
                        prod_inv = prod_inv.filter(estado=False)

                    for s in prod_inv:
                        t_conversion = str(s.porcentaje_conversion) + '% ↑'
                        if s.tipo_conversion == True:
                            t_conversion = str(s.porcentaje_conversion) + '% ↓'
                        estado = 'Bloqueado'
                        if s.estado == True:
                            estado = 'Activo'
                        data.append([
                            s.producto.id,
                            s.producto.nombre + ' ' + s.producto.descripcion + ' ' + s.producto.marca.nombre,
                            s.medida + ' (' + format(s.equivalencia, '.2f') + ')',
                            s.producto.stock,
                            t_conversion,
                            estado,
                            format(s.pvp_medida, '.2f')
                        ])
                else:
                    prod_inv = Inventario.objects.all().order_by('producto__nombre','producto_id')
                    if t_estado == 'btnActivo':
                        prod_inv = prod_inv.filter(estado=True)
                    elif t_estado == 'btnBloqueado':
                        prod_inv = prod_inv.filter(estado=False)

                    for s in prod_inv:
                        t_conversion = str(s.porcentaje_conversion) + '% ↑'
                        if s.tipo_conversion == True:
                            t_conversion = str(s.porcentaje_conversion) + '% ↓'
                        estado = 'Bloqueado'
                        if s.estado == True:
                            estado = 'Activo'
                        data.append([
                            s.producto.id,
                            s.producto.nombre + ' ' + s.producto.descripcion + ' ' + s.producto.marca.nombre,
                            s.medida + ' (' + format(s.equivalencia, '.2f') + ')',
                            s.producto.stock,
                            t_conversion,
                            estado,
                            format(s.pvp_medida, '.2f')
                        ])
                suma_total = 0
                stock_total = 0
                for s in prod_inv:
                    suma_total += float(s.pvp_medida)
                prod_inv = prod_inv.order_by().distinct('producto')
                for s in prod_inv:
                    stock_total += s.producto.stock
                data.append([
                    '___',
                    '___',
                    '___',
                    stock_total,
                    '___',
                    '___',
                    format(suma_total, '.2f')
                ])

            elif action == 'search_producto':
                data = []
                prod = Producto.objects.filter(Q(nombre__icontains=request.POST['term']) | Q(descripcion__icontains=request.POST['term']) | Q(marca__nombre__icontains=request.POST['term']))
                for i in prod[0:10]:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Inventario'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('reports:inventario_report')
        context['form'] = report_inventario_form()
        return context

class reporte_inventario_pdf_view(LoginRequiredMixin, View):

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
            template = get_template('inventario/pdf.html')
            pk = self.kwargs['pk']
            t_estado = self.kwargs['filtro']
            producto = []
            data = []
            prod_inv = ''
            text_estado = 'Todo'
            if pk == 'null':
                prod_inv = Inventario.objects.all().order_by('producto__nombre','producto_id')
                if t_estado == 'btnActivo':
                    prod_inv = prod_inv.filter(estado=True)
                    text_estado = 'Activo'
                elif t_estado == 'btnBloqueado':
                    prod_inv = prod_inv.filter(estado=False)
                    text_estado = 'Bloqueado'
                for s in prod_inv:
                    t_conversion = str(s.porcentaje_conversion) + '% ↑'
                    if s.tipo_conversion == True:
                        t_conversion = str(s.porcentaje_conversion) + '% ↓'
                    estado = 'Bloqueado'
                    if s.estado == True:
                        estado = 'Activo'
                    data.append([
                        s.producto.id,
                        s.producto.nombre + ' ' + s.producto.descripcion + ' ' + s.producto.marca.nombre,
                        s.medida + ' (' + format(s.equivalencia, '.2f') + ')',
                        s.producto.stock,
                        t_conversion,
                        estado,
                        format(s.pvp_medida, '.2f')
                    ])
                producto = {'nombre': '------------------', 'reporte': 'Reporte de Inventario', 'marca': '------------------',
                            'text_estado': text_estado, 'fecha': datetime.now}
            else:
                prod_inv = Inventario.objects.filter(producto_id=pk)
                if t_estado == 'btnActivo':
                    prod_inv = prod_inv.filter(estado=True)
                    text_estado = 'Activo'
                elif t_estado == 'btnBloqueado':
                    prod_inv = prod_inv.filter(estado=False)
                    text_estado = 'Bloqueado'
                for s in prod_inv:
                    t_conversion = str(s.porcentaje_conversion) + '% ↑'
                    if s.tipo_conversion == True:
                        t_conversion = str(s.porcentaje_conversion) + '% ↓'
                    estado = 'Bloqueado'
                    if s.estado == True:
                        estado = 'Activo'
                    data.append([
                        s.producto.id,
                        s.producto.nombre + ' ' + s.producto.descripcion + ' ' + s.producto.marca.nombre,
                        s.medida + ' (' + format(s.equivalencia, '.2f') + ')',
                        s.producto.stock,
                        t_conversion,
                        estado,
                        format(s.pvp_medida, '.2f')
                    ])
                pro = Producto.objects.get(pk=pk)
                producto = {'nombre': pro.nombre, 'reporte': 'Reporte de Inventario', 'marca': pro.marca.nombre,
                            'text_estado': text_estado, 'fecha': datetime.now}

            suma_total = 0
            stock_total = 0
            data_sum = []
            for s in prod_inv:
                suma_total += float(s.pvp_medida)
            prod_inv = prod_inv.order_by().distinct('producto')
            for s in prod_inv:
                stock_total += s.producto.stock
            data_sum.append([
                '___',
                '___',
                '___',
                stock_total,
                '___',
                '___',
                format(suma_total, '.2f')
            ])

            ima = 'logo.png'
            emp = Empresa.objects.get(pk=1)
            if emp.imagen:
                ima = emp.imagen
            context = {
                'producto': producto,
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
        return HttpResponseRedirect(reverse_lazy('reports:inventario_report'))
