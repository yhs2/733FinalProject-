import json

import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .models import Employee
from .models import PredictImage
from .average_delay import airport_statistics
import time
from django.conf import settings
import os
from django.core.files import File
import base64
# Create your views here.
def index(request):
    return render(request, 'index.html')

def add_new(request):
    if request.method == "GET":
        form = EmployeeForm()
        return render(request, 'add_new.html', {"form": form})
    else:
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('./display')

def display(request):
    print(request)
    context = {'employee_list': Employee.objects.all()}
    return render(request, "display.html", context)

def get_desired(request):
    form = request.GET
    fullname = form.get("fullname")
    # fullname = dict(form).fullname
    # print(fullname)
    if len(form) != 0:
        context = {'employee_list': Employee.objects.filter(fullname=fullname)}
    else:
        context = {'employee_list': Employee.objects.all()}
    return render(request, "get_desired.html", context)

def prediction(request):
    form = request.GET
    if len(form) != 0:
        pred_image = PredictImage()
        pred_image_1 = PredictImage()
        pred_image_2 = PredictImage()
        plot_1, plot_2, plot_3, name = airport_statistics(form.get("AIRPORT_CODE"), form.get("START_DATE"), form.get("END_DATE")
                                          , form.get("GRAPH_NAME"))
        pred_image.img_name = name
        pred_image.image.save(name + "1.png", plot_1)
        pred_image.save()

        pred_image_1.img_name = name
        pred_image_1.image.save(name + "2.png", plot_2)
        pred_image_1.save()

        pred_image_2.img_name = name
        pred_image_2.image.save(name + "3.png", plot_3)
        pred_image_2.save()

        context = {'img_list': PredictImage.objects.filter(img_name=name), 'start_date':form.get("START_DATE"),\
                   'end_date': form.get('END_DATE'), 'iata_code': form.get('AIRPORT_CODE')}
    else:
        context = {'img_list': []}

    return render(request, "prediction.html", context)

def flight_status_dist(request):
    return render(request, "flight_status_dist.html")

# WEB Funtion

#
#
# airport_statistics('ATL', '2021-12-06', '2021-12-26', 'Delay_minutes')