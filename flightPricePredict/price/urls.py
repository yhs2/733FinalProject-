from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = {
    path('', views.index, name="price"),
    path('add_new', views.add_new, name="add-new"),
    path('display', views.display, name="display"),
    path('get_desired', views.get_desired, name="get_desired"),
    path('prediction', views.prediction, name="prediction"),
    path('flight_status_dist', views.flight_status_dist, name="flight_status_dist")
}

