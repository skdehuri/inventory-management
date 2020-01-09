from django.contrib.auth.models import User
from django.db import models
from inventory.models import Inventory


class ApprovalRequests(models.Model):
    PENDING = 1
    APPROVED = 2
    STATUS_CHOICES = (
        (PENDING, 'PENDING'),
        (APPROVED, 'APPROVED'),
    )

    id = models.AutoField(primary_key=True)
    requested_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_user')
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='approved_by')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    reason = models.TextField()
    last_update_time = models.DateTimeField(auto_now=True)
    is_delete_request = models.BooleanField(default=False)
