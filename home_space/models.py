from django.db import models
import datetime
from django.contrib.auth.models import User
import django.utils
# Create your models here.

HELP_TEXT = {
	'ITEM': {
		'info':'A short description. Is adjustable.',
		'quantity':'Is adjustable.',
		'bot_date':'',
	},
	
	'FOOD': {
		'bot_date':'',
		'exp_date':'',
		'consumed':''
	},
	
	'SPACE': {
		'super_space':'',
		'kind':''
	},

}

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
class Info(models.Model):
	space = models.ForeignKey(Space, on_delete=models.CASCADE)
	#Date bought and/or put into inventory. 
	bot_date = models.DateField(help_text=HELP_TEXT['ITEM']['bot_date'])

	class Meta:
		abstract=True

class ItemInfo(models.Model):
	name = models.CharField(max_length=80)

	class Meta:
		abstract = True

class FoodInfo(ItemInfo):
	quantity = models.IntegerField(default=1,help_text=HELP_TEXT['ITEM']['quantity'])
	
	WEIGHT = [
		('g','grams'),
		('oz','ounces'),
		('lb','pounds'),
	]

	VOLUME = [
		('floz','fluid ounces'),
		('tbsp','tablespoon'),
		('L','liter'),
		('g','gallon'),
		('c','cup'),
		('pt','pint'),
		('mL','milliliter'),
		('tsp','teaspoon')
	]

	w_metric = models.CharField(max_length=2,choices=WEIGHT, blank=True)
	v_metric = models.CharField(max_length=4,choices=VOLUME, blank=True)

	weight = models.IntegerField(blank=True)
	volume = models.IntegerField(blank=True)

	class Meta:
		abstract = True

'''For now weight and '''
class Item(Info, ItemInfo):
	info = models.CharField(max_length=100, blank=True, help_text=HELP_TEXT['ITEM']['info'])
	quantity = models.IntegerField(default=1,help_text=HELP_TEXT['ITEM']['quantity'])
	
	def __str__(self):
		return self.name

'''Food Items are different than regular items in that they expire. 
They are only good for a certain period of time. And I want to keep track 
as to whether it was consumed or not. 
Expired date will not be fixed. It will be adjustable and should be changed to whenever the
food is deemed inedible. 
'''

class Recipe(models.Model):
	name = models.CharField(max_length=50)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	instructions = models.TextField()

class Ingredient(FoodInfo):
	recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)

class Food(FoodInfo, Info):
		#Expiration date. Estimated expiration date or date deemed expired.
	exp_date = models.DateField(help_text=HELP_TEXT['FOOD']['exp_date'])
	#Was consumed
	consumed = models.BooleanField(default=False,help_text=HELP_TEXT['FOOD']['consumed'])
