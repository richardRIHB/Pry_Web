from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView
from Apps.App_Facturacion.forms import GaleriaForm
from Apps.App_Facturacion.models import Marca, Seccion, Galeria, Bloque, Posicion, Producto
from datetime import datetime

class galeria_view(LoginRequiredMixin, TemplateView):
    template_name = 'galeria/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Galeria.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_producto':
                data = []
                mar = Producto.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in mar:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    formulario = GaleriaForm(request.POST, request.FILES or None)
                    if formulario.is_valid():
                        formulario.save()
                    else:
                        data['error'] = formulario.errors
            elif action == 'edit':
                with transaction.atomic():
                    gale = Galeria.objects.get(pk=request.POST['id'])
                    formulario = GaleriaForm(request.POST, request.FILES or None, instance=gale)
                    if formulario.is_valid():
                        formulario.save()
                    else:
                        data['error'] = formulario.errors
            elif action == 'delete':
                with transaction.atomic():
                    gale = Galeria.objects.get(pk=request.POST['id'])
                    gale.estado = False
                    gale.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ="Listado de galería"
        context['entity'] = 'Galería'
        context['list_url'] = reverse_lazy('App_Facturacion:galeria_list')
        context['count_marca'] = Marca.objects.filter(estado='True').count()
        context['count_ubicacion'] = Bloque.objects.count()+Seccion.objects.count()+Posicion.objects.count()
        context['count_galeria'] = Galeria.objects.count()
        context['date_now'] = datetime.now
        context['form'] = GaleriaForm()
        return context

class galeria_show_view(DetailView):
    model = Galeria
    template_name = 'galeria/show.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Información'
        context['list_url'] = reverse_lazy('App_Facturacion:galeria_list')
        context['entity'] = 'Galería'
        context['count_marca'] = Marca.objects.filter(estado='True').count()
        context['count_ubicacion'] = Bloque.objects.count()+Seccion.objects.count()+Posicion.objects.count()
        context['count_galeria'] = Galeria.objects.count()
        context['date_now'] = datetime.now
        return context