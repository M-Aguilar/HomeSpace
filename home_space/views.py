from django.shortcuts import render, redirect, get_object_or_404
from .models import Home, Room, Inventory, Item, Food, Recipe, Ingredient, FOOD_STORAGE_IND
from .forms import HomeForm, RoomForm, ItemForm, FoodForm, RecipeForm, IngredientForm, HoldsFoodForm, InventoryForm, GarageSaleForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

def index(request):
	if request.user.is_authenticated:
		response = redirect('dashboard')
		return response
	return render(request, 'home_space/index.html')

@login_required
def dashboard(request):
	homes = Home.objects.filter(owner=request.user)
	context = {'homes':homes}
	if not homes:
		context['home_form'] = HomeForm()
	else:
		context['room_form'] = RoomForm()
	return render(request, 'home_space/dashboard.html', context)

def about(request):
	return render(request,'home_space/about.html')

@login_required
def room(request, room_id):
	space = get_object_or_404(Room,id=room_id)
	if space.home.owner != request.user:
		raise Http404
	context = {'room': space, 'i_form': InventoryForm()}
	return render(request,'home_space/room.html', context)

@login_required
def new_home(request):
	if request.method == 'POST':
		form = HomeForm(data=request.POST)
		if form.is_valid():
			new_space = form.save(commit=False)
			new_space.owner = request.user
			new_space.save()
			return HttpResponseRedirect(reverse('dashboard'))

@login_required
def new_room(request, home_id):
	home = Home.objects.get(id=home_id)
	if request.method == 'POST':
		form = RoomForm(data=request.POST)
		if form.is_valid():
			new_space = form.save(commit=False)
			new_space.home = home
			new_space.owner = request.user
			new_space.save()
			new_inv = Inventory.objects.create(space=new_space, name='{0} Inventory'.format(new_space.name))
			if new_space.name in FOOD_STORAGE_IND:
				new_inv.holds_food = True
			new_inv.save()
			return HttpResponseRedirect(reverse('dashboard'))

@login_required
def delete_room(request, room_id):
	room = get_object_or_404(Room, id=room_id)
	if request.user == room.home.owner:
		room.delete()
		return HttpResponseRedirect(reverse('dashboard'))

@login_required
def edit_room(request, room_id):
	space = get_object_or_404(Room,id=room_id)
	if space.home.owner != request.user:
		raise Http404
	if request.method != 'POST':
		form = RoomForm(instance=space)
		i_form = HoldsFoodForm(instance=space.inventory_set.first())
	else:
		form = RoomForm(instance=space,data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('dashboard'))
	context = {'room':space, 'form':form, 'i_form': i_form}
	return render(request,'home_space/edit_room.html',context)

@login_required
def inventory(request, inventory_id):
	inv = get_object_or_404(Inventory, id=inventory_id)
	if request.user != inv.space.home.owner:
		raise Http404
	context = {'inv': inv}
	return render(request, 'home_space/inventory.html', context)

@login_required
def new_inventory(request, room_id):
	room = get_object_or_404(Room, id=room_id)
	if room.home.owner == request.user:
		if request.method =='POST':
			form  = InventoryForm(data=request.POST)
			if form.is_valid():
				new_inv = form.save(commit=False)
				new_inv.space = room
				new_inv.save()
				return HttpResponseRedirect(reverse('room', args=[room.id]))
	else:
		raise Http404

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
def new_food(request, inventory_id):
	space = Inventory.objects.get(id=inventory_id)
	if request.method != 'POST':
		form = FoodForm(initial={'space':space})
	else:
		form = FoodForm(data=request.POST)
		if form.is_valid():
			food = form.save(commit=False)
			food.space = space
			food.save()
			food.space.save()
			return HttpResponseRedirect(reverse('room', args=[space.space.id]))
	context = {'form':form,'inventory':space}
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
def new_item(request, inventory_id):
	space = Inventory.objects.get(id=inventory_id)
	if request.method != 'POST':
		form = ItemForm(initial={'space':space})
	else:
		form = ItemForm(data=request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.inventory = space
			item.save()
			item.inventory.save()
			return HttpResponseRedirect(reverse('room', args=[item.inventory.room.id]))
	context = {'form':form, 'inventory':space}
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

def new_garage_sale(request):
	form = GarageSaleForm()
	context = {'form': form}
	return render(request, 'home_space/new_garage_sale.html', context)