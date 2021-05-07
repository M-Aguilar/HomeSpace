from django.db import models
import datetime
from django.contrib.auth.models import User
import django.utils

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

FOOD_STORAGE_IND = [
	'Kitchen',
	'Freezer',
	'Pantry',
]


def user_directory_path(instance, filename):
	try:
		return '{0}/{1}/{2}'.format('items', instance.item.name, filename)
	except AttributeError:
		print("Attribute Error: user_directory_path 1")
		pass

class Space(models.Model):
	name = models.CharField(max_length=35)

	def __str__(self):
		return self.name

	class Meta:
		abstract = True

class Home(Space):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'homes'

class Membership(models.Model):
	household = models.ForeignKey(Home, on_delete=models.CASCADE)
	member = models.ForeignKey(User, on_delete=models.CASCADE)
	can_edit = models.BooleanField(default=True)

class Room(Space):
	home = models.ForeignKey(Home, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'rooms'

class Inventory(Space):
	holds_food = models.BooleanField(default=False)
	space = models.ForeignKey(Room, on_delete=models.CASCADE)

'''Food and Non-food items share some similar descriptive qualities of which are
present below. 
'''
class Info(models.Model):
	space = models.ForeignKey(Inventory, on_delete=models.CASCADE)
	#Date bought and/or put into inventory. 
	bot_date = models.DateField(help_text=HELP_TEXT['ITEM']['bot_date'])

	class Meta:
		abstract=True

class ItemInfo(models.Model):
	name = models.CharField(max_length=80)

	class Meta:
		abstract = True

	def __str__(self):
		return self.name

class FoodInfo(ItemInfo):
	NUMBER = 'n'
	GRAM = 'gm'
	OUNCES = 'oz'
	POUNDS = 'lb'
	FLUIDOUNCES = 'floz'
	TABLESPOON = 'tbsp'
	LITER = 'L'
	GALLON = 'gal'
	CUP = 'c'
	PINT = 'pt'
	MILLILITER = 'mL'
	TEASPOON = 'tsp'

	METRIC = [
		(NUMBER, 'number'),
		(GRAM,'gram'),
		(OUNCES,'ounces'),
		(POUNDS,'pounds'),
		(FLUIDOUNCES,'fluid ounces'),
		(TABLESPOON,'tablespoon'),
		(LITER,'liter'),
		(GALLON,'gallon'),
		(CUP,'cup'),
		(PINT,'pint'),
		(MILLILITER,'milliliter'),
		(TEASPOON,'teaspoon'),
	]

	quantity = models.DecimalField(default=1, max_digits=6, decimal_places=3, help_text=HELP_TEXT['ITEM']['quantity'])
	metric = models.CharField(max_length=4,choices=METRIC, blank=True, default=METRIC[0])

	class Meta:
		abstract = True

'''For now weight and '''
class Item(Info, ItemInfo):
	info = models.CharField(max_length=100, blank=True, help_text=HELP_TEXT['ITEM']['info'])
	quantity = models.IntegerField(default=1,help_text=HELP_TEXT['ITEM']['quantity'])

	class Meta:
		verbose_name_plural = 'items'

class ItemImage(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

class Recipe(models.Model):
	name = models.CharField(max_length=50)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'Recipes'

class Step(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	step_number = models.IntegerField()
	instruction = models.TextField()

	class Meta:
		verbose_name_plural = 'steps'

class Ingredient(FoodInfo):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'ingredients'

class Food(FoodInfo, Info):
	exp_date = models.DateField(help_text=HELP_TEXT['FOOD']['exp_date'])
	consumed = models.BooleanField(default=False,help_text=HELP_TEXT['FOOD']['consumed'])

class FoodImage(models.Model):
	item = models.ForeignKey(Food, on_delete=models.CASCADE)
	image = models.ImageField(upload_to=user_directory_path, blank=True,  null=True)

class GarageSale(models.Model):
	name = models.CharField(max_length=50)
	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)
	home = models.ForeignKey(Home, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class ForSale(models.Model):
	vendor = models.ForeignKey(GarageSale, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)