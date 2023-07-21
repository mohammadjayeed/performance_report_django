from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
# Create your views here.
from areas.models import ProductionLine
from django.views.generic import UpdateView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView


class HomeView(FormView):

    template_name = 'reports/home.html'
    form_class = ReportSelectLineForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs




class ReportUpdateView(UpdateView):
    

    model = Report
    form_class = ReportForm
    template_name = 'reports/update.html'

    def get(self, request, *args, **kwargs):
        self.custom_value = self.kwargs['production_line']
        # Do something with the parameter value
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'custom_value'):
            kwargs['production_line'] = self.custom_value
        return kwargs


    def get_success_url(self):
        return self.request.path


@login_required
def delete_view(request, *args, **kwargs):
    report_record_number = kwargs.get('pk')
    report = Report.objects.get(id=report_record_number)
    report.delete()

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
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
            # form = ReportForm()
            # problem_report_form = ProblemReportedForm()

            return redirect(request.META.get('HTTP_REFERER'))
        
    elif "submitbutton2" in request.POST:
        r_id = request.POST.get('report_id')
    

        if problem_report_form.is_valid():
            report = Report.objects.get(id= r_id)
            obj = problem_report_form.save(commit=False)
            obj.user = request.user
            obj.report = report
            obj.save()
            # form = ReportForm()
            # problem_report_form = ProblemReportedForm()
            return redirect(request.META.get('HTTP_REFERER'))
        
    context = {

        'form':form,
        'problem_report_form':problem_report_form,
        'report_list':queryset
    }

    return render(request, 'reports/report.html', context=context)