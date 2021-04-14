from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView

from Apps.App_Facturacion.forms import MarcaForm
from Apps.App_Facturacion.models import Marca, Seccion, Galeria, Bloque, Posicion
from datetime import datetime

class marca_view(LoginRequiredMixin, TemplateView):
    template_name = 'marca/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Marca.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                with transaction.atomic():
                    formulario = MarcaForm(request.POST)
                    if formulario.is_valid():
                        formulario.save()
                    else:
                        data['error'] = formulario.errors
            elif action == 'edit':
                with transaction.atomic():
                    cli = Marca.objects.get(pk=request.POST['id'])
                    formulario = MarcaForm(request.POST, instance=cli)
                    if formulario.is_valid():
                        formulario.save()
                    else:
                        data['error'] = formulario.errors
            elif action == 'delete':
                with transaction.atomic():
                    mar = Marca.objects.get(pk=request.POST['id'])
                    mar.estado = False
                    mar.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ="Listado de Marcas"
        context['entity'] = 'Marca'
        context['list_url'] = reverse_lazy('App_Facturacion:marca_list')
        context['count_marca'] = Marca.objects.filter(estado='True').count()
        context['count_ubicacion'] = Bloque.objects.count()+Seccion.objects.count()+Posicion.objects.count()
        context['count_galeria'] = Galeria.objects.count()
        context['date_now'] = datetime.now
        context['form'] = MarcaForm()
        return context

class marca_show_view(DetailView):
    model = Marca
    template_name = 'marca/show.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Información'
        context['entity'] = 'Marca'
        context['date_now'] = datetime.now
        context['count_marca'] = Marca.objects.filter(estado='True').count()
        context['count_ubicacion'] = Bloque.objects.count() + Seccion.objects.count() + Posicion.objects.count()
        context['count_galeria'] = Galeria.objects.count()
        return context
