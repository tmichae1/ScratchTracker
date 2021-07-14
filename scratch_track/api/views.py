from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from scratch.models import Scratch, NightScratch, DailyScratchCount
from medication.models import Ointment, NasalSpray
from reports.models import DailyReport, MedicalReportDailyScores
from medication.functions import days_between, insertion_sort_medical_history
from.serializer import StatsSerializer, MedicalHistoryDaysSerializer, DailyScratchSerializer, DailyMedicalScoreSerializer, NightScratchScoreSerializer
from .classes import Stats, MedicalHistoryDays
from .functions import get_medical_scores
import datetime


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_stats(request):
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    today = datetime.date.today()
    last_month = today.replace(day=1) - datetime.timedelta(days=1)
    today_time = datetime.datetime.now().time()

    #   Scratch stats
    all_scratches = list()
    total_days = 7
    for i in range(1, 8):
        scratches = Scratch.objects.filter(user=request.user, date=today - datetime.timedelta(days=i)).order_by("time")
        if scratches is None:
            total_days -= 1
        else:
            for scratch in scratches:
                if scratch.time <= today_time:
                    all_scratches.append(scratch)
                else:
                    break
    today_total = len(Scratch.objects.filter(user=request.user, date=today))

    #   Average scratches for current month
    current_month_scratch_count = DailyScratchCount.objects.filter(user=request.user, date__month=today.month, date__year=today.year).exclude(date__day=today.day).order_by("date")
    total = 0
    if len(current_month_scratch_count) > 0:
        for day in current_month_scratch_count:
            total += day.total
        current_month_scratch_count = round(total / (today.day -1))
    else:
        current_month_scratch_count = 0

    #   Average scratches for last month
    last_month_scratch_count = DailyScratchCount.objects.filter(user=request.user, date__month=last_month.month, date__year=last_month.year).order_by("date")
    last_month_total = 0
    if last_month_scratch_count:
        for day in last_month_scratch_count:
            last_month_total += day.total
        if last_month_scratch_count[0].date.day == 1:
            last_month_scratch_count = round(last_month_total / month_days[last_month.month - 1])
        else:
            last_month_scratch_count = round(last_month_total / (month_days[last_month.month - 1] - (last_month_scratch_count[0].date.day -1)))
    else:
        last_month_scratch_count = 0
    #   NightPoints stats
    #   Current Month
    night_scratches = NightScratch.objects.filter(user=request.user, date__month=today.month, date__year=today.year).order_by("date")
    current_month_avg = 0.00
    if night_scratches:
        night_scratch_date = datetime.date.today()
        for scratch in night_scratches:
            current_month_avg += scratch.points
        current_month_avg = round(current_month_avg / (night_scratch_date.day - 1), 1)
    else:
        current_month_avg = -1.0
    #   Last Month
    night_scratches = NightScratch.objects.filter(user=request.user, date__month=last_month.month, date__year=last_month.year).order_by("date")
    last_month_avg = 0.00
    if night_scratches:
        for scratch in night_scratches:
            last_month_avg += scratch.points
        #   if first entry fo night scratch was the 1st, divide by total days in month
        if night_scratches[0].date.day == 1:
            last_month_avg = round(last_month_avg / month_days[last_month.month - 1], 1)
        #   if first entry is not the 1st, divide by total days from first entry
        else:
            last_month_avg = round(last_month_avg / (month_days[last_month.month - 1] - (night_scratches[0].date.day - 1)), 1)
    else:
        last_month_avg = -1.0

    # #   Medical Scores
    # reports = []
    # #   get last month and this month reports and append them to a list
    #
    # last_month = today.replace(day=1) - datetime.timedelta(days=1)
    # month_before_last = last_month.replace(day=1) - datetime.timedelta(days=1)
    # #   month before last
    # reports_month_before_last = DailyReport.objects.filter(user=request.user, date__month=month_before_last.month, date__year=month_before_last.year).order_by('date')
    # for report in reports_month_before_last:
    #     reports.append(report)
    # #   last month
    # reports_last_month = DailyReport.objects.filter(user=request.user, date__month=last_month.month, date__year=last_month.year).order_by('date')
    # for report in reports_last_month:
    #     reports.append(report)
    # #   current month
    # reports_this_month = DailyReport.objects.filter(user=request.user, date__month=today.month, date__year=today.year).exclude(date__day=today.day).order_by('date')
    # for report in reports_this_month:
    #     reports.append(report)
    scores = get_medical_scores(request)
    this_month_score = scores[0]
    last_month_score = scores[1]
    stats = Stats(weekly_avg_time=round(len(all_scratches) / total_days),
                  daily_total=today_total,
                  scratch_avg_current_month=current_month_scratch_count,
                  scratch_avg_last_month=last_month_scratch_count,
                  night_points_current_month=current_month_avg,
                  night_points_last_month=last_month_avg,
                  medical_score_current_month=this_month_score,
                  medical_score_last_month=last_month_score
                  )
    serializer = StatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_medical_history_days(request):
    medical_history = list()
    # Ointment intake
    ointments = Ointment.objects.all()
    for ointment in ointments:
        last_used = DailyReport.objects.filter(user=request.user, ointment_used=ointment.id).order_by("date").last()
        if last_used:
            days = days_between(last_used.date)
            medication = MedicalHistoryDays(ointment.name, days)
            medical_history.append(medication)

    # Nasal spray intake

    last_used = DailyReport.objects.filter(user=request.user, nasal_spray_used__isnull=False).order_by("date").last()
    if last_used:
        days = days_between(last_used.date)
        medication = MedicalHistoryDays("Nasal Spray", days)
        medical_history.append(medication)

    # Steroid and tablet intake
    all_reports = DailyReport.objects.filter(user=request.user).order_by("-date")

    # for antihistamine_120mg
    for report in all_reports:
        if report.antihistamine_120mg > 0:
            days = days_between(report.date)
            medication = MedicalHistoryDays("Antihistamine 120mg", days)
            medical_history.append(medication)
            break

    #     # for steroid tablet
    for report in all_reports:
        if report.steroid_tablet > 0:
            days = days_between(report.date)
            medication = MedicalHistoryDays("Steroid Tablet", days)
            medical_history.append(medication)
            break

    #     # for inhaler tablet
    for report in all_reports:
        if report.inhaler > 0:
            days = days_between(report.date)
            medication = MedicalHistoryDays("Inhaler", days)
            medical_history.append(medication)
            break

    scalp = DailyReport.objects.filter(user=request.user, scalp_steroid=True).order_by("date").last()
    if scalp:
        days = days_between(scalp.date)
        medication = MedicalHistoryDays("Scalp Steroid", days)
        medical_history.append(medication)
    insertion_sort_medical_history(medical_history)
    serializer = MedicalHistoryDaysSerializer(medical_history, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_daily_scratch_counts(request, date):
    wanted_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    print(type(wanted_date))
    scratches = DailyScratchCount.objects.filter(user=request.user, date__month = wanted_date.month, date__year = wanted_date.year).order_by("date")
    serializer = DailyScratchSerializer(scratches, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_daily_medical_scores(request, date):
    wanted_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    report_scores = MedicalReportDailyScores.objects.filter(user=request.user, date__month = wanted_date.month, date__year = wanted_date.year).order_by("date")
    serializer = DailyMedicalScoreSerializer(report_scores, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_night_scratch_scores(request, date):
    wanted_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    night_scores = NightScratch.objects.filter(user=request.user, date__month = wanted_date.month, date__year = wanted_date.year).order_by("date")
    serializer = NightScratchScoreSerializer(night_scores, many=True)
    return Response(serializer.data)



