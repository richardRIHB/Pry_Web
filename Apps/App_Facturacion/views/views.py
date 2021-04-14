from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView

from Apps.App_Facturacion.forms import cliente_form
from Apps.App_Facturacion.models import Cliente

class cliente_view(LoginRequiredMixin, TemplateView):
    template_name = 'cliente/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Cliente.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                with transaction.atomic():
                    formulario = cliente_form(request.POST)
                    if formulario.is_valid():
                        formulario.save()
                    else:
                        data['error'] = formulario.errors
            elif action == 'edit':
                with transaction.atomic():
                    cli = Cliente.objects.get(pk=request.POST['id'])
                    formulario = cliente_form(request.POST, instance=cli)
                    if formulario.is_valid():
                        formulario.save()
                    else:
                        data['error'] = formulario.errors
            elif action == 'delete':
                with transaction.atomic():
                    cli = Cliente.objects.get(pk=request.POST['id'])
                    cli.estado = False
                    cli.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['list_url'] = reverse_lazy('App_Facturacion:cliente_list')
        context['entity'] = 'Clientes'
        context['date_now'] = datetime.now
        context['form'] = cliente_form
        return context

class cliente_show_view(DetailView):
    model = Cliente
    template_name = 'cliente/show.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Información'
        context['entity'] = 'Cliente'
        context['date_now'] = datetime.now
        return context
