from django.shortcuts import render, redirect, get_object_or_404
from .models import Space, Item, Food, Recipe, Ingredient
from .forms import SpaceForm, ItemForm, FoodForm, RecipeForm, IngredientForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
# Create your views here.
def index(request):
	if request.user.is_authenticated:
		response = redirect('dashboard')
		return response
	return render(request, 'home_space/index.html')

@login_required
def dashboard(request):
	spaces = Space.objects.filter(owner=request.user)
	context = {'spaces':spaces}
	return render(request, 'home_space/dashboard.html', context)

'''TODO: Suggest spaces if none are present.
Another possibility if this gains enough traction is to limit spaces of type home. 
That typing would not allow for a super-space
'''

#------------------------SPACES------------------------
def about(request):
	return render(request,'home_space/about.html')

@login_required
def space(request, space):
	space = get_object_or_404(Space,id=space)
	spaces = Space.objects.filter(super_space=space)
	items = Item.objects.filter(space=space)
	if space.owner != request.user:
		raise Http404
	context = {'space': space,'items':items,'spaces':spaces}
	return render(request,'home_space/space.html',context)

@login_required
def new_space(request, space=''):
	if request.method != 'POST':
		form = SpaceForm(initial={'super_space':space})
	else:
		form = SpaceForm(data=request.POST)
		if form.is_valid():
			new_space = form.save(commit=False)
			new_space.owner = request.user
			new_space.save()
			return HttpResponseRedirect(reverse('dashboard'))
	context = {'form':form}
	return render(request, 'home_space/new_space.html',context)

@login_required
def edit_space(request, space):
	space = get_object_or_404(Space,id=space)
	if space.owner != request.user:
		raise Http404
	if request.method != 'POST':
		form = SpaceForm(instance=space)
	else:
		form = SpaceForm(instance=space,data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('dashboard'))
	context = {'space':space, 'form':form}
	return render(request,'home_space/edit_space.html',context)
#------------------------RECIPES------------------------
def recipes(request):
	recipes = Recipe.objects.all()
	context={'recipe':recipes}
	return render(request,'home_space/recipes.html',context)

def recipe(request,recipe_id):
	recipe = get_object_or_404(Recipe,recipe_id)
	context={'recipe':recipe}
	return render(request,'home_space/recipe.html',context)

@login_required
def new_recipe(request):
	if request.method != 'POST':
		form = RecipeForm()
	else:
		form = RecipeForm(data=request.POST)
		if form.is_valid():
			recipe = form.sace(commit=False)
			recipe.owner = request.user
			recipe.save()
			return HttpResponseRedirect(reverse('recipes'))
	i_form = IngredientForm()
	context={'form':form, 'i_form':i_form}
	return render(request,'home_space/new_recipe.html',context)

def new_ingredient(request,recipe):
	if request.method != 'POST':
		form = IngredientForm()
	else:
		form = IngredientForm(data=request.POST)
		if form.is_valid():
			ingredient = form.save()
			ingredient.recipe = recipe
			ingredient.save()
			return HttpResponseRedirect(reverse('recipes'))
	context = {'form':form}
	return render(request,'home_space/new_ingredient.html',context)
#------------------------FOOD------------------------
@login_required
def new_food(request, space):
	space = Space.objects.get(id=space)
	if request.method != 'POST':
		form = FoodForm(initial={'space':space,'quantity':1})
	else:
		form = FoodForm(data=request.POST)
		if form.is_valid():
			food = form.save(commit=False)
			food.space = space
			food.save()
			food.space.save()
			return HttpResponseRedirect(reverse('space', args=[space.id]))
	context = {'form':form,'space':space}
	return render(request,'home_space/new_food.html',context)

@login_required
def edit_food(request, food):
	food = get_object_or_404(Food,id=food)
	if food.space.owner != request.user:
		raise Http404
	if request.method != 'POST':
		form = FoodForm(instance=food)
	else:
		form = FoodForm(data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('space',args=[food.space.id]))
	context = {'form':form,'food':food}
	return render(request,'home_space/edit_food.html',context)
#------------------------ITEMS------------------------
@login_required
def new_item(request, space):
	space = Space.objects.get(id=space)
	if request.method != 'POST':
		form = ItemForm(initial={'space':space,'quantity':1})
	else:
		form = ItemForm(data=request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.space = space
			item.save()
			item.space.save()
			return HttpResponseRedirect(reverse('space', args=[space.id]))
	context = {'form':form, 'space':space}
	return render(request, 'home_space/new_item.html',context)

def edit_item(request,item):
	item = get_object_or_404(Item,id=item)
	if item.space.owner != request.user:
		raise Http404
	if request.method != 'POST':
		form = ItemForm(instance=item)
	else:
		form = ItemForm(instance=item,data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('space',args=[item.space.id]))
	context = {'form':form,'item':item}
	return render(request,'home_space/edit_item.html',context)

@login_required
def delete_item(request, item):
	item = get_object_or_404(Item,id=item)
	space = item.space.id
	if item.space.owner != request.user:
		raise Http404
	else:
		item.delete()
		return HttpResponseRedirect(reverse('space',args=[space]))

