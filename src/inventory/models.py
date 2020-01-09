from django.contrib.auth.models import User
from django.db import models


class Inventory(models.Model):
    PENDING = 1
    APPROVED = 2
    STATUS_CHOICES = (
        (PENDING, 'PENDING'),
        (APPROVED, 'APPROVED'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    batch_number = models.IntegerField(null=True, blank=True)
    batch_date = models.DateField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    creation_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    last_update_time = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by', null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

