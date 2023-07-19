from django.shortcuts import get_object_or_404, render, redirect
# Create your views here.
from areas.models import ProductionLine

from .forms import *


def report_view(request, production_line):
    form = ReportForm(request.POST or None, production_line= production_line)
    problem_report_form = ProblemReportedForm(request.POST or None)
    queryset = Report.objects.filter(production_line__name = production_line)
    


    
    if "submitbutton1" in request.POST:
        line = get_object_or_404(ProductionLine, name=production_line)


        if form.is_valid():
            
            obj = form.save(commit=False)
            obj.user = request.user
            obj.production_line = line
            obj.save()
            form = ReportForm()
            problem_report_form = ProblemReportedForm()

            # return redirect(request.META.get('HTTP_REFERER'))
        
    elif "submitbutton2" in request.POST:
        r_id = request.POST.get('report_id')
    

        if problem_report_form.is_valid():
            report = Report.objects.get(id= r_id)
            obj = problem_report_form.save(commit=False)
            obj.user = request.user
            obj.report = report
            obj.save()
            form = ReportForm()
            problem_report_form = ProblemReportedForm()
            # return redirect(request.META.get('HTTP_REFERER'))
        
    context = {

        'form':form,
        'problem_report_form':problem_report_form,
        'report_list':queryset
    }

    return render(request, 'reports/report.html', context=context)