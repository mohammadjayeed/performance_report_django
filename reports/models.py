from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User
from products.models import Product
from areas.models import ProductionLine
from category.models import Category
from django.urls import reverse
from django.db.models import Sum
import datetime
hours = ([(str(x),str(x)) for x in range(1,25)])
import random

el = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
     'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]



class ReportQueryset(models.QuerySet):

    def get_by_line_and_day(self, day, line):
        return Report.objects.filter(day=day, production_line__id = line)

    def aggregate_execution(self):
        return self.aggregate(Sum('execution'))

    def aggregate_plan(self):
        return self.aggregate(Sum('plan'))

class ReportManager(models.Manager):

    def get_queryset(self):
        return ReportQueryset(self.model, using=self._db)

    def get_by_line_and_day(self, day, line):
        return self.get_queryset().get_by_line_and_day(day,line)
    
    def aggregate_execution(self):
        return self.get_queryset.aggregate_execution()

    def aggregate_plan(self):
        return self.get_queryset.aggregate_plan()


# Create your models here.
class Report(models.Model):
    day = models.DateField(default=timezone.now)
    start_hour = models.CharField(max_length=2, choices=hours)
    end_hour = models.CharField(max_length=2, choices=hours)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.PositiveIntegerField()
    execution = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    production_line = models.ForeignKey(ProductionLine,on_delete=models.CASCADE, related_name='pl')

    objects = ReportManager()
    def get_day(self):
        return self.day.strftime('%d/%m/%Y')
    
    def get_absolute_url(self):
        return reverse('reports:update-view',kwargs={'production_line':self.production_line,'pk':self.pk})

    def __str__(self):
        return f"{self.start_hour} {self.end_hour} {self.production_line}"
    
    class Meta:
        ordering = ('-created_at',)


def random_code():
    random.shuffle(el)
    code = [str(x) for x in el[:12]]
    str_code = ''.join(code)

    return str_code


class ProblemReportedManager(models.Manager):
    def get_report_by_line_and_day(self, day, line):
        return super().get_queryset().filter(report__day = day, report__production_line__name = line)

    def get_todays_report():
        today = datetime.now().strftime('%Y-%m-%d')
        return super().get_queryset().filter(report__day=today)

class ProblemReported(models.Model):

    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    problem_id = models.CharField(max_length=12, unique=True, blank=True, default=random_code)
    breakdown = models.SmallIntegerField()
    public = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    objects = ProblemReportedManager()

    def __str__(self):
        return self.category.name

    class Meta:
        verbose_name = 'Problem Reported'
        verbose_name_plural = 'Problems Reported'