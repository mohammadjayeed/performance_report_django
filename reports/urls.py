from django.contrib import admin
from django.urls import path,include
from .views import report_view, delete_view, ReportUpdateView, HomeView, SelectView, summary_report, get_problems_in_pdf

app_name = 'reports'

urlpatterns = [
    path('',HomeView.as_view(), name='home-view'),
    path('reports/',SelectView.as_view(), name='select-view'),
    path('reports/summary/',summary_report, name='summary-view'),
    path('reports/<str:production_line>/',report_view, name='report-view'),
    path('reports/delete/<pk>/',delete_view, name='delete-view'),
    path('reports/<str:production_line>/<pk>/update/',ReportUpdateView.as_view(), name='update-view'),
    path('reports/generate/pdf/',get_problems_in_pdf, name='pdf'),
]