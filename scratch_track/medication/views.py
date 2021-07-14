from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from reports.models import DailyReport
from.models import Ointment, NasalSpray
import datetime
from.classes import MedicalHistoryDays
from.functions import days_between, insertion_sort_medical_history
# Create your views here.



