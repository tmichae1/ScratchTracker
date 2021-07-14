from django.shortcuts import render, redirect, get_object_or_404
from .forms import DailyReportForm
from.models import DailyReport, MedicalReportScores, MedicalReportDailyScores
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from scratch.models import DailyScratchCount, NightScratch, NightScratchMonthlyAvg, ScratchMonthlyAvg
from scratch.functions import get_daily_score
from django.core.paginator import Paginator
import datetime
from api.functions import get_medical_scores
from reports.models import MedicalReportScores, MedicalReportDailyScores

# Create your views here.

@login_required
def add_daily_report(request):
    template_name = 'reports/add_daily_report.html'
    if request.method == 'POST':
        form = DailyReportForm(request.POST)
        last_month_date = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        if form.is_valid():
            # Check to see if report has already been made for selected date, if so alert
            # user and redirect them back to report screen
            if DailyReport.objects.filter(user=request.user, date=form.instance.date).first():
                messages.warning(request, "Report already added for {0}".format(form.instance.date.strftime("%d/%m/%Y")))
                return redirect('add-daily-report')
            # Assign form values to save to model
            form.instance.user = request.user
            if form.instance.nasal_spray_used is None:
                form.instance.nostril_used = None
            if form.instance.nasal_spray_used and form.instance.nostril_used is None:
                form.instance.nostril_used = "both"
            if form.instance.antihistamine_120mg is None:
                form.instance.antihistamine_120mg = 0
            if form.instance.steroid_tablet is None:
                form.instance.steroid_tablet = 0
            if form.instance.inhaler is None:
                form.instance.inhaler = 0
            form.save()
            # Check to see if any scratches have taken place on selected date. if not, create a daily scratch instance
            # and set it to 0
            if DailyScratchCount.objects.filter(user=request.user, date=form.instance.date).first() is None:
                date = form.instance.date
                daily_scratch = DailyScratchCount(user=request.user, date=date, total=0)
                daily_scratch.save()
            messages.success(request, "Report added")
            # CHeck if selected date for for previous month, if so, last month medical score must be updated
            if form.instance.date.month == last_month_date.month and form.instance.date.year == last_month_date.year:
                scores = get_medical_scores(request)
                last_month_scores = MedicalReportScores.objects.filter(user=request.user, date = last_month_date).first()
                if last_month_scores:
                    if last_month_scores.score != scores[1]:
                        last_month_scores.score = scores[1]
                        last_month_scores.save()
            get_daily_score(request, form.instance.date)
            return redirect('scratch-home')
    else:
        report = DailyReport.objects.filter(user=request.user).order_by("-date").first()
        if report:
            date = report.date + datetime.timedelta(days=1)
        else:
            date = datetime.date.today()
        form = DailyReportForm(initial={'date': date})
    context = {'form': form}
    return render(request, template_name, context)

@login_required
def update_medical_report(request, date):
    template_name = 'reports/add_daily_report.html'
    report = get_object_or_404(DailyReport, date=date, user=request.user)
    report_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    if request.method == 'POST':
        # Get form instance and update values accordingly
        form = DailyReportForm(request.POST, instance=report)
        last_month_date = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        if form.is_valid():
            if form.instance.nasal_spray_used is None:
                form.instance.nostril_used = None
            if form.instance.nasal_spray_used and form.instance.nostril_used is None:
                form.instance.nostril_used = "both"
            if form.instance.antihistamine_120mg is None:
                form.instance.antihistamine_120mg = 0
            if form.instance.steroid_tablet is None:
                form.instance.steroid_tablet = 0
            if form.instance.inhaler is None:
                form.instance.inhaler = 0
            form.save()
            messages.success(request, "Report successfully updated")

            #   Check if report was from last month, may need to update medical score table
            if report_date.month == last_month_date.month and report_date.year == last_month_date.year:
                scores = get_medical_scores(request)
                last_month_scores = MedicalReportScores.objects.filter(user=request.user, date = last_month_date).first()
                if last_month_scores:
                    if last_month_scores.score != scores[1]:
                        last_month_scores.score = scores[1]
                        last_month_scores.save()

            #   Update daily scores
            #   report date score
            get_daily_score(request, report_date)

            #   next 4 days up until yesterday ( wont go any further)
            for i in range(1,5):
                new_date = report_date + datetime.timedelta(days=i)
                if new_date.date() < datetime.datetime.now().date():
                    get_daily_score(request, new_date)
            return redirect('get-report', date=date)
    else:
        form = DailyReportForm(instance=report)
    context = {'form': form}
    return render(request, template_name, context)




@login_required
def get_todays_report(request):
    template_name="reports/medical_report.html"
    # Get today's date
    date = datetime.datetime.now()
    # Get report and daily scratch count using today's date
    report = DailyReport.objects.filter(user=request.user, date=date).first()
    total_scratches = DailyScratchCount.objects.filter(user=request.user, date=date).first()

    # Convert date into string and pass it into context
    date = date.strftime("%A - %d/%m/%Y")
    context = {"report": report,
               "date": date,
               "total_scratches": total_scratches}
    # Check if there are any nights scratches for today, if so, pass that into the context
    if NightScratch.objects.filter(user=request.user, date=datetime.datetime.today()):
        context['night_points'] = NightScratch.objects.filter(user=request.user, date=datetime.datetime.today()).first()
    return render(request, template_name, context)


@login_required
def get_all_reports(request):
    template_name = "reports/all_reports.html"
    #   Get all daily scratch counts
    total_scratches = DailyScratchCount.objects.filter(user=request.user).order_by("-date")
    #   Use Paginator to select how many to show on each page
    paginator = Paginator(total_scratches, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"total_scratches": total_scratches, "page_obj": page_obj}

    return render(request, template_name, context)


@login_required
def get_report(request, date):
    #   Check if date from url is todays date, if so, redirect to todays-rport
    if date == datetime.datetime.now().strftime("%Y-%m-%d"):
        return redirect('get-todays-report')
    template_name = "reports/medical_report.html"
    #   convert date string from url into datetime object
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    #   get report using selected date
    report = DailyReport.objects.filter(user=request.user, date=date).first()
    #   Get daily scratch count of selected date
    total_scratches = DailyScratchCount.objects.filter(user=request.user, date=date).first()
    #   Convert date back into a string and pass it into the context
    date = date.strftime("%A - %d/%m/%Y")
    context = {"report": report,
               "date": date,
               "total_scratches": total_scratches}
    date = datetime.datetime.strptime(date, "%A - %d/%m/%Y")
    if NightScratch.objects.filter(user=request.user, date=date):
        context['night_points'] = NightScratch.objects.filter(user=request.user, date=date).first()
    return render(request, template_name, context)



@login_required
def daily_report_exists(request):
    if DailyReport.objects.filter(user=request.user, date=datetime.datetime.now()) is None:
        return redirect("add-daily-report")
    template_name = "reports/daily_report_exists.html"
    return render(request, template_name)

@login_required
def view_stats_table(request):
    template_name = "reports/medical_score_table.html"
    today = datetime.date.today()

    #   stats for Avg medical scores
    monthly_scores = MedicalReportScores.objects.filter(user=request.user).order_by("-date")
    for score in monthly_scores:
        score.date = score.date.strftime("%b %Y")
    daily_scores = MedicalReportDailyScores.objects.filter(user=request.user, date__month=today.month, date__year=today.year).order_by("-date")
    for score in daily_scores:
        score.date = score.date.strftime("%a %b %d")

    #   stats for avg NightScratches
    night_scratch_monthly_avg = NightScratchMonthlyAvg.objects.filter(user=request.user).order_by("-date")
    for score in night_scratch_monthly_avg:
        score.date = score.date.strftime("%b %Y")
    night_scratch_daily_scores = NightScratch.objects.filter(user=request.user, date__month = today.month, date__year=today.year).order_by("-date")
    for score in night_scratch_daily_scores:
        score.date = score.date.strftime("%a %b %d")

    #   stats for AvgScratches
    scratch_monthly_avg = ScratchMonthlyAvg.objects.filter(user=request.user).order_by("-date")
    for scratch in scratch_monthly_avg:
        scratch.date = scratch.date.strftime("%b %Y")
    daily_scratches = DailyScratchCount.objects.filter(user=request.user, date__month=today.month, date__year=today.year).order_by("-date")
    for scratch in daily_scratches:
        scratch.date = scratch.date.strftime("%a %b %d")

    context = {"monthly_scores": monthly_scores,
               "daily_scores": daily_scores,
               "night_avg": night_scratch_monthly_avg,
               "night_daily_scores": night_scratch_daily_scores,
               "scratch_avg": scratch_monthly_avg,
               "daily_scratches": daily_scratches}
    return render(request, template_name, context)


@login_required()
def scratch_score_chart(request):
    template_name = "reports/stats_chart.html"
    dates = []
    first_scratch = DailyScratchCount.objects.filter(user=request.user).order_by("date").first()
    dates.append(first_scratch.date)
    today_date = datetime.date.today().strftime("%Y-%m")
    first_daily_medical_score = MedicalReportDailyScores.objects.filter(user=request.user).order_by("date").first()
    dates.append(first_daily_medical_score.date)
    first_night_scratch = NightScratch.objects.filter(user=request.user).order_by("date").first()
    dates.append(first_night_scratch.date)
    print(dates)
    #   Use insertion sort to sort the 3 dates
    for i in range(1, len(dates)):
        key = dates[i]
        j = i - 1
        while j >=0 and key < dates[j]:
            dates[j+1] = dates[j]
            j -= 1
            dates[j+1] = key
    last_date = dates[0].strftime("%Y-%m")
    context = {"min_date": last_date,
               "today_date": today_date}

    return render(request, template_name, context)

