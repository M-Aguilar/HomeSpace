from django import forms

from .models import Home, Room, Inventory, Item, Food, Ingredient, Recipe, Step

class InventoryForm(forms.ModelForm):
	class Meta:
		model = Inventory
		fields = ['name']
		labels = {'name': 'Inventory Name'}

class HoldsFoodForm(forms.ModelForm):
	class Meta:
		model = Inventory
		fields = ['holds_food']
		labels = {'holds_food': 'Holds Food'}
		widgets = {'holds_food': forms.CheckboxInput(attrs={'class':'form-check-input'})}

class RoomForm(forms.ModelForm):
	class Meta:
		model = Room
		fields = ['name']
		labels = {'name': ''}

		widgets = {'name': forms.TextInput(attrs={'placeholder': 'Room Name'})}

class HomeForm(forms.ModelForm):
	class Meta:
		model = Home
		fields = ['name']
		labels = {'name': 'Home Name'}

		widgets = {'name': forms.TextInput(attrs={'autofocus':'autofocus'})}

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['name','quantity','space', 'info','bot_date']
		labels = {'quantity': 'Quantity','space':'Inventory','bot_date':'Date bought'}

		widgets = {
			'name': forms.TextInput(attrs={'autofocus':'autofocus'}),
			'bot_date':forms.DateInput(attrs={'placeholder':'MM/DD/YYYY'})
		}

class FoodForm(forms.ModelForm):
	class Meta:
		model = Food
		fields = ['name','quantity','metric','exp_date','bot_date']
		labels = {'weight':'Weight', 'exp_date':'Expiration Date','bot_date':'Date Purchased'}

		widgets = {
			'name': forms.TextInput(attrs={'autofocus':'autofocus'}),
			'exp_date':forms.DateInput(attrs={'placeholder':'MM/DD/YYYY'}),
			'bot_date':forms.DateInput(attrs={'placeholder':'MM/DD/YYYY'})
		}

class RecipeForm(forms.ModelForm):
	class Meta:
		model = Recipe
		fields = ['name'] #,'instructions']
		labels = {}

		widgets = {
			'name': forms.TextInput(attrs={'autofocus':'autofocus'}),
			#'instructions':forms.Textarea(attrs={'placeholder':'Steps go here...'}),
		}

class IngredientForm(forms.ModelForm):
	class Meta:
		model = Ingredient
		fields = ['name','quantity','metric']
		labels = {}

		widgets = {
			'name': forms.TextInput(attrs={'autofocus':'autofocus'}),
		}

class StepForm(forms.ModelForm):
	class Meta:
		model = Step
		fields = ['instruction', 'step_number']
		labels = {}