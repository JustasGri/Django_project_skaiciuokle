from collections import namedtuple
from .models import Veikla, Uzdarbis
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.bootstrap import InlineRadios


class VeiklaForm(forms.ModelForm):

    PENSIJA_STATUS = (
        ('p24', 'Pensija 2.4%'),
        ('p3', 'Pensija 3%'),
        ('pn', 'Nekaupiama'),

    )

    ISLAIDOS_STATUS = (
        ('i30', 'Išlaidos 30%'),
        ('isf', 'Faktinės išlaidos'),
    )

    pavadinimas = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Pavadinimas'}))
    status = forms.ChoiceField(widget=forms.RadioSelect(choices=PENSIJA_STATUS))
    status2 = forms.CharField(widget=forms.RadioSelect(choices=ISLAIDOS_STATUS))


class UzdarbisForm(forms.ModelForm):
    pajamos = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    islaidos = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'value':0}))
    
    class Meta:
        model = Uzdarbis
        fields = ['pajamos', 'islaidos']
    
    

    
    

