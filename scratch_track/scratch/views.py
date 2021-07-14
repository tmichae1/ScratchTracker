from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import Scratch, DailyScratchCount, NightScratch, NightScratchMonthlyAvg, ScratchMonthlyAvg
from.functions import get_daily_score
from rest_framework.authtoken.models import Token
from.forms import NightScratchForm, AddScratchForm
from django.utils.safestring import mark_safe
from reports.models import MedicalReportScores, DailyReport
from api.functions import get_medical_scores
from django.contrib import messages
import datetime


# Create your views here.


@login_required
def scratch(request):
    template_name = "scratch/scratch.html"
    if request.user.is_authenticated:
        token = Token.objects.filter(user=request.user).first()
        context = {'token': token
                   }
    else:
        context = {}
    last_month = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
    last_month_last = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)

    medical_score_last_month = MedicalReportScores.objects.filter(user=request.user, date=last_month).first()
    #   check if last months medical score has not already been added
    if not medical_score_last_month:
        print("yes")
        scores = get_medical_scores(request)
        last_month_score = scores[1]
        #   create a new entry for medical report scores and save it
        new_score = MedicalReportScores(user=request.user, date=last_month, score=last_month_score)
        new_score.save()
    yesterday_date = datetime.date.today() - datetime.timedelta(days=1)
    get_daily_score(request, yesterday_date)

    #   Check if NightScoreAvg was added for last month, if not, add it
    night_scratch_avg_last_month = NightScratchMonthlyAvg.objects.filter(user=request.user, date=last_month).first()
    if not night_scratch_avg_last_month:
        score = 0
        nights_scores = NightScratch.objects.filter(user=request.user, date__month=last_month.month, date__year=last_month.year).order_by("date")
        for scores in nights_scores:
            score += scores.points
        if nights_scores:
            #   if first entry fo night scratch was the 1st, divide by total days in month
            if nights_scores[0].date.day == 1:
                score = round(score / last_month_last.day, 1)
            #   if first entry is not the 1st, divide by total days from first entry
            else:
                score = round(score / (last_month_last.day - (nights_scores[0].date.day - 1)), 1)
        new_avg_nightscore = NightScratchMonthlyAvg(user=request.user, date=last_month, points=score)
        new_avg_nightscore.save()

    #   Check if scratchMonthlyAvg has been added, if not, add it
    scratch_monthly_avg = ScratchMonthlyAvg.objects.filter(user=request.user, date=last_month).first()
    if not scratch_monthly_avg:
        total = 0
        scratches = DailyScratchCount.objects.filter(user=request.user, date__month=last_month.month, date__year=last_month.year)
        for x in scratches:
            total += x.total
        total = round(total / last_month_last.day)
        new_scratch_monthly_avg = ScratchMonthlyAvg(user=request.user, date=last_month, total=total)
        new_scratch_monthly_avg.save()
    # else:
    #     total = 0
    #     scratches = DailyScratchCount.objects.filter(user=request.user, date__month=last_month.month, date__year=last_month.year)
    #     for x in scratches:
    #         total += x.total
    #     if total != scratch_monthly_avg.total:
    #         scratch_monthly_avg.total = total
    #         scratch_monthly_avg.save()

    return render(request, template_name, context)


@login_required
def add_scratch(request):
    date = datetime.datetime.now()
    time = date.time()
    user_scratch = Scratch(user=request.user, date=date, time=time)
    user_scratch.save()
    daily_scratch_count, created = DailyScratchCount.objects.get_or_create(user=request.user, date=date,
                                                                           defaults={'total': 0})
    if daily_scratch_count:
        daily_scratch_count.total += 1
        daily_scratch_count.save()
    if daily_scratch_count.total == 1:
        messages.warning(request, mark_safe("Have you input your night score for last night? <a href='night/nightly-scratch-/'><strong>Do it Now</strong></a>"))
    return redirect('scratch-home')


@login_required
def night_scratch(request):
    template_name = "scratch/night_scratch.html"
    last_month = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
    if request.method == "POST":
        form = NightScratchForm(request.POST)
        if form.is_valid():
            if NightScratch.objects.filter(user=request.user, date=form.instance.date).first():
                messages.error(request, "Night Scratches already recorded for {0}".format(form.instance.date.strftime("%d/%m/%Y")))
                return redirect("night-scratch")
            form.instance.user = request.user
            if form.instance.time_of_10th_scratch == "before 12am":
                form.instance.points = 0
            elif form.instance.time_of_10th_scratch == "between 12am and 1am":
                form.instance.points = 1
            elif form.instance.time_of_10th_scratch == "between 1am and 2am":
                form.instance.points = 2
            else:
                form.instance.points = 3
            form.save()
            #   if night_scratch added was from last month, we must update the avg night score
            if form.instance.date.month == last_month.month and form.instance.date.year == last_month.year:
                night_scratch_avg_last_month = NightScratchMonthlyAvg.objects.filter(user=request.user, date=last_month).first()
                if night_scratch_avg_last_month:
                    last_month_last = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
                    score = 0
                    nights_scores = NightScratch.objects.filter(user=request.user, date__month=last_month.month, date__year=last_month.year).order_by("date")
                    for scores in nights_scores:
                        score += scores.points
                    if nights_scores[0].date.day == 1:
                        score = round(score / last_month_last.day, 1)
                        #   if first entry is not the 1st, divide by total days from first entry
                    else:
                        score = round(score / (last_month_last.day - (nights_scores[0].date.day - 1)), 1)
                    if score != night_scratch_avg_last_month.points:
                        night_scratch_avg_last_month.points = score
                        night_scratch_avg_last_month.save()

            messages.success(request, "Night Scratches Recorded")
            return redirect('scratch-home')
    else:
        form = NightScratchForm(initial={'date': datetime.datetime.today() - datetime.timedelta(days=1)})
    context = {"form": form}
    return render(request, template_name, context)


@login_required
def update_night_scratch(request, date):
    template_name = "scratch/night_scratch.html"
    last_month = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
    report = get_object_or_404(NightScratch, date=date, user=request.user)
    if request.method == "POST":
        form = NightScratchForm(request.POST, instance=report)
        if form.is_valid():
            if form.instance.time_of_10th_scratch == "before 12am":
                form.instance.points = 0
            elif form.instance.time_of_10th_scratch == "between 12am and 1am":
                form.instance.points = 1
            elif form.instance.time_of_10th_scratch == "between 1am and 2am":
                form.instance.points = 2
            else:
                form.instance.points = 3
            form.save()
            #   if night_Scratch that is updated is from last month, we must update the avg night score
            if form.instance.date.month == last_month.month and form.instance.date.year == last_month.year:
                night_scratch_avg_last_month = NightScratchMonthlyAvg.objects.filter(user=request.user, date=last_month).first()
                if night_scratch_avg_last_month:
                    last_month_last = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
                    score = 0
                    nights_scores = NightScratch.objects.filter(user=request.user, date__month=last_month.month, date__year=last_month.year).order_by("date")
                    for scores in nights_scores:
                        score += scores.points
                    if nights_scores[0].date.day == 1:
                        score = round(score / last_month_last.day, 1)
                        #   if first entry is not the 1st, divide by total days from first entry
                    else:
                        score = round(score / (last_month_last.day - (nights_scores[0].date.day - 1)), 1)
                    if score != night_scratch_avg_last_month.points:
                        night_scratch_avg_last_month.points = score
                        night_scratch_avg_last_month.save()
            messages.success(request, "Night Scratches updated successfully")
            return redirect('get-report', date=date)
    else:
        form = NightScratchForm(instance=report)
    context = {"form": form}
    return render(request, template_name, context)


@login_required
def night_scratch_exists(request):
    template_name = "scratch/night_scratch_exists.html"
    if NightScratch.objects.filter(user=request.user, date=datetime.datetime.today() - datetime.timedelta(days=1)):
        return render(request, template_name)
    return redirect("night-scratch")


#   Extra view to manually add scratch if missed
def add_missed_scratch(request, date):
    template_name = "scratch/update_scratch.html"
    last_month = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
    last_month_last = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    if request.method == 'POST':
        form = AddScratchForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            daily_scratch_count, created = DailyScratchCount.objects.get_or_create(user=request.user, date=date,
                                                                                   defaults={'total': 0})
            if daily_scratch_count:
                daily_scratch_count.total += 1
                daily_scratch_count.save()
            form.save()
            #   if missed scratch is from last month, we must update the avg scratches from last month
            if form.instance.date.month == last_month.month and form.instance.date.year == last_month.year:
                scratch_monthly_avg = ScratchMonthlyAvg.objects.filter(user=request.user, date=last_month).first()
                if scratch_monthly_avg:
                    total = 0
                    scratches = DailyScratchCount.objects.filter(user=request.user, date__month=last_month.month, date__year=last_month.year)
                    for x in scratches:
                        total += x.total
                    total = round(total / last_month_last.day)
                    if total != scratch_monthly_avg.total:
                        scratch_monthly_avg.total = total
                        scratch_monthly_avg.save()

            messages.success(request, "Scratch successfully added")
            return redirect('add-missed-scratch', date=date)
    else:
        form = AddScratchForm(initial={"date": date})
    context = {"form": form}
    return render(request, template_name, context)