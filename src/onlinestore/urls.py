"""onlinestore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from user.views import login, logout
from inventory.views import add_item, edit_item, delete_item, home, pending_approvals, approve_item

urlpatterns = [
    path('', home, name='home'),
    path('admin', admin.site.urls),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('pending-approval', pending_approvals, name='pending_approval'),
    path('item/add', add_item, name='add_item'),
    re_path(r'item/delete/(?P<item_id>\d+)', delete_item, name='delete_item'),
    re_path(r'item/edit/(?P<item_id>\d+)', edit_item, name='edit_item'),
    re_path(r'item/approve/(?P<item_id>\d+)', approve_item, name='approve_item'),
]


