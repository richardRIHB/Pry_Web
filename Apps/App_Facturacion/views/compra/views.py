import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, UpdateView, View
from Apps.App_Facturacion.forms import compra_form
from Apps.App_Facturacion.models import Compra, Producto, Detalle_Compra, Proveedor, Cuentas_Compra, Empresa, Inventario
from datetime import datetime
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class compra_view(LoginRequiredMixin, TemplateView):
    template_name = 'compra/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Compra.objects.order_by('-id'):
                    data.append(i.toJSON())
            elif action == 'search_detalle_producto':
                data = []
                for i in Detalle_Compra.objects.filter(compra_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'delete':
                comp = Compra.objects.get(pk=request.POST['id'])
                contador = 0
                for i in comp.detalle_compra_set.all():
                    prod = Producto.objects.get(pk=i.producto.id)
                    if i.cantidad > prod.stock:
                        contador = 1
                if contador == 0:
                    with transaction.atomic():
                        if Cuentas_Compra.objects.filter(compra_id=comp.id).exists():
                            cuentas_com = Cuentas_Compra.objects.get(compra_id=comp.id)
                            if cuentas_com.estado:
                                cuentas_com.estado_compra = False
                                cuentas_com.save()
                                comp.estado = False
                                comp.save()
                                for i in comp.detalle_compra_set.all():
                                    prod = Producto.objects.get(pk=i.producto.id)
                                    precio_base_actual = float(prod.stock) * float(prod.precio_bruto)
                                    precio_base_compra = i.cantidad * float(i.precio)
                                    precio_base_acumulado = precio_base_actual - precio_base_compra
                                    stock_acumulado = float(prod.stock) - i.cantidad
                                    precio_actualizado = 0
                                    if precio_base_acumulado == 0:
                                        precio_actualizado = 0
                                    elif stock_acumulado == 0:
                                        precio_actualizado = prod.precio_bruto
                                    else:
                                        precio_actualizado = precio_base_acumulado / stock_acumulado
                                    prod.precio_bruto = precio_actualizado
                                    prod.stock -= i.cantidad
                                    calculo_iva = float(prod.precio_bruto) * (float(prod.iva) + 1)
                                    calculo_ganancia = calculo_iva * ((float(prod.porcentaje_ganancia) / 100) + 1)
                                    prod.precio = calculo_ganancia
                                    prod.save()

                                    for a in Inventario.objects.filter(producto_id=prod.pk):
                                        inv = Inventario.objects.get(pk=a.id)
                                        if inv.tipo_conversion == True:
                                            pvp_medida = float(inv.producto.precio) * float(inv.equivalencia)
                                            pvp_medida = pvp_medida - (
                                                    (float(inv.porcentaje_conversion) / 100) * pvp_medida)
                                            inv.pvp_medida = pvp_medida
                                            inv.save()
                                        else:
                                            pvp_medida = float(inv.producto.precio) / float(inv.equivalencia)
                                            pvp_medida = ((float(inv.porcentaje_conversion) / 100) + 1) * pvp_medida
                                            inv.pvp_medida = pvp_medida
                                            inv.save()
                            else:
                                data['error'] = 'No se puede eliminar la Factura, debido a que tiene un saldo pendiente de.- $' + str(
                                    cuentas_com.saldo)
                        else:
                            comp.estado = False
                            comp.save()
                            for i in comp.detalle_compra_set.all():
                                prod = Producto.objects.get(pk=i.producto.id)
                                precio_base_actual = float(prod.stock) * float(prod.precio_bruto)
                                precio_base_compra = i.cantidad * float(i.precio)
                                precio_base_acumulado = precio_base_actual - precio_base_compra
                                stock_acumulado = float(prod.stock) - i.cantidad
                                precio_actualizado = 0
                                if precio_base_acumulado == 0:
                                    precio_actualizado = 0
                                elif stock_acumulado == 0:
                                    precio_actualizado = prod.precio_bruto
                                else:
                                    precio_actualizado = precio_base_acumulado / stock_acumulado
                                prod.precio_bruto = precio_actualizado
                                prod.stock -= i.cantidad
                                calculo_iva = float(prod.precio_bruto) * (float(prod.iva) + 1)
                                calculo_ganancia = calculo_iva * ((float(prod.porcentaje_ganancia) / 100) + 1)
                                prod.precio = calculo_ganancia
                                prod.save()

                                for a in Inventario.objects.filter(producto_id=prod.pk):
                                    inv = Inventario.objects.get(pk=a.id)
                                    if inv.tipo_conversion == True:
                                        pvp_medida = float(inv.producto.precio) * float(inv.equivalencia)
                                        pvp_medida = pvp_medida - (
                                                    (float(inv.porcentaje_conversion) / 100) * pvp_medida)
                                        inv.pvp_medida = pvp_medida
                                        inv.save()
                                    else:
                                        pvp_medida = float(inv.producto.precio) / float(inv.equivalencia)
                                        pvp_medida = ((float(inv.porcentaje_conversion) / 100) + 1) * pvp_medida
                                        inv.pvp_medida = pvp_medida
                                        inv.save()
                else:
                    data['error'] = 'La cantidad de productos es superior al stock actual'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['list_url'] = reverse_lazy('App_Facturacion:compra_list')
        context['create_url'] = reverse_lazy('App_Facturacion:compra_create')
        context['list_proforma_url'] = reverse_lazy('App_Facturacion:proforma_compra_list')
        context['entity'] = 'Compras'
        context['date_now'] = datetime.now
        return context

class CompraCreateView(LoginRequiredMixin, CreateView):
    model = Compra
    form_class = compra_form
    template_name = 'compra/create.html'
    success_url = reverse_lazy('App_Facturacion:compra_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_productos':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                prods = Producto.objects.filter(Q(nombre__icontains=request.POST['term']) | Q(descripcion__icontains=request.POST['term']) | Q(marca__nombre__icontains=request.POST['term']))
                for i in prods.exclude(pk__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'search_proveedor':
                data = []
                prove = Proveedor.objects.filter(Q(nombre__icontains=request.POST['term']) | Q(apellido__icontains=request.POST['term']) | Q(empresa__icontains=request.POST['term']))[0:10]
                for i in prove:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    compra_diccionario = json.loads(request.POST['compra_diccionario'])
                    comp = Compra()
                    comp.proveedor_id = compra_diccionario['proveedor']
                    fecha_entrega = datetime.strptime(compra_diccionario['fecha'], '%d-%m-%Y')
                    comp.fecha = datetime.strftime(fecha_entrega, '%Y-%m-%d')  # trasformar
                    comp.subtotal = compra_diccionario['subtotal']
                    comp.iva_base = compra_diccionario['iva_base']
                    comp.iva = compra_diccionario['iva']
                    comp.total = compra_diccionario['total']
                    metodo_p = request.POST['metodo_pago_valor']
                    comp.metodo_pago = metodo_p.capitalize()
                    comp.save()
                    if comp.metodo_pago == 'True':
                        cuentas = Cuentas_Compra()
                        cuentas.compra_id = comp.id
                        cuentas.descripcion = request.POST['descripcion_metodo_pago']
                        cuentas.valor = compra_diccionario['total']
                        cuentas.saldo = compra_diccionario['total']
                        cuentas.save()
                    for i in compra_diccionario['productos']:
                        detalle = Detalle_Compra()
                        detalle.compra_id = comp.id
                        detalle.producto_id = i['id']
                        detalle.cantidad = i['cantidad']
                        detalle.precio = i['precio_new']
                        detalle.subtotal = i['subtotal']
                        detalle.save()

                        prod = Producto.objects.get(pk=i['id'])
                        precio_base_anterior = float(prod.stock) * float(prod.precio_bruto)
                        precio_base_nuevo = i['cantidad'] * float(i['precio_new'])
                        precio_base_acumulado = precio_base_anterior + precio_base_nuevo
                        stock_acumulado = float(prod.stock) + i['cantidad']
                        precio_actualizado = precio_base_acumulado / stock_acumulado
                        prod.precio_bruto = precio_actualizado
                        prod.stock += i['cantidad']
                        calculo_iva = float(prod.precio_bruto) * (float(comp.iva_base) + 1)
                        calculo_ganancia = calculo_iva * ((float(prod.porcentaje_ganancia) / 100) + 1)
                        prod.precio = calculo_ganancia
                        prod.save()

                        for a in Inventario.objects.filter(producto_id=prod.pk):
                            inv = Inventario.objects.get(pk=a.id)
                            if inv.tipo_conversion == True:
                                pvp_medida = float(inv.producto.precio) * float(inv.equivalencia)
                                pvp_medida = pvp_medida - ((float(inv.porcentaje_conversion) / 100) * pvp_medida)
                                inv.pvp_medida = pvp_medida
                                inv.save()
                            else:
                                pvp_medida = float(inv.producto.precio) / float(inv.equivalencia)
                                pvp_medida = ((float(inv.porcentaje_conversion) / 100) + 1) * pvp_medida
                                inv.pvp_medida = pvp_medida
                                inv.save()
                    data = {'id': comp.id}
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
        context['title'] = 'Creación de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['iva_base'] = self.get_iva_empresa()
        context['detalle_pro'] = []
        return context

class CompraUpdateView(LoginRequiredMixin, UpdateView):
    model = Compra
    form_class = compra_form
    template_name = 'compra/create.html'
    success_url = reverse_lazy('App_Facturacion:compra_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_productos':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                prods = Producto.objects.filter(Q(nombre__icontains=request.POST['term']) | Q(descripcion__icontains=request.POST['term']) | Q(marca__nombre__icontains=request.POST['term']))
                for i in prods.exclude(pk__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'search_proveedor':
                data = []
                prove = Proveedor.objects.filter(Q(nombre__icontains=request.POST['term']) | Q(apellido__icontains=request.POST['term']) | Q(empresa__icontains=request.POST['term']))[0:10]
                for i in prove:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    compra_diccionario = json.loads(request.POST['compra_diccionario'])
                    comp = Compra.objects.get(pk=self.get_object().id)
                    comp.proveedor_id = compra_diccionario['proveedor']
                    fecha_entrega = datetime.strptime(compra_diccionario['fecha'], '%d-%m-%Y')
                    comp.fecha = datetime.strftime(fecha_entrega, '%Y-%m-%d')  # trasformar
                    comp.subtotal = compra_diccionario['subtotal']
                    comp.iva_base = compra_diccionario['iva_base']
                    comp.iva = compra_diccionario['iva']
                    comp.total = compra_diccionario['total']
                    comp.tipo_documento = False
                    metodo_p = request.POST['metodo_pago_valor']
                    comp.metodo_pago = metodo_p.capitalize()
                    comp.save()
                    if comp.metodo_pago == 'True':
                        cuentas = Cuentas_Compra()
                        cuentas.compra_id = comp.id
                        cuentas.descripcion = request.POST['descripcion_metodo_pago']
                        cuentas.valor = float(compra_diccionario['total'])
                        cuentas.saldo = float(compra_diccionario['total'])
                        cuentas.save()
                    # Eliminamos el detalle anterior para poder actualizar
                    comp.detalle_compra_set.all().delete()
                    for i in compra_diccionario['productos']:
                        detalle = Detalle_Compra()
                        detalle.compra_id = comp.id
                        detalle.producto_id = i['id']
                        detalle.cantidad = i['cantidad']
                        detalle.precio = float(i['precio_new'])
                        detalle.subtotal = float(i['subtotal'])
                        detalle.save()

                        prod = Producto.objects.get(pk=i['id'])
                        precio_base_anterior = float(prod.stock) * float(prod.precio_bruto)
                        precio_base_nuevo = i['cantidad'] * float(i['precio_new'])
                        precio_base_acumulado = precio_base_anterior + precio_base_nuevo
                        stock_acumulado = float(prod.stock) + i['cantidad']
                        precio_actualizado = precio_base_acumulado / stock_acumulado
                        prod.precio_bruto = precio_actualizado
                        prod.stock += i['cantidad']
                        calculo_iva = float(prod.precio_bruto) * (float(comp.iva_base) + 1)
                        calculo_ganancia = calculo_iva * ((float(prod.porcentaje_ganancia) / 100) + 1)
                        prod.precio = calculo_ganancia
                        prod.save()

                        for a in Inventario.objects.filter(producto_id=prod.pk):
                            inv = Inventario.objects.get(pk=a.id)
                            if inv.tipo_conversion == True:
                                pvp_medida = float(inv.producto.precio) * float(inv.equivalencia)
                                pvp_medida = pvp_medida - ((float(inv.porcentaje_conversion) / 100) * pvp_medida)
                                inv.pvp_medida = pvp_medida
                            else:
                                pvp_medida = float(inv.producto.precio) / float(inv.equivalencia)
                                pvp_medida = ((float(inv.porcentaje_conversion) / 100) + 1) * pvp_medida
                                inv.pvp_medida = pvp_medida
                            inv.save()
                    data = {'id': comp.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_detalle_productos(self):
        data = []
        try:
            for i in Detalle_Compra.objects.filter(compra_id=self.get_object().id):
                item = i.producto.toJSON()
                item['cantidad'] = i.cantidad
                item['precio_new'] = format(i.precio, '.3f')
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
        context['title'] = 'Facturacion de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['detalle_pro'] = json.dumps(self.get_detalle_productos())
        context['iva_base'] = self.get_iva_empresa()
        return context

class CompraPdfView(LoginRequiredMixin, View):

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

        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('compra/pdf.html')
            ima = 'logo.png'
            emp = Empresa.objects.get(pk=1)
            if emp.imagen:
                ima = emp.imagen
            context = {
                'compra': Compra.objects.get(pk=self.kwargs['pk']),
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
        return HttpResponseRedirect(reverse_lazy('App_Facturacion:compra_list'))

