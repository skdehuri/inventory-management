from django import forms

from inventory.models import Inventory
from user.models import ApprovalRequests


class InventoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'required': True}))
    vendor = forms.CharField()
    price = forms.NumberInput()
    batch_number = forms.NumberInput()
    batch_date = forms.CharField(widget=forms.DateInput(format="%Y-%m-%d", attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Inventory
        fields = ['name', 'vendor', 'price', 'batch_number', 'batch_date', 'quantity']


class ApprovalReasonForm(forms.ModelForm):
    reason = forms.Textarea(attrs={'required': True})

    class Meta:
        model = ApprovalRequests
        fields = ['reason']
        labels = {'reason': 'Reason For Change'}
