from django.shortcuts import render
from .forms import *
# Create your views here.
def report_view(request):
    form = ReportForm()
    problem_report_form = ProblemReportedForm()

    context = {

        'form':form,
        'problem_report_form':problem_report_form
    }

    return render(request, 'reports/report.html', context=context)