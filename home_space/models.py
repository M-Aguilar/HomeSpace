from django.db import models
import datetime
from django.contrib.auth.models import User
import django.utils
# Create your models here.
class Space(models.Model):
	TYPE = [
		('inv','inventory'),
		('rm','room'),
		('hm','home')
	]

	name = models.CharField(max_length=35)
	super_space = models.ForeignKey('self', on_delete=models.CASCADE,blank=True, null=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	kind = models.CharField(max_length=3,choices=TYPE, default=TYPE[2])

	def __str__(self):
		return self.name

'''Food and Non-food items share some similar descriptive qualities of which are
present below. 
'''
class ItemInfo(models.Model):
	name = models.CharField(max_length=80)
	quantity = models.IntegerField(default=1)
	space = models.ForeignKey(Space, on_delete=models.CASCADE)
	#Date bought and/or put into inventory. 
	bot_date = models.DateField()

	class Meta:
		abstract = True

'''For now weight and '''
class Item(ItemInfo):
	info = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.name

'''Food Items are different than regular items in that they expire. 
They are only good for a certain period of time. And I want to keep track 
as to whether it was consumed or not. 
Expired date will not be fixed. It will be adjustable and should be changed to whenever the
food is deemed inedible. 
'''
class Food(ItemInfo):
	WEIGHT = [
		('g','grams'),
		('oz','ounces'),
		('lb','pounds'),
	]

	VOLUME = [
		('floz','fluid ounces'),
		('tbsp',''),
		('L','liter'),
		('g','gallon'),
		('c','cup'),
		('pt','pint'),
		('mL','milliliter'),
		('tsp','teaspoon')
	]

	w_metric = models.CharField(max_length=2,choices=WEIGHT, blank=True)
	v_metric = models.CharField(max_length=4,choices=VOLUME, blank=True)

	weight = models.IntegerField()
	volume = models.IntegerField()
	#Expiration date. Estimated expiration date or date deemed expired.
	exp_date = models.DateField()
	#Was consumed
	consumed = models.BooleanField(default=False)