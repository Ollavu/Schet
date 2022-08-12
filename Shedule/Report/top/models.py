from django.db import models
from django.contrib.auth.models import User
import datetime
class Worker(models.Model):
	"""docstring for worker"""

	def __str__(self):
		return f"{self.fullname}"
	
	workerid = models.IntegerField(primary_key=True)
	user=models.OneToOneField(User,on_delete=models.CASCADE, null=True, unique = True)
	tabel = models.IntegerField(null=True)
	fullname = models.CharField(max_length=50, null=True)
	post = models.CharField(max_length=20, null=True)
	coeff = models.FloatField()

	class Meta:

		verbose_name = "Монтажник"
		verbose_name_plural = "Монтажники"
			



class Object(models.Model):

	objectid = models.IntegerField(primary_key=True)
	location = models.CharField(max_length=150, null=True)
	name = models.CharField(max_length=50, null=True)
	objecttype = models.CharField(max_length=20, null=True)
	radius = models.IntegerField()

	def __str__(self):
		return f"{self.name}"

	class Meta:

		verbose_name = "Объект"
		verbose_name_plural = "Объекты"

class Opening(models.Model):
	openid = models.IntegerField(primary_key=True)
	workerid = models.ForeignKey(Worker,to_field='workerid', on_delete=models.CASCADE, null=True)
	objectid = models.ForeignKey(Object,to_field='objectid', on_delete=models.CASCADE, null=True)
	date = models.DateField(max_length=50)
	time = models.TimeField()
	location = models.CharField(max_length=150)
	distance = models.IntegerField()

	def __str__(self):
		return f"{self.workerid}, {self.objectid}, {self.date}, {self.time}"

	class Meta:

		verbose_name = "Открытые заявки"
		verbose_name_plural = "Открытые заявки"

class ClosingStatus(models.Model):
	statusid = models.IntegerField(primary_key=True)
	definition = models.CharField(max_length=20)
	def __str__(self):
		return f"{self.definition}"

	class Meta:

		verbose_name = "Статусы закрытых заявок"
		verbose_name_plural = "Статусы закрытых заявок"

def uploadPath():
	Y = str(datetime.date.today()).split('-')[0]
	M = str(datetime.date.today()).split('-')[1]
	D = str(datetime.date.today()).split('-')[2]
	return 'photos/'+Y+'/'+M+'/'+D+'/'

class Closing(models.Model):	
	noteid = models.IntegerField(primary_key=True)
	openid = models.OneToOneField(Opening,to_field='openid', on_delete=models.CASCADE, null=True, unique = True)
	time = models.TimeField()
	distance = models.IntegerField()
	location = models.CharField(max_length=150)
	photo_1 = models.ImageField(upload_to=uploadPath(), blank=True, verbose_name='Фото 1')
	photo_2 = models.ImageField(upload_to=uploadPath(), blank=True, verbose_name='Фото 2')
	photo_3 = models.ImageField(upload_to=uploadPath(), blank=True, verbose_name='Фото 3')
	statusid = models.ForeignKey(ClosingStatus, to_field='statusid', on_delete = models.CASCADE, null = True)
	date = models.DateField(max_length=50)

	def __str__(self):
		return f"{self.openid}"

	class Meta:

		verbose_name = "Закрытые заявки"
		verbose_name_plural = "Закрытые заявки"



class DataToExport(models.Model):

	worker_fullname = models.CharField(max_length=150, verbose_name = 'ФИО')
	object_name = models.CharField(max_length=150, verbose_name = 'Объект')
	opendate = models.DateField(verbose_name = 'Окрыто')
	closedate = models.DateField(verbose_name = 'Закрыто')
	spended_time = models.CharField(max_length=25,verbose_name = 'Затраченное время')

	class Meta:

		verbose_name = "Отчёт в Excel"
		verbose_name_plural = "Отчёт в Excel"


class TotalSpendedTimeOnObject(models.Model):

	worker_fullname = models.CharField(max_length=150, verbose_name = 'ФИО')
	object_name = models.CharField(max_length=150, verbose_name = 'Объект')
	spended_time = models.CharField(max_length=25,verbose_name = 'Затраченное время')

	class Meta:

		verbose_name = "Суммарное время на объекте в Excel"
		verbose_name_plural = "Суммарное время на объекте в Excel"