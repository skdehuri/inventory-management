from django.contrib.auth.models import User
from django.db import models
from inventory.models import Inventory


class ApprovalRequests(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
