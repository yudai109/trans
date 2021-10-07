from django.urls import path
from trans_scraip import views

# app_name= 'trans_scraip'

urlpatterns = [
    path('', views.kddi_trance, name='kddi_trance'),
    path('import/', views.csvimport, name='csvimport'),
    path('export/', views.csvexport, name='csvexport'),
    path('transdata/', views.transdata, name='transdata'),
    path('back/', views.deleteData_all, name='deleteData_all'),
]

