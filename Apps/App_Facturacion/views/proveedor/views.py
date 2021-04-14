from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView

from Apps.App_Facturacion.forms import proveedor_form
from Apps.App_Facturacion.models import Proveedor

class proveedor_view(LoginRequiredMixin, TemplateView):
    template_name = 'proveedor/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Proveedor.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                with transaction.atomic():
                    formulario = proveedor_form(request.POST, request.FILES or None)
                    if formulario.is_valid():
                        formulario.save()
                    else:
                        data['error'] = formulario.errors
            elif action == 'edit':
                with transaction.atomic():
                    prov = Proveedor.objects.get(pk=request.POST['id'])
                    formulario = proveedor_form(request.POST, request.FILES or None, instance=prov)
                    if formulario.is_valid():
                        formulario.save()
                    else:
                        data['error'] = formulario.errors
            elif action == 'delete':
                with transaction.atomic():
                    prov = Proveedor.objects.get(pk=request.POST['id'])
                    prov.estado = False
                    prov.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proveedores'
        context['list_url'] = reverse_lazy('App_Facturacion:proveedor_list')
        context['entity'] = 'Proveedores'
        context['date_now'] = datetime.now
        context['form'] = proveedor_form
        return context

class proveedor_show_view(DetailView):
    model = Proveedor
    template_name = 'proveedor/show.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Información'
        context['entity'] = 'Proveedor'
        context['date_now'] = datetime.now
        return context