from django.urls import path

from .views import StaffListView

urlpatterns = [
    path('', StaffListView.as_view(), name='staff_list'),
    path('<slug:slug>', StaffListView.as_view(), name='sub_staff_category'),
]
