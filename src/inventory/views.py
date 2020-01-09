from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from inventory.forms import InventoryForm, ApprovalReasonForm
from django.urls import reverse

from inventory.models import Inventory
from user.models import ApprovalRequests


def home(request):
    """
    Function to get home page
    :param request: request received from web server
    :return: renders home
    """
    try:
        is_store_manager = request.user.groups.filter(name='Store Manager').exists()
        items = Inventory.objects.filter(is_deleted=False)
        return render(request, 'home.html', {'items': items, 'is_store_manager': is_store_manager})
    except Exception as e:
        return HttpResponse('Something went wrong')


@login_required
def add_item(request):
    """
    Function used to add item in the inventory
    :param request: request received from web server
    :return: renders home if success
    """
    try:
        is_store_manager = request.user.groups.filter(name='Store Manager').exists()
        if request.method == 'POST':
            approval_form = ApprovalReasonForm(request.POST or None)
            form = InventoryForm(request.POST or None)
            if form.is_valid():
                inventory = form.save(commit=False)
                inventory.created_by = request.user
                inventory.save()
                if not is_store_manager and approval_form.is_valid():
                    approval = ApprovalRequests(requested_user=request.user, inventory=inventory,
                                                reason=approval_form.cleaned_data.get('reason', ''))
                    approval.save()
                else:
                    inventory.status = Inventory.APPROVED
                    inventory.save()
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Something went wrong')
        else:
            form = InventoryForm()
            approval_form = ApprovalReasonForm()
        return render(request, 'inventory.html', {'form': form, 'approval_form': approval_form,
                                                  'is_store_manager': is_store_manager})
    except Exception as e:
        return HttpResponse("Something went wrong")


@login_required
def edit_item(request, item_id):
    """
    Function used to add item in the inventory
    :param request: request received from web server
    :param item_id: current item id
    :return: renders home if success
    """
    try:
        instance = Inventory.objects.get(id=item_id)
        is_store_manager = request.user.groups.filter(name='Store Manager').exists()
        approval_form = ApprovalReasonForm(request.POST or None)
        form = InventoryForm(request.POST or None, instance=instance)
        if request.method == 'POST':
            if form.is_valid():
                inventory = form.save(commit=False)
                inventory.created_by = request.user
                if not is_store_manager and approval_form.is_valid():
                    approval = ApprovalRequests(requested_user=request.user, inventory=instance,
                                                reason=approval_form.cleaned_data.get('reason', ''))
                    approval.save()
                    inventory.status = Inventory.PENDING
                else:
                    inventory.status = Inventory.APPROVED
                inventory.save()
                return HttpResponseRedirect(reverse('home'))
        return render(request, 'inventory.html', {'form': form, 'approval_form': approval_form, 'item': instance,
                                                  'is_store_manager': is_store_manager})
    except Exception as e:
        return HttpResponse("Something went wrong")


@login_required
def delete_item(request, item_id):
    """
    Function used to delete item in the inventory
    :param request: request received from web server
    :param item_id: current item id
    :return: renders home if success
    """
    try:
        inventory = Inventory.objects.get(id=item_id)
        is_store_manager = request.user.groups.filter(name='Store Manager').exists()
        if not is_store_manager:
            approval = ApprovalRequests(requested_user=request.user, inventory=inventory,
                                        reason='Delete Request', is_delete_request=True)
            approval.save()
        else:
            inventory.is_deleted = True
            inventory.save()
        return HttpResponseRedirect(reverse('home'))
    except Exception as e:
        return HttpResponse("Something went wrong")


@login_required
def approve_item(request, item_id):
    """
    Function used to delete item in the inventory
    :param request: request received from web server
    :param item_id: current item id
    :return: renders home if success
    """
    try:
        approval = ApprovalRequests.objects.get(id=item_id, status=ApprovalRequests.PENDING)
        is_store_manager = request.user.groups.filter(name='Store Manager').exists()
        if is_store_manager:
            if approval:
                inventory = Inventory.objects.get(id=approval.inventory_id)
                inventory.status = Inventory.APPROVED
                if approval.is_delete_request:
                    inventory.is_deleted = True
                    inventory.save()
                approval.status = ApprovalRequests.APPROVED
                approval.approved_by = request.user
                approval.save()
        return HttpResponseRedirect(reverse('pending_approval'))
    except Exception as e:
        return HttpResponse("Something went wrong")


@login_required
def pending_approvals(request):
    items = ApprovalRequests.objects.filter(status=ApprovalRequests.PENDING).select_related('inventory',
                                                                                            'requested_user')
    return render(request, 'pending-approvals.html', {'items': items})
