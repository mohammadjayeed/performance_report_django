from django.contrib import admin
from django.urls import path,include
from .views import report_view, delete_view, ReportUpdateView
app_name = 'reports'
urlpatterns = [
    
    path('<str:production_line>/',report_view, name='report-view'),
    path('delete/<pk>/',delete_view, name='delete-view'),
    path('<str:production_line>/<pk>/update/',ReportUpdateView.as_view(), name='update-view'),



]