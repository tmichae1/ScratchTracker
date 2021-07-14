from reports.models import DailyReport, MedicalReportDailyScores
from medication.models import Ointment
import datetime

def get_daily_score(request, report_date):
    ointments = Ointment.objects.all()
    score = 0
    extra_points = 0
    yesterday_report = DailyReport.objects.filter(user=request.user, date=report_date).first()
    if yesterday_report:
        if yesterday_report.inhaler > 0:
            score += 1
        score += yesterday_report.steroid_tablet
        score += yesterday_report.antihistamine_120mg
        if yesterday_report.nostril_used:
            if yesterday_report.nostril_used == "both":
                score += 1
            else:
                score += 0.5
        #   Elecon +2 points
        if yesterday_report.ointment_used == ointments[0]:
            score += 10 / 5
        #   Synylar + 8/5 points
        elif yesterday_report.ointment_used == ointments[1]:
            score += 8 / 5
        #   Elidel +1 point
        elif yesterday_report.ointment_used == ointments[2]:
            score += 1
        #   Locoid + 1 point
        elif yesterday_report.ointment_used == ointments[3]:
            score += 5 / 5

        #   scalp steroid + 4/5 points
        if yesterday_report.scalp_steroid:
            score += 4/5

    #   Get last 4 days reports
    reports = []
    for i in range(1,5):
        date = report_date - datetime.timedelta(days=i)
        report = DailyReport.objects.filter(user=request.user, date=date).first()
        if report:
            reports.append(report)
    for report in reports:
        if report.ointment_used == ointments[0]:
            extra_points += 10/5
        elif report.ointment_used == ointments[1]:
            extra_points += 8/5
        elif report.ointment_used == ointments[3]:
            extra_points += 5/5
        if report.scalp_steroid:
            extra_points += 4/5
    score += extra_points
    daily_score = MedicalReportDailyScores.objects.filter(user=request.user, date=report_date).first()
    if not daily_score:
        daily_score = MedicalReportDailyScores(user=request.user, score=score, date=report_date)
        daily_score.save()
    else:
        if daily_score.score != score:
            print("yes")
            daily_score.score = score
            daily_score.save()




