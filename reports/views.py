from django.shortcuts import render
from .forms import *
# Create your views here.
def report_view(request, production_line):
    form = ReportForm()
    problem_report_form = ProblemReportedForm()
    queryset = Report.objects.filter(production_line__name = production_line)

    context = {

        'form':form,
        'problem_report_form':problem_report_form,
        'report_list':queryset
    }

    return render(request, 'reports/report.html', context=context)