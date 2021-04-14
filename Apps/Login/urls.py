from django.urls import path

from Apps.Login.views import *

urlpatterns = [
    path('', login_form_view.as_view(), name='login'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', logout_view.as_view(), name='logout')
]
