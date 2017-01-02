import django
from django import forms

from app.models import Cbt_students

class RegistrationForm(forms.ModelForm):
 
    class Meta:
        model= Cbt_students
        fields='__all__'

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
                })