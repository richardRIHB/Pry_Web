from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from Apps.App_Facturacion.forms import UbicacionForm
from Apps.App_Facturacion.models import Marca, Seccion, Galeria, Bloque, Posicion
from datetime import datetime

class ubicacion_view(LoginRequiredMixin, TemplateView):
    template_name = 'ubicacion/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            modulo = request.POST['modulo']
            if action == 'searchBloque':
                data = []
                for i in Bloque.objects.all():
                    data.append(i.toJSON())
            elif action == 'searchSeccion':
                data = []
                for i in Seccion.objects.all():
                    data.append(i.toJSON())
            elif action == 'searchPosicion':
                data = []
                for i in Posicion.objects.all():
                    data.append(i.toJSON())
            elif modulo == 'moduloBloque':
                if action == 'add':
                    with transaction.atomic():
                        blo = Bloque()
                        blo.nombre = request.POST['nombre']
                        blo.descripcion = request.POST['descripcion']
                        estad = request.POST['estado_valor']
                        blo.estado = estad.capitalize()
                        blo.save()
                elif action == 'edit':
                    with transaction.atomic():
                        blo = Bloque.objects.get(pk=request.POST['id'])
                        blo.nombre = request.POST['nombre']
                        blo.descripcion = request.POST['descripcion']
                        estad = request.POST['estado_valor']
                        blo.estado = estad.capitalize()
                        blo.save()
                elif action == 'delete':
                    with transaction.atomic():
                        blo = Bloque.objects.get(pk=request.POST['id'])
                        blo.estado = False
                        blo.save()
                else:
                    data['error'] = 'Ha ocurrido un error en el Modulo Bloque'
            elif modulo == 'moduloSeccion':
                if action == 'add':
                    with transaction.atomic():
                        sec = Seccion()
                        sec.nombre = request.POST['nombre']
                        sec.descripcion = request.POST['descripcion']
                        estad = request.POST['estado_valor']
                        sec.estado = estad.capitalize()
                        sec.save()
                elif action == 'edit':
                    with transaction.atomic():
                        sec = Seccion.objects.get(pk=request.POST['id'])
                        sec.nombre = request.POST['nombre']
                        sec.descripcion = request.POST['descripcion']
                        estad = request.POST['estado_valor']
                        sec.estado = estad.capitalize()
                        sec.save()
                elif action == 'delete':
                    with transaction.atomic():
                        sec = Seccion.objects.get(pk=request.POST['id'])
                        sec.estado = False
                        sec.save()
                else:
                    data['error'] = 'Ha ocurrido un error en el Modulo Seccion'
            elif modulo == 'moduloPosicion':
                if action == 'add':
                    with transaction.atomic():
                        pos = Posicion()
                        pos.nombre = request.POST['nombre']
                        pos.descripcion = request.POST['descripcion']
                        estad = request.POST['estado_valor']
                        pos.estado = estad.capitalize()
                        pos.save()
                elif action == 'edit':
                    with transaction.atomic():
                        pos = Posicion.objects.get(pk=request.POST['id'])
                        pos.nombre = request.POST['nombre']
                        pos.descripcion = request.POST['descripcion']
                        estad = request.POST['estado_valor']
                        pos.estado = estad.capitalize()
                        pos.save()
                elif action == 'delete':
                    with transaction.atomic():
                        pos = Posicion.objects.get(pk=request.POST['id'])
                        pos.estado = False
                        pos.save()
                else:
                    data['error'] = 'Ha ocurrido un error en el Modulo Posicion'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Ubicaciones"
        context['title_1'] = "Listado de Bloques"
        context['title_2'] = "Listado de Secciones"
        context['title_3'] = "Listado de Posiciones"
        context['entity'] = 'Ubicacion'
        context['list_url'] = reverse_lazy('App_Facturacion:ubicacion_list')
        context['count_marca'] = Marca.objects.filter(estado='True').count()
        context['count_ubicacion'] = Bloque.objects.count()+Seccion.objects.count()+Posicion.objects.count()
        context['count_galeria'] = Galeria.objects.count()
        context['date_now'] = datetime.now
        context['form'] = UbicacionForm()
        return context