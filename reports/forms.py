from .models import Report, ProblemReported
from django import forms
from django.shortcuts import get_object_or_404
from areas.models import ProductionLine


class ReportResultForm(forms.Form):
    production_line = forms.ModelChoiceField(queryset=ProductionLine.objects.all())
    date = forms.CharField(widget=forms.DateTimeInput(

        attrs={'class':'datepicker'}

    ))
class ReportSelectLineForm(forms.Form):
    production_line = forms.ModelChoiceField(queryset=ProductionLine.objects.none(), label='')

    def __init__(self,user,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['production_line'].queryset = ProductionLine.objects.filter(team_lead__user__username = user)


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        exclude = ('user','production_line',)

    def __init__(self, *args, **kwargs):
        production_line = kwargs.pop('production_line',None)
        super().__init__(*args, **kwargs)
        if production_line is not None:
            line = get_object_or_404(ProductionLine, name = production_line)
            self.fields['product'].queryset = line.product.all()
            




class ProblemReportedForm(forms.ModelForm):
    class Meta:
        model = ProblemReported
        exclude = ('user','report','problem_id')