from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.forms import model_to_dict

from Pry_Web.settings import MEDIA_URL, STATIC_URL


class User(AbstractUser):
    imagen = models.ImageField(upload_to='users/%Y/%m/%d',null=True,blank=True)

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['groups', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['imagen'] = self.get_image()
        return item

#    def save(self, *args, **kwargs):
 #       if self.pk is None:
  #          self.set_password(self.password)
   #     else:
    #        user = User.objects.get(pk=self.pk)
     #       if user.password != self.password:
      #          self.set_password(self.password)
       # super().save(*args, **kwargs)