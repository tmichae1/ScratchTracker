from rest_framework import serializers
from scratch.models import Scratch, DailyScratchCount, NightScratch
from reports.models import MedicalReportDailyScores




class ScratchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scratch
        fields = ["user", "date", "time"]



class StatsSerializer(serializers.Serializer):
    weekly_avg_time = serializers.IntegerField()
    daily_total = serializers.IntegerField()
    scratch_avg_current_month = serializers.IntegerField()
    scratch_avg_last_month = serializers.IntegerField()
    night_points_current_month = serializers.FloatField()
    night_points_last_month = serializers.FloatField()
    medical_score_current_month = serializers.FloatField()
    medical_score_last_month = serializers.FloatField()

class MedicalHistoryDaysSerializer(serializers.Serializer):
    name = serializers.CharField()
    days = serializers.IntegerField()


class DailyScratchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyScratchCount
        fields = ["total", "date"]


class DailyMedicalScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalReportDailyScores
        fields = ["score", "date"]


class NightScratchScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = NightScratch
        fields = ["points", "date"]