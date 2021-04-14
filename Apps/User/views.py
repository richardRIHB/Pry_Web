from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, TemplateView, FormView
from datetime import datetime

from Apps.User.forms import user_form, UserProfileForm
from Apps.User.models import User
from Apps.App_Facturacion.mixins import IsSuperuserMixin

class usuario_list_view(LoginRequiredMixin, IsSuperuserMixin, TemplateView):
    template_name = 'user/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                pk1 = self.request.user.pk
                data = []
                for i in User.objects.filter().exclude(pk=pk1):
                    data.append(i.toJSON())
            elif action == 'add':
                with transaction.atomic():
                    form = user_form(request.POST)
                    if form.is_valid():
                        imagen = ''
                        if request.FILES:
                            imagen = request.FILES['imagen']
                        nuevo_usuario = User(
                            username=form.cleaned_data.get('username'),
                            first_name=form.cleaned_data.get('first_name'),
                            last_name=form.cleaned_data.get('last_name'),
                            email=form.cleaned_data.get('email'),
                            imagen=imagen,
                            is_active=form.cleaned_data.get('is_active')
                        )
                        nuevo_usuario.set_password(form.cleaned_data.get('password'))
                        nuevo_usuario.save()
                    else:
                        data['error'] = form.errors
            elif action == 'edit':
                with transaction.atomic():
                    usu = User.objects.get(pk=request.POST['id'])
                    form = user_form(request.POST, request.FILES or None, instance=usu)
                    if form.is_valid():
                        form.save()
                    else:
                        data['error'] = form.errors
            elif action == 'delete':
                with transaction.atomic():
                    usu = User.objects.get(pk=request.POST['id'])
                    usu.is_active = False
                    usu.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de usuarios"
        context['entity'] = 'Usuario'
        context['list_url'] = reverse_lazy('user:usuario_list')
        context['date_now'] = datetime.now
        context['form'] = user_form()
        return context

class user_perfil_view(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'user/perfil.html'
    success_url = reverse_lazy('App_Facturacion:dashboard')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                with transaction.atomic():
                    form = self.get_form()
                    data = form.save()
                    if data:
                        print('error')
                    else:
                        pk1 = self.request.user.pk
                        usu = User.objects.get(pk=pk1)
                        if request.FILES:
                            usu.imagen = request.FILES['imagen']
                            usu.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Perfil'
        context['entity'] = 'Perfil'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class user_password_view(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/password.html'
    success_url = reverse_lazy('login')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su contraseña'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Password'
        context['entity'] = 'Password'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

