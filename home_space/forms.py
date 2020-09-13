from django import forms

from .models import Space, Item, Food, Ingredient, Recipe

class SpaceForm(forms.ModelForm):
	class Meta:
		model = Space
		fields = ['name','super_space', 'kind']
		labels = {'name': 'Space Name'}

		widgets = {'name': forms.TextInput(attrs={'autofocus':'autofocus'})}

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['name','quantity','space', 'info','bot_date']
		labels = {'quantity': 'Quantity','space':'Space','bot_date':'Date bought'}

		widgets = {
			'name': forms.TextInput(attrs={'autofocus':'autofocus'}),
			'bot_date':forms.DateInput(attrs={'placeholder':'MM/DD/YYYY'})
		}

class FoodForm(forms.ModelForm):
	class Meta:
		model = Food
		fields = ['name','quantity','weight','w_metric','volume','v_metric','exp_date','bot_date']
		labels = {'weight':'Weight','volume':'Volume','v_metric':'Volume Convention','w_metric':'Weight Convention','exp_date':'Expiration Date','bot_date':'Date Purchased'}

		widgets = {
			'name': forms.TextInput(attrs={'autofocus':'autofocus'}),
			'exp_date':forms.DateInput(attrs={'placeholder':'MM/DD/YYYY'}),
			'bot_date':forms.DateInput(attrs={'placeholder':'MM/DD/YYYY'})
		}

class RecipeForm(forms.ModelForm):
	class Meta:
		model = Recipe
		fields = ['name', 'instructions']
		labels = {}

		widgets = {
			'instructions':forms.Textarea(attrs={'placeholder':'Steps go here...'}),
		}

class IngredientForm(forms.ModelForm):
	class Meta:
		model = Ingredient
		fields = ['name','quantity','weight','w_metric','volume','v_metric']
		labels = {}