from .models import Report, ProblemReported
from django import forms

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'

class ProblemReportedForm(forms.ModelForm):
    class Meta:
        model = ProblemReported
        fields = '__all__'