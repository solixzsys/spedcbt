"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.forms.utils import ValidationError
from app.models import Cbt_students
class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    error_messages={'invalid_login':_('Re-Check You Matric Number !!!'),}

    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    matricnumber = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Matric Number'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
    def clean_matricnumber(self):
        print('clean_matricnumber.....................................',self.cleaned_data['matricnumber'])
        try:
            student=Cbt_students.objects.get(matricnumber= self.cleaned_data['matricnumber'])
            if student.username != self.cleaned_data['username']:
                 raise  ValidationError(self.error_messages['invalid_login'])
        except Exception as e:
            print(e)
            raise ValidationError(self.error_messages['invalid_login'])
        
        return self.cleaned_data['matricnumber']