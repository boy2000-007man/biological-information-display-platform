from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile


class MyProfile(UserenaBaseProfile):
    
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')

    
    first_name = models.CharField(_('first_name'),
                                 max_length=15)

    last_name = models.CharField(_('Last_name'),
                                 max_length=15)

    school = models.CharField(_('Your School'),
    	                         max_length=15)

    age = models.CharField(_('Your age'),
    	                     max_length=2)
