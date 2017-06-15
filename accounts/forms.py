from django import forms

from userena.forms import AuthenticationForm

class SigninForm(AuthenticationForm):
    identification = forms.CharField(
        label = "Email or username",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "required",
                "data-bv-notempty": "true",
                "data-bv-notempty-message": "Email or username is required"
            }
        )
    )
    
    password = forms.CharField(
        label = "Password",
        widget=forms.PasswordInput(
            attrs = {
                "class": "form-control",
                "placeholder": "required",
                "data-bv-notempty": "true",
                "data-bv-notempty-message": "Password is required"
            }
        )
    )

from django.utils.translation import ugettext_lazy as _
from userena.forms import SignupForm

from collections import OrderedDict
attrs_dict = {
    'class': 'required form-control',
    "placeholder": "required",
    "data-bv-notempty": "true",
}
USERNAME_RE = r'^[\.\w]+$'
class SignupFormExtra(SignupForm):
        
    username = forms.RegexField(regex=USERNAME_RE,
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _('Username must contain only letters, numbers, dots and underscores.')})
                                
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("Email"))
                             
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Create password"))
                                
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Repeat password"))
                                
    first_name = forms.CharField(label=_(u'First name'),
                                 widget=forms.TextInput(attrs=attrs_dict),
                                 max_length=30,
                                 required=False)

    last_name = forms.CharField(label=_(u'Last name'),
                                widget=forms.TextInput(attrs=attrs_dict),
                                max_length=30,
                                required=False)

    Age = forms.CharField(label=_(u'Age'),
                         widget=forms.TextInput(attrs=attrs_dict),
                         max_length=2,
                         required=True)

    school = forms.CharField(label=_(u'School'),
                              widget=forms.TextInput(attrs=attrs_dict),
                              max_length=15,
                              required=True)

    def __init__(self, *args, **kw):
        """

        A bit of hackery to get the first name and last name at the top of the
        form instead at the end.

        """
        super(SignupFormExtra, self).__init__(*args, **kw)
        # Put the first and last name at the top
        new_order = self.fields.keyOrder[:-4]
        new_order.insert(0, 'first_name')
        new_order.insert(1, 'last_name')
        new_order.insert(2, 'Age')
        new_order.insert(3, 'school')
        self.fields.keyOrder = new_order

    def save(self):
        """
        Override the save method to save the first and last name to the user
        field.

        """
        # First save the parent form and get the user.
        new_user = super(SignupFormExtra, self).save()

        # Get the profile, the `save` method above creates a profile for each
        # user because it calls the manager method `create_user`.
        # See: https://github.com/bread-and-pepper/django-userena/blob/master/userena/managers.py#L65
        user_profile = new_user.get_profile()

        user_profile.first_name = self.cleaned_data['first_name']
        user_profile.last_name = self.cleaned_data['last_name']
        user_profile.age = self.cleaned_data['Age']
        user_profile.school = self.cleaned_data['school']
        user_profile.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user
