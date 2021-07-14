from django.urls import path
from . import views

urlpatterns = [
    path('', views.scratch, name='scratch-home'),
    path('add/scratch/', views.add_scratch, name='add-scratch'),
    path('night/nightly-scratch-/', views.night_scratch, name='night-scratch'),
    path('night/night-scratch-exists/', views.night_scratch_exists, name='night-scratch-exists'),
    path('night/update-night-scratch/<date>/', views.update_night_scratch, name='update-night-scratch'),
    path('add/missed-scratch/<date>/', views.add_missed_scratch, name="add-missed-scratch")
]