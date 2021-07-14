class Stats(object):

    def __init__(self, weekly_avg_time, daily_total,
                 scratch_avg_current_month, scratch_avg_last_month,
                 night_points_current_month, night_points_last_month,
                 medical_score_current_month, medical_score_last_month):
        self.weekly_avg_time = weekly_avg_time
        self.daily_total = daily_total
        self.scratch_avg_current_month = scratch_avg_current_month
        self.scratch_avg_last_month = scratch_avg_last_month
        self.night_points_current_month = night_points_current_month
        self.night_points_last_month = night_points_last_month
        self.medical_score_current_month = medical_score_current_month
        self.medical_score_last_month = medical_score_last_month


class MedicalHistoryDays(object):
    def __init__(self, name, days):
        self.name = name
        self.days = days
