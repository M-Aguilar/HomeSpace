from django import forms

from .models import Space, Item, Food

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

		widgets = {'name': forms.TextInput(attrs={'autofocus':'autofocus'})}

class FoodForm(forms.ModelForm):
	class Meta:
		model = Food
		fields = ['weight','volume','exp_date','bot_date']
		labels = {'weight':'weight','volume':'Volume','exp_date':'Expiration Date','bot_date':'Date Purchased'}