from django.urls import path

from Apps.User.views import usuario_list_view, user_perfil_view, user_password_view

app_name = 'user'

urlpatterns = [
    path('usuario/list/', usuario_list_view.as_view(), name='usuario_list'),
    path('perfil/', user_perfil_view.as_view(), name='user_perfil'),
    path('password/', user_password_view.as_view(), name='user_password'),
]