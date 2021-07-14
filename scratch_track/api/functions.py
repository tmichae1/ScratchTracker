from medication.models import Ointment
from reports.models import DailyReport
import datetime


def get_medical_scores(request):
    reports = []
    ointments = Ointment.objects.all()
    today = datetime.date.today()
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    last_month_date = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    month_before_last_date = last_month_date.replace(day=1) - datetime.timedelta(days=1)

    #   Get reports from this month, last month and month before last
    #   Append them to reports
    #   month before last
    reports_month_before_last = DailyReport.objects.filter(user=request.user, date__month=month_before_last_date.month, date__year=month_before_last_date.year).order_by('date')
    for report in reports_month_before_last:
        reports.append(report)
    #   last month
    reports_last_month = DailyReport.objects.filter(user=request.user, date__month=last_month_date.month, date__year=last_month_date.year).order_by('date')
    for report in reports_last_month:
        reports.append(report)
    #   current month
    reports_this_month = DailyReport.objects.filter(user=request.user, date__month=today.month, date__year=today.year).order_by('date')
    for report in reports_this_month:
        reports.append(report)

    #   boolean values to check if there is at least 1 report for the month
    last_month = False
    this_month = False
    month_before_last = False

    last_month_score = 0
    this_month_score = 0

    # last month carries
    last_month_elocon = []
    last_month_synylar = []
    last_month_scalp_steroid = []
    last_month_locoid = []

    #   month before last extra
    month_before_last_extra = 0

    #   index's so we know where the first report for last month is
    index = 0
    index_final = 0
    have_index_final = False

    for report in reports:
        #   Check if report is from month before last
        if report.date.month == month_before_last_date.month:
            month_before_last = True
            #   Just working out what extra to add for last month,
            #   so only concerned about the reports that are 4 days before the end of the month before last
            if report.date.day > month_days[report.date.month -1] -4:
                if report.ointment_used == ointments[0]:
                    days_diff = month_days[report.date.month - 1] - (report.date.day-1)
                    month_before_last_extra +=(10/5)*(5-days_diff)
                elif report.ointment_used == ointments[1]:
                    days_diff = month_days[report.date.month - 1] - (report.date.day-1)
                    month_before_last_extra +=(8/5)*(5-days_diff)
                elif report.ointment_used == ointments[3]:
                    days_diff = month_days[report.date.month - 1] - (report.date.day-1)
                    month_before_last_extra +=(5/5)*(5-days_diff)
                if report.scalp_steroid:
                    days_diff = month_days[report.date.month - 1] - (report.date.day-1)
                    month_before_last_extra += (4/5)*(5-days_diff)
            index += 1
        #   Check if current report is from last month
        elif report.date.month == last_month_date.month:
            last_month = True
            if not have_index_final:
                index_final = index
                have_index_final = True
            if report.inhaler > 0:
                last_month_score += 1
            last_month_score += report.steroid_tablet
            last_month_score += report.antihistamine_120mg
            if report.nostril_used:
                if report.nostril_used == "both":
                    last_month_score += 1
                else:
                    last_month_score += 0.5
            #   Elocon ointment
            if report.ointment_used == ointments[0]:
                #   Check if date is 5 days before end of last month
                if report.date.day > month_days[report.date.month -1] - 4:
                    days_diff = month_days[report.date.month - 1] - (report.date.day-1)
                    #   Sort carry over points for last month and this month
                    last_month_score += (10 / 5)*days_diff
                    last_month_elocon.append((10/5)*(5-days_diff))
                else:
                    #   assign all points to last month
                    last_month_score += 10
            #   Synylar ointment
            elif report.ointment_used == ointments[1]:
                #   Check if date is 5 days before end of last month
                if report.date.day > month_days[report.date.month -1] - 4:
                    days_diff = month_days[report.date.month - 1] - (report.date.day-1)
                    #   Sort carry over points for last month and this month
                    last_month_score += (8 / 5)*days_diff
                    last_month_synylar.append((8/5)*(5-days_diff))
                else:
                    #   assign all points to last month
                    last_month_score += 8
            elif report.ointment_used == ointments[2]:
                last_month_score += 1
            #   Locoid ointment
            elif report.ointment_used == ointments[3]:
                #   Check if date is 5 days before end of last month
                if report.date.day > month_days[report.date.month -1] - 4:
                    days_diff = month_days[report.date.month - 1] - (report.date.day-1)
                    #   Sort carry over points for last month and this month
                    last_month_score += (5 / 5)*days_diff
                    last_month_locoid.append((5/5)*(5-days_diff))
                else:
                    #   assign all points to last month
                    last_month_score += 5
            if report.scalp_steroid:
                #   Check if date is 5 days before end of last month
                if report.date.day > month_days[report.date.month -1] - 4:
                    days_diff = month_days[report.date.month - 1] - (report.date.day-1)
                    #   Sort carry over points for last month and this month
                    last_month_score += (4 / 5)*days_diff
                    last_month_scalp_steroid.append((4/5)*(5-days_diff))
                else:
                    #   assign all points to last month
                    last_month_score += 4
        else:
            #   Report is for current month
            this_month = True
            if report.inhaler > 0:
                last_month_score += 1
            this_month_score += report.steroid_tablet
            this_month_score += report.antihistamine_120mg
            if report.nostril_used:
                if report.nostril_used == "both":
                    this_month_score += 1
                else:
                    this_month_score += 0.5
            #   Elocon ointment
            if report.ointment_used == ointments[0]:
                if report.date.day + 5 < today.day:
                    this_month_score += 10
                else:
                    this_month_score += (10/5) * (today.day - report.date.day)
            #   Synylar ointment
            elif report.ointment_used == ointments[1]:
                if report.date.day + 5 < today.day:
                    this_month_score += 8
                else:
                    this_month_score += (8/5) * (today.day - report.date.day)
            #   Elidel ointment
            elif report.ointment_used == ointments[2]:
                this_month_score += 1
            #   Locoid
            elif report.ointment_used == ointments[3]:
                if report.date.day + 5 < today.day:
                    this_month_score += 5
                else:
                    this_month_score += (5/5) * (today.day - report.date.day)
            if report.scalp_steroid:
                if report.date.day + 5 < today.day:
                    this_month_score += 4
                else:
                    this_month_score += (4/5) * (today.day - report.date.day)
            print(this_month_score)
    #   add overlapping points from last month onto this month
    #   Elocon
    for score in last_month_elocon:
        days_overlap = (score * 5) / 10
        if days_overlap < today.day:
            this_month_score += score
        else:
            if DailyReport.objects.filter(user=request.user, date=today):
                this_month_score += ((score / days_overlap) * today.day)
            else:
                this_month_score += ((score / days_overlap) * (today.day - 1))
    #   Synyar
    for score in last_month_synylar:
        days_overlap = (score * 5) / 8
        if days_overlap < today.day:
            this_month_score += score
        else:
            if DailyReport.objects.filter(user=request.user, date=today):
                this_month_score += ((score / days_overlap) * today.day)
            else:
                this_month_score += ((score / days_overlap) * (today.day - 1))
    #   Locoid
    for score in last_month_locoid:
        days_overlap = (score * 5) / 5
        if days_overlap < today.day:
            this_month_score += score
        else:
            if DailyReport.objects.filter(user=request.user, date=today):
                this_month_score += ((score / days_overlap) * today.day)
            else:
                this_month_score += ((score / days_overlap) * (today.day - 1))
    #   Scalp Steroid
    for score in last_month_scalp_steroid:
        days_overlap = (score * 5) / 4
        if days_overlap < today.day:
            this_month_score += score
        else:
            if DailyReport.objects.filter(user=request.user, date=today):
                this_month_score += ((score / days_overlap) * today.day)
            else:
                this_month_score += ((score / days_overlap) * (today.day - 1))
    #   calculate the final average
    print(this_month_score)
    if this_month:
        if today.day > 1:
            if DailyReport.objects.filter(user=request.user, date=today):
                this_month_score = round(this_month_score / today.day, 1)
                print(today.day)
            else:
                this_month_score = round(this_month_score / (today.day - 1), 1)
                print(today.day - 1)
        else:
            if DailyReport.objects.filter(user=request.user, date=today):
                this_month_score = round(this_month_score / today.day, 1)
            else:
                this_month_score = 0
    if last_month:
        last_month_score += month_before_last_extra
        if month_before_last:
            last_month_score = round(last_month_score / (month_days[last_month_date.month - 1]), 1)
        else:
            if reports[index_final].date.day == 1:
                last_month_score = round(last_month_score / (month_days[last_month_date.month - 1]), 1)
            else:
                last_month_score = round(last_month_score / ((month_days[reports[index_final].date.month - 1]) - (reports[index_final].date.day - 1)), 1)
    return[this_month_score, last_month_score]
