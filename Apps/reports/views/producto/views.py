from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.db.models import Q
from Apps.App_Facturacion.models import Producto, Detalle_Compra, Proveedor, Empresa
from Apps.reports.forms import reporte_producto_form
from datetime import datetime

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class reporte_producto_view(LoginRequiredMixin, TemplateView):
    template_name = 'producto/reporte.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                filtro = request.POST.get('filtro', '')
                provee = request.POST.get('provee', '')
                if provee:
                    Prod_Provee = Detalle_Compra.objects.filter(compra__proveedor_id=provee)
                    Prod_Provee = Prod_Provee.order_by().distinct('producto')
                    if filtro == 'todo_prod':
                        for s in Prod_Provee:
                            data.append([
                                s.producto.id,
                                s.producto.nombre,
                                s.producto.descripcion,
                                s.producto.marca.nombre,
                                s.producto.stock,
                                s.producto.stock_minimo,
                                format(s.producto.precio, '.2f')
                            ])
                    elif filtro == 'minimo_prod':
                        for s in Prod_Provee:
                            if s.producto.stock <= s.producto.stock_minimo:
                                data.append([
                                    s.producto.id,
                                    s.producto.nombre,
                                    s.producto.descripcion,
                                    s.producto.marca.nombre,
                                    s.producto.stock,
                                    s.producto.stock_minimo,
                                    format(s.producto.precio, '.2f')
                                ])
                    elif filtro == 'agotado_prod':
                        for s in Prod_Provee:
                            if s.producto.stock <= 0:
                                data.append([
                                    s.producto.id,
                                    s.producto.nombre,
                                    s.producto.descripcion,
                                    s.producto.marca.nombre,
                                    s.producto.stock,
                                    s.producto.stock_minimo,
                                    format(s.producto.precio, '.2f')
                                ])
                else:
                    search = Producto.objects.all()
                    if filtro == 'todo_prod':
                        for s in search:
                            data.append([
                                s.id,
                                s.nombre,
                                s.descripcion,
                                s.marca.nombre,
                                s.stock,
                                s.stock_minimo,
                                format(s.precio, '.2f')
                            ])
                    elif filtro == 'minimo_prod':
                        for s in search:
                            if s.stock <= s.stock_minimo:
                                data.append([
                                    s.id,
                                    s.nombre,
                                    s.descripcion,
                                    s.marca.nombre,
                                    s.stock,
                                    s.stock_minimo,
                                    format(s.precio, '.2f')
                                ])
                    elif filtro == 'agotado_prod':
                        for s in search:
                            if s.stock <= 0:
                                data.append([
                                    s.id,
                                    s.nombre,
                                    s.descripcion,
                                    s.marca.nombre,
                                    s.stock,
                                    s.stock_minimo,
                                    format(s.precio, '.2f')
                                ])

                suma_total = 0
                stock_total = 0
                stock_minimo_t = 0
                for prod in data:
                    suma_total += float(prod[6])
                    stock_minimo_t += prod[5]
                    stock_total += prod[4]
                data.append([
                    '___',
                    '___',
                    '___',
                    '___',
                    stock_total,
                    stock_minimo_t,
                    format(suma_total, '.2f')
                ])
            elif action == 'search_proveedor':
                data = []
                prove = Proveedor.objects.filter(Q(nombre__icontains=request.POST['term']) | Q(apellido__icontains=request.POST['term']) | Q(empresa__icontains=request.POST['term']))[0:10]
                for i in prove:
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
        context['title'] = 'Reporte del stock de Productos'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('reports:producto_report')
        context['form'] = reporte_producto_form()
        return context

class reporte_producto_pdf_view(LoginRequiredMixin, View):

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
            template = get_template('producto/pdf.html')
            pk = self.kwargs['pk']
            filtro = self.kwargs['filtro']
            proveedor = []
            data = []
            if pk == 'null' and filtro == 'null':
                search = Producto.objects.all()
                for s in search:
                    data.append([
                        s.id,
                        s.nombre,
                        s.descripcion,
                        s.marca.nombre,
                        s.stock,
                        s.stock_minimo,
                        format(s.precio, '.2f')
                    ])
                proveedor = {'proveedor': '------------------', 'reporte': 'Todos los productos', 'empresa': '------------------', 'fecha': datetime.now}
            else:
                if pk == 'null':
                    search = Producto.objects.all()
                    if filtro == 'todo_prod':
                        for s in search:
                            data.append([
                                s.id,
                                s.nombre,
                                s.descripcion,
                                s.marca.nombre,
                                s.stock,
                                s.stock_minimo,
                                format(s.precio, '.2f')
                            ])
                        proveedor = {'proveedor': '------------------', 'reporte': 'Todos los productos',
                                     'empresa': '------------------', 'fecha': datetime.now}
                    elif filtro == 'minimo_prod':
                        for s in search:
                            if s.stock <= s.stock_minimo:
                                data.append([
                                    s.id,
                                    s.nombre,
                                    s.descripcion,
                                    s.marca.nombre,
                                    s.stock,
                                    s.stock_minimo,
                                    format(s.precio, '.2f')
                                ])
                        proveedor = {'proveedor': '------------------', 'reporte': 'Productos con existencia minima',
                                     'empresa': '------------------', 'fecha': datetime.now}
                    elif filtro == 'agotado_prod':
                        for s in search:
                            if s.stock <= 0:
                                data.append([
                                    s.id,
                                    s.nombre,
                                    s.descripcion,
                                    s.marca.nombre,
                                    s.stock,
                                    s.stock_minimo,
                                    format(s.precio, '.2f')
                                ])
                        proveedor = {'proveedor': '------------------', 'reporte': 'Productos agotados',
                                     'empresa': '------------------', 'fecha': datetime.now}
                elif pk != 'null':
                    Prod_Provee = Detalle_Compra.objects.filter(compra__proveedor_id=pk)
                    Prod_Provee = Prod_Provee.order_by().distinct('producto')
                    if filtro == 'todo_prod':
                        for s in Prod_Provee:
                            data.append([
                                s.producto.id,
                                s.producto.nombre,
                                s.producto.descripcion,
                                s.producto.marca.nombre,
                                s.producto.stock,
                                s.producto.stock_minimo,
                                format(s.producto.precio, '.2f')
                            ])
                        provee = Proveedor.objects.get(pk=pk)
                        proveedor = {'proveedor': provee, 'reporte': 'Todos los productos',
                                     'empresa': provee.empresa, 'fecha': datetime.now}
                    elif filtro == 'minimo_prod':
                        for s in Prod_Provee:
                            if s.producto.stock <= s.producto.stock_minimo:
                                data.append([
                                    s.producto.id,
                                    s.producto.nombre,
                                    s.producto.descripcion,
                                    s.producto.marca.nombre,
                                    s.producto.stock,
                                    s.producto.stock_minimo,
                                    format(s.producto.precio, '.2f')
                                ])
                        provee = Proveedor.objects.get(pk=pk)
                        proveedor = {'proveedor': provee, 'reporte': 'Productos con existencia minima',
                                     'empresa': provee.empresa, 'fecha': datetime.now}
                    elif filtro == 'agotado_prod':
                        for s in Prod_Provee:
                            if s.producto.stock <= 0:
                                data.append([
                                    s.producto.id,
                                    s.producto.nombre,
                                    s.producto.descripcion,
                                    s.producto.marca.nombre,
                                    s.producto.stock,
                                    s.producto.stock_minimo,
                                    format(s.producto.precio, '.2f')
                                ])
                        provee = Proveedor.objects.get(pk=pk)
                        proveedor = {'proveedor': provee, 'reporte': 'Productos agotados',
                                     'empresa': provee.empresa, 'fecha': datetime.now}

            suma_total = 0
            stock_total = 0
            stock_minimo_t = 0
            data_sum = []
            for prod in data:
                suma_total += float(prod[6])
                stock_minimo_t += prod[5]
                stock_total += prod[4]
            data_sum.append([
                '___',
                '___',
                '___',
                '___',
                stock_total,
                stock_minimo_t,
                format(suma_total, '.2f')
            ])
            ima = 'logo.png'
            emp = Empresa.objects.get(pk=1)
            if emp.imagen:
                ima = emp.imagen
            context = {
                'proveedor': proveedor,
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
        return HttpResponseRedirect(reverse_lazy('reports:producto_report'))
