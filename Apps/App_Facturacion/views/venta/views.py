import json
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import CreateView, ListView, DeleteView, UpdateView, TemplateView
from reportlab.lib import colors
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import cm
from reportlab.platypus import TableStyle, Table
from xhtml2pdf import pisa
from datetime import datetime
from Apps.App_Facturacion.forms import venta_form, pedido_form, cliente_form
from Apps.App_Facturacion.models import Venta, Producto, Detalle_Venta, Cliente, Cuentas, Pedido, Inventario, Empresa
from reportlab.pdfgen import canvas
from django.views.generic import View
from django.conf import settings
from io import BytesIO

class venta_list_view(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'venta/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Venta.objects.all().order_by(Coalesce('id', 'cliente').desc()):
                    data.append(i.toJSON())
                    # pedido = Pedido.objects.filter(venta_id=i.id)
            elif action == 'search_details_prod':
                data = []
                for i in Detalle_Venta.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'anular':
                with transaction.atomic():
                    venta = Venta.objects.get(id=request.POST['id'])
                    venta.estado = False
                    venta.save(update_fields=["estado"])
                    if Cuentas.objects.filter(venta_id=venta.id).exists():
                        cuentas_v = Cuentas.objects.get(venta_id=venta.id)
                        cuentas_v.estado_venta = False
                        cuentas_v.save(update_fields=["estado_venta"])
                    if Pedido.objects.filter(venta_id=venta.id).exists():
                        pedido = Pedido.objects.get(venta_id=venta.id)
                        pedido.estado = False
                        pedido.save(update_fields=["estado"])
                    for i in venta.detalle_venta_set.all():
                        pro = Producto.objects.get(id=i.inventario.producto.id)
                        pro.stock = float(pro.stock) + (float(i.cantidad)*float(i.inventario.conversion_stock))
                        pro.save(update_fields=["stock"])
            elif action == 'add':
                with transaction.atomic():
                    pedido = Pedido()
                    pedido.venta_id = request.POST['venta']
                    pedido.fecha_entrega = datetime.strptime(request.POST['fecha_entrega'], "%d-%m-%Y %H:%M %p")
                    pedido.direccion = request.POST['direccion']
                    pedido.total = request.POST['total']
                    pedido.descripcion = request.POST['descripcion']
                    pedido.ubicacion = request.POST['ubicacion']
                    pedido.ubicacion_link = request.POST['ubicacion_link']
                    pedido.save()
                    venta = Venta.objects.get(id=request.POST['venta'])
                    venta.estado_pedido = True
                    venta.save(update_fields=["estado_pedido"])
            # elif action == 'edit':
            #     with transaction.atomic():
            #         pedido = Pedido()
            #         pedido.id = request.POST['id']
            #         pedido.venta_id = request.POST['venta']
            #         pedido.fecha_entrega = request.POST['fecha_entrega']
            #         pedido.direccion = request.POST['direccion']
            #         pedido.descripcion = request.POST['descripcion']
            #         pedido.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('App_Facturacion:venta_create')
        context['list_url'] = reverse_lazy('App_Facturacion:venta_list')
        context['proforma_url'] = reverse_lazy('App_Facturacion:proforma_list')
        context['pedido_url'] = reverse_lazy('App_Facturacion:pedido_list')
        context['entity'] = 'Ventas'
        context['form'] = pedido_form
        context['date_now'] = datetime.now
        return context

class venta_create_view(LoginRequiredMixin, CreateView):
    model = Venta
    form_class = venta_form
    template_name = 'venta/create.html'
    success_url = reverse_lazy('App_Facturacion:venta_list')
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
                list_invt = Inventario.objects.filter(Q(producto__nombre__icontains=request.POST['term'])|Q(producto__descripcion__icontains=request.POST['term'])|Q(producto__marca__nombre__icontains=request.POST['term']))[0:10]
                for i in list_invt:
                    item = i.toJSON()
                    item['value'] = i.producto.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    venta = Venta()
                    venta.cliente_id = vents['cliente']
                    venta.subtotal = float(vents['subtotal'])
                    venta.iva = float(vents['iva'])
                    venta.total = float(vents['total'])
                    venta.metodo_pago = bool(vents['metodo_pago'])
                    venta.iva_base = request.POST['iva_base']
                    venta.save()
                    print(vents)
                    if venta.metodo_pago:
                        cuentas=Cuentas()
                        cuentas.venta_id = venta.id
                        cuentas.valor = venta.total
                        cuentas.saldo = venta.total
                        cuentas.descripcion = vents['descripcion']
                        cuentas.save()
                    for i in vents['products']:
                        det = Detalle_Venta()
                        det.venta_id = venta.id
                        det.inventario_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['pvp_medida'])
                        det.total = float(i['subtotal'])
                        det.descuento = float(i['descuento'])
                        det.save()
                        pro = i['producto']
                        pro = Producto.objects.get(id=pro['id'])
                        pro.stock = float(pro.stock) - (float(i['conversion_stock'])*det.cantidad)
                        pro.save(update_fields=["stock"])
                    data = {'id': venta.id}
            elif action == 'search_clientes':
                data = []
                list_cli = Cliente.objects.filter(
                    Q(nombre__icontains=request.POST['term']) | Q(apellido__icontains=request.POST['term']) | Q(
                        c_i__icontains=request.POST['term']))[0:10]
                for i in list_cli:
                    cli = i.toJSON()
                    cli['text'] = i.get_full_name()
                    data.append(cli)
            elif action == 'add_cliente':
                #data = []
                with transaction.atomic():
                    formulario = cliente_form(request.POST)
                    if formulario.is_valid():
                        formulario.save()
                        cli = Cliente.objects.get(c_i=request.POST['c_i'])
                        print(cli)
                        cliente = cli.toJSON()
                        cliente['text'] = cli.get_full_name()
                        data = cliente
                    else:
                        data['error'] = formulario.errors
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
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['frm_cliente'] = cliente_form()
        context['iva'] = self.get_iva_empresa()
        return context

class venta_update_view(LoginRequiredMixin, UpdateView):
    model = Venta
    form_class = venta_form
    template_name = 'venta/create.html'
    success_url = reverse_lazy('App_Facturacion:venta_list')
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
                    print(venta.fecha)
                    venta.cliente_id = vents['cliente']
                    venta.subtotal = float(vents['subtotal'])
                    venta.iva = float(vents['iva'])
                    venta.total = float(vents['total'])
                    venta.metodo_pago = bool(vents['metodo_pago'])
                    venta.tipo_documento = False
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
                        pro = Producto.objects.get(id=i['id'])
                        pro.stock = int(pro.stock) - int(i['cantidad'])
                        pro.save(update_fields=["stock"])
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
        context['title'] = 'Edición de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product())
        return context

class venta_report_view_2(View):

    def header(self, pdf, id):
        vent = Venta.objects.get(id=id)
        # # Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        # archivo_imagen = settings.MEDIA_ROOT + '/imagen/logo_django.png'
        # # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        # pdf.drawImage(archivo_imagen, 2, 350, 120, 90, preserveAspectRatio=True)
        # # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        # pdf.setFont("Helvetica", 16)
        # # Dibujamos una cadena en la ubicación X,Y especificada
        # pdf.drawString(20, 340, u"FERRETERIA CONSTRUCTOR")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(220, 320, u"" + str(vent.fecha))
        pdf.drawString(60, 300, u"" + str(vent.cliente))
        pdf.drawString(60, 280, u"" + str(vent.cliente.direccion))
        pdf.drawString(60, 260, u"" + str(vent.cliente.ruc or vent.cliente.c_i))

    def footer(self, pdf, id):
        vent = Venta.objects.get(id=id)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(250, 70, u"" + str(vent.subtotal))
        pdf.drawString(250, 30, u"" + str(vent.iva))
        pdf.drawString(250, 20, u"" + str(vent.total))

    def get(self, request, *args, **kwargs):
        # Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        # Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer, pagesize=A6)
        # Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.header(pdf, kwargs.get('pk'))
        self.footer(pdf, kwargs.get('pk'))
        self.tabla(pdf, kwargs.get('pk'))
        # Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    def tabla(self, pdf, id):
        # Creamos una tupla de encabezados para neustra tabla
        # encabezados = ('Cant', 'Descripción', 'P/Unit', 'Total')
        # Creamos una lista de tuplas que van a contener a las personas

        detalles = [(det.cantidad, det.producto.nombre + ' ' + det.producto.descripcion, det.precio, det.total) for det
                    in
                    Detalle_Venta.objects.filter(venta_id=id)]
        count = len(detalles)

        # Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table(detalles, colWidths=[1 * cm, 5.1 * cm, 1.5 * cm, 1.5 * cm])
        # Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                # La primera fila(encabezados) va a estar centrada
                # ('ALIGN', (0, 0), (3, 0), 'CENTER'),
                # Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.white),
                # El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        # Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_orden.wrapOn(pdf, 30, 200)
        # Definimos la coordenada donde se dibujará la tabla
        # y=220-(count*10)
        y = 0
        if count == 1:
            y = 230
        elif count == 2:
            y = 210
        elif count == 3:
            y = 190
        elif count == 4:
            y = 170

        print(y)
        detalle_orden.drawOn(pdf, 30, y)

class venta_factura_view(View):
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
            template = get_template('venta/factura.html')
            venta = Venta.objects.get(pk=self.kwargs['pk'])
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
            context = {
                'estado': estado,
                'venta': venta,
                'comp': {'name': emp.nombre, 'ruc': emp.ruc, 'correo': emp.correo,
                         'address': emp.ciudad, 'ubicacion': emp.direccion, 'telefono': emp.telefono},
                'icon': '{}{}'.format(settings.MEDIA_URL, ima),
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
        return HttpResponseRedirect(reverse_lazy('App_Facturacion:venta_list'))
