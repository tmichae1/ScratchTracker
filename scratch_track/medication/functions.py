import datetime


def days_between(date):
    today = datetime.date.today()
    return abs((today - date).days)


def insertion_sort_medical_history(medical_history_list):
    for i in range(1, len(medical_history_list)):
        j = i-1
        while medical_history_list[j].days > medical_history_list[j+1].days and j >= 0:
            medical_history_list[j], medical_history_list[j+1] = medical_history_list[j+1], medical_history_list[j]
            j -= 1
