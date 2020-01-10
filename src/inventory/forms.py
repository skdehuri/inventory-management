from django import forms

from inventory.models import Inventory
from user.models import ApprovalRequests


class InventoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}))
    vendor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    batch_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    batch_date = forms.CharField(widget=forms.DateInput(format="%Y-%m-%d", attrs={'placeholder': 'YYYY-MM-DD',
                                                                                  'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Inventory
        fields = ['name', 'vendor', 'price', 'batch_number', 'batch_date', 'quantity']


class ApprovalReasonForm(forms.ModelForm):
    reason = forms.Textarea(attrs={'required': True, 'class': 'form-control'})

    class Meta:
        model = ApprovalRequests
        fields = ['reason']
        labels = {'reason': 'Reason For Change'}
