from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from django.contrib.auth.models import Group


class BaseRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )

#    def save(self, request):
#        user = super(BaseRegisterForm, self).save(request)
#        basic_group = Group.objects.get(name='common')
#        basic_group.user_set.add(user)
#        return user


