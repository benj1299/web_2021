from django.forms import Form, CharField, ChoiceField, Select, DecimalField, TextInput
from .models import Operators
from .constants import OPERATORS, GENERATIONS, STATUT, S_OPERATORS

class OperatorsForm(Form):
    operators = ChoiceField(
        required=False,
        choices=[(op, op) for op in OPERATORS],
        widget=Select(attrs={'class':'form-control selector'}),
        label="")
    
    sous_operator = ChoiceField(
        required=False,
        choices=[(op, op) for op in S_OPERATORS],
        widget=Select(attrs={'class':'form-control selector'}),
        label="")

    generation = ChoiceField(
        required=False,
        choices=[(op, op) for op in GENERATIONS],
        widget=Select(attrs={'class':'form-control selector'}),
        label="")

    statut = ChoiceField(
        required=False,
        choices=[(op, op) for op in STATUT],
        widget=Select(attrs={'class':'form-control selector'}),
        label="")

    forfait = DecimalField(required=False, 
        max_digits=4, 
        decimal_places=2, 
        widget=TextInput(attrs={'type': 'range', 'min': '1', 'max': "7w0", "value": "30", "id": 'pricerange', "onchange": "updateTextInput(this.value);"}))