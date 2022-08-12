from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from .models import Object
import top.models as mo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
import datetime
from django.views.generic import View
from django.shortcuts import redirect
from geopy.distance import geodesic as GD 
import os
import sys
import json
from rest_framework import serializers
from django.conf import settings
geolocator = Nominatim(user_agent="geoapiExercises")
from django.http.response import JsonResponse
from PIL import Image
from django.contrib import messages

class ClosingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = mo.Closing
        fields = ['openid','date','time']
 
class ClosedRequest():
	"""docstring for ClosedRequests"""
	def __init__(self, name,obj,open_date,close_date):
		super(ClosedRequest, self).__init__()
		self.name = name
		self.obj = obj
		self.open_date = open_date
		self.close_date = close_date

def home(request):
    return render(request,"registration/login.html")


def newform(request):
	return render(request,"newnote.html")

def GetClosedRequests(name):
	closed_openid = []
	closed_dates = []
	closed_objects = []
	closed_open_dates = []

	listofrequests = []


	for req in mo.Closing.objects.all():
		if str(req.statusid) == 'Принята':
			closed_openid.append(ClosingModelSerializer(req).data.get('openid'))
			closed_dates.append(str(ClosingModelSerializer(req).data.get('date')) + " " + str(ClosingModelSerializer(req).data.get('time')))

	for req in mo.Opening.objects.all():
		if req.openid in closed_openid and str(req.workerid) == name:
			closed_objects.append(req.objectid)
			closed_open_dates.append(str(req.date)+ " " + str(req.time))
	for i in range(len(closed_objects)):
		listofrequests.append(ClosedRequest(name,closed_objects[i],closed_open_dates[i],closed_dates[i]))
	del closed_openid
	del closed_dates
	del closed_objects
	del closed_open_dates

	return listofrequests

@login_required
def mainworker(request):

	statuses = []
	objects = []
	userdata = []

	#ДЛЯ ВЫВОДА ЗАКРЫТЫХ ЗАЯВОК
	

	worker = GetWorker(request)

	closedrequests = GetClosedRequests(worker.fullname)

	#OBJECTS
	for objectx in mo.Object.objects.all():
		objects.append(objectx.name)

	confirmed = GetConfirmedRequests(mo.Closing.objects.all())

	unclosed = GetUnclosedRequest(mo.Opening.objects.all(),confirmed, worker.fullname)

	return render(request,"mainworker.html",{'objects' : objects, 'worker':worker, 'unclosed':unclosed,
	 'closed_requests':closedrequests})

@login_required
def base(request):
	objectname = str(request.POST.get("object"))
	objectt = GetObjectt(objectname)
	worker = GetWorker(request)
	longitude = GetObject(request,"longitude")
	latitude = GetObject(request,"latitude")
	location = geolocator.geocode(GetLocation(latitude,longitude))
	radius = GetObjectRadius(objectname)
	addres = GetObjectAddres(objectname)


	if longitude == "" or latitude == "":
		messages.error(request,"Приложению нужен доступ к геолокации")
		return HttpResponseRedirect("../")

	distance = GetDistance((float(addres.split(",")[0]),float(addres.split(",")[1])),(latitude, longitude))
	if distance > radius:
		messages.error(request,"Вы слишком далеко от объекта")
		return HttpResponseRedirect("../")
	AddNewNote(worker,objectt, location, distance)
	messages.success(request, 'Новая заявка успешно создана')
	return HttpResponseRedirect("../")


@login_required
def closing(request):
	objectname = str(GetObjectNameByNote(GetObject(request,"note")))
	longitude = GetObject(request,"longitude")
	latitude = GetObject(request,"latitude")
	if longitude == "" or latitude == "":
		messages.error(request,"Приложению нужен доступ к геолокации")
		return HttpResponseRedirect("../")
	location = geolocator.geocode(GetLocation(latitude,longitude))
	radius = GetObjectRadius(objectname)
	addres = GetObjectAddres(objectname)

	distance = GetDistance((float(addres.split(",")[0]),float(addres.split(",")[1])),(latitude, longitude))
	if distance > radius:
		messages.error(request,"Вы слишком далеко от объекта")
		return HttpResponseRedirect("../")
	photos = GetPhotos(request)
	AddClosingNote(GetObject(request,"note"), location, distance, photos,GetWorker(request).fullname, objectname)
	messages.success(request, 'Заявка отправлена на рассмотрение')
	return HttpResponseRedirect("../")


def GetObjectNameByNote(note):
	for opened in mo.Opening.objects.all():
		if opened.__str__() == note:
			return opened.objectid

def GetUnclosedRequest(opened, closed, fullname):
	unclosed = []
	for unclose in opened:
		if unclose not in closed:
			if str(unclose.workerid) == fullname:
				unclosed.append(unclose.__str__())
	return unclosed

def GetConfirmedRequests(closed):
	comfirmed = []
	for obj in closed:
		if str(obj.statusid) == "Принята" or str(obj.statusid) == "Открыта":
			comfirmed.append(obj.openid)
	return comfirmed

def GetPhotos(request):
	photos = []
	photos.append(request.FILES['photo1'])
	photos.append(request.FILES['photo2'])
	photos.append(request.FILES['photo3'])
	return photos

def GetObjectt(objectname):
	for objectt in mo.Object.objects.all():
		if objectname == objectt.name:
			return objectt

def GetObject(request, item):
	return request.POST.get(item)

def GetWorker(request):
	for worker in mo.Worker.objects.all():
		if worker.user_id == request.user.id:
			return worker

def GetLocation(latitude,longitude):
	return geolocator.geocode(latitude+","+longitude)

def GetCurrentTime():
	return datetime.datetime.now().replace(microsecond = 0)

def GetDistance(location1, location2):
	return round(float(str(GD(location1,location2))[:-3]))

def GetObjectRadius(objectname):
	for objectt in mo.Object.objects.all():
		if str(objectname) == str(objectt.__str__()):
			return objectt.radius

def GetObjectAddres(objectname):
	for objectt in mo.Object.objects.all():
		if objectname == objectt.name:
			return objectt.location

def GetLocationFromAddres(addres):
	location = geolocator.geocode(addres)
	return (location.latitude, location.longitude)

def AddNewNote(worker,objectt, location, distance):
	openid = 0
	if str(mo.Opening.objects.all().order_by('-openid')[:1]) =="<QuerySet []>":
		openid = 1
	else:
		for x in mo.Opening.objects.all().order_by('-openid')[:1]:
			openid = x.openid
	obj = mo.Opening()

	obj.openid = openid + 1
	obj.workerid = worker
	obj.objectid = objectt
	obj.location = location
	obj.distance = distance
	obj.time = GetCurrentTime()
	obj.date = datetime.date.today()

	obj.save()
	del obj

def GetOpenIdByStr(openid):
	for opened in mo.Opening.objects.all():
		if opened.__str__() == openid:
			return opened

def GetClosingStatus(status):
	for closestatus in mo.ClosingStatus.objects.all():
		if closestatus.__str__() == status:
			return closestatus

def AddClosingNote(openid, location, distance, photos,name, objectname):
	noteid = 0
	if str(mo.Closing.objects.all().order_by('-noteid')[:1]) =="<QuerySet []>":
		noteid = 0
	else:
		for x in mo.Closing.objects.all().order_by('-noteid')[:1]:
			noteid = x.noteid
	
	obj = mo.Closing()

	obj.noteid = noteid + 1
	obj.openid = GetOpenIdByStr(openid)
	obj.location = location
	obj.distance = distance
	obj.time = GetCurrentTime()
	obj.date = datetime.date.today()
	obj.statusid = GetClosingStatus("Открыта")

	obj.photo_1 = photos[0]
	obj.photo_2 = photos[1]
	obj.photo_3 = photos[2]
	obj.save()

	
	for i in range(1,4):
		photos[i-1] = NewPhotoName(name, objectname,i)


	PhotoRename(obj.photo_1, photos[0])
	PhotoRename(obj.photo_2, photos[1])
	PhotoRename(obj.photo_3, photos[2])

	#update_photo_names
	t = mo.Closing.objects.get(noteid=obj.noteid)
	t.photo_1 = photos[0]
	t.photo_2 = photos[1]
	t.photo_3 = photos[2]
	t.save() #

	del obj
	del photos
	del t


def uploadPath():
	Y = str(datetime.date.today()).split('-')[0]
	M = str(datetime.date.today()).split('-')[1]
	D = str(datetime.date.today()).split('-')[2]
	return "D:/TabelPr/Shedule/Report/"

def uploadPath2():
	Y = str(datetime.date.today()).split('-')[0]
	M = str(datetime.date.today()).split('-')[1]
	D = str(datetime.date.today()).split('-')[2]
	return "photos/"+Y+'/'+M+'/'+D+'/'

def Time():
	return str(str(datetime.datetime.now().hour)+"-"+str(datetime.datetime.now().minute))

def NewPhotoName(workername, objectname,photonumber):
	return uploadPath2()+ workername +"-"+objectname+"-"+ str(photonumber)+ "-"+Time()+ ".jpg"

def PhotoRename(photo,newname):
	os.rename(str(uploadPath()+str(photo)),newname)