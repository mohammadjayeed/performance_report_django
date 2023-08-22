from django.contrib.auth.decorators import login_required
# self made logic
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.edit import FormView

# Create your views here.
from areas.models import ProductionLine
from reports.models import ProblemReported

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile


from .forms import *



def get_problems_in_pdf(request):
    problems = ProblemReported.objects.get_todays_report()

    context = {'problems':problems}

    html_string = render_to_string('reporst/problems.html',context)

    html = HTML(string=html_string)
    result = html.write_pdf()


    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=problem_list.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response




@login_required
def summary_report(request):
    report_qs = None
    try:
        day = request.session.get('day',None)
        line = request.session.get('production_line',None)
        # print(line)
        production_line = ProductionLine.objects.get(id= line)
        qs = Report.objects.get_by_line_and_day(day=day,line=line)
        execution = qs.aggregate_execution()['execution__sum']
        plan = qs.aggregate_plan()['plan__sum']
        problems = ProblemReported.objects.get_report_by_line_and_day(day=day,line=production_line)
        # print(problems)
        
        
    except ObjectDoesNotExist:
        report_qs = Report.objects.none()

    context = {

        'execution': execution,
        'plan':plan,
        'line': production_line,
        'day':day,
        'problems':problems
    }
    return render(request, 'reports/summary.html', context)


class SelectView(FormView):
    template_name = 'reports/select.html'
    form_class = ReportResultForm
    success_url = reverse_lazy('reports:summary-view')

    def form_valid(self, form):
        self.request.session['day'] = self.request.POST.get('day', None)
        self.request.session['production_line'] = self.request.POST.get('production_line', None)
        # print(self.request.session['day'])
        # print(self.request.session['production_line'])
        return super().form_valid(form)
class HomeView(FormView):

    template_name = 'reports/home.html'
    form_class = ReportSelectLineForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request):
        prod_line = self.request.POST.get('prod_line')
        url = reverse('reports:report-view', kwargs={'production_line': prod_line})
        return redirect(url)



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