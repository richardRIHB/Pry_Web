from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from Apps.App_Facturacion.forms import empresa_form
from Apps.App_Facturacion.models import Empresa, Producto, Inventario
from datetime import datetime

class empresa_view(LoginRequiredMixin, TemplateView):
    template_name = 'empresa/create.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                verifi = request.POST['id']
                if verifi == '0':
                    with transaction.atomic():
                        formulario = empresa_form(request.POST, request.FILES or None)
                        if formulario.is_valid():
                            nuevo_emp = Empresa(
                                id=1,
                                nombre=formulario.cleaned_data.get('nombre'),
                                ruc=formulario.cleaned_data.get('ruc'),
                                telefono=formulario.cleaned_data.get('telefono'),
                                correo=formulario.cleaned_data.get('correo'),
                                ciudad=formulario.cleaned_data.get('ciudad'),
                                direccion=formulario.cleaned_data.get('direccion'),
                                sitio_web=formulario.cleaned_data.get('sitio_web'),
                                iva=formulario.cleaned_data.get('iva'),
                                imagen=formulario.cleaned_data.get('imagen'),
                                logo_login=formulario.cleaned_data.get('logo_login')
                            )
                            nuevo_emp.save()
                            emp = Empresa.objects.get(pk=1)
                            for i in Producto.objects.all():
                                prod = Producto.objects.get(pk=i.id)
                                prod.iva = emp.iva
                                calculo_iva = float(prod.precio_bruto) * (float(prod.iva) + 1)
                                calculo_ganancia = calculo_iva * ((float(prod.porcentaje_ganancia) / 100) + 1)
                                prod.precio = calculo_ganancia
                                prod.save()
                            for a in Inventario.objects.all():
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
                        else:
                            data['error'] = formulario.errors
            elif action == 'edit':
                with transaction.atomic():
                    emp = Empresa.objects.get(pk=request.POST['id'])
                    formulario = empresa_form(request.POST, request.FILES or None, instance=emp)
                    if formulario.is_valid():
                        formulario.save()
                        for i in Producto.objects.all():
                            prod = Producto.objects.get(pk=i.id)
                            prod.iva = emp.iva
                            calculo_iva = float(prod.precio_bruto) * (float(prod.iva) + 1)
                            calculo_ganancia = calculo_iva * ((float(prod.porcentaje_ganancia)/100) + 1)
                            prod.precio = calculo_ganancia
                            prod.save()
                        for a in Inventario.objects.all():
                            inv = Inventario.objects.get(pk=a.id)
                            if inv.tipo_conversion == True:
                                pvp_medida = float(inv.producto.precio) * float(inv.equivalencia)
                                pvp_medida = pvp_medida-((float(inv.porcentaje_conversion)/100)*pvp_medida)
                                inv.pvp_medida = pvp_medida
                                inv.save()
                            else:
                                pvp_medida = float(inv.producto.precio) / float(inv.equivalencia)
                                pvp_medida = ((float(inv.porcentaje_conversion) / 100) + 1) * pvp_medida
                                inv.pvp_medida = pvp_medida
                                inv.save()
                    else:
                        data['error'] = formulario.errors
            elif action == 'search_empresa':
                data = []
                for i in Empresa.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Configuracion de la Empresa"
        context['entity'] = 'Empresa'
        context['list_url'] = reverse_lazy('App_Facturacion:dashboard')
        context['date_now'] = datetime.now
        context['form'] = empresa_form()
        context['action'] = 'add'
        return context

