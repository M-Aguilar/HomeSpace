from django.shortcuts import render, redirect, get_object_or_404
from .models import Home, Room, Inventory, Item, Food, Recipe, Ingredient, FOOD_STORAGE_IND, GarageSale, ForSale, Membership
from .forms import HomeForm, RoomForm, ItemForm, FoodForm, RecipeForm, IngredientForm, HoldsFoodForm, InventoryForm, GarageSaleForm, ItemImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.db.models import Q, F
from django.template.loader import render_to_string
from django.core import serializers
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse

def homehelp(request):
	if request.user.is_authenticated:
		response = redirect('dashboard')
		return response
	return render(request, 'home_space/index.html')

@login_required
def dashboard(request):
	homes = Home.objects.filter(Q(owner=request.user)|Q(membership__member=request.user))
	context = {'homes':homes}
	if not homes:
		context['home_form'] = HomeForm()
	else:
		context['room_form'] = RoomForm()
	return render(request, 'home_space/dashboard.html', context)

def about(request):
	return render(request,'home_space/about.html')

def isMember(user, home):
	return Membership.objects.filter(Q(member=user),Q(household=home))

@login_required
def room(request, room_id):
	space = get_object_or_404(Room,id=room_id)
	if space.home.owner != request.user and not isMember(request.user, space.home):
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
	if request.method == 'POST' and (request.user == home.owner or isMember(request.user,home)):
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
	else:
		messages.error(request, "Sorry you don't have permission to do that.")
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def edit_room(request, room_id):
	space = get_object_or_404(Room,id=room_id)
	if space.home.owner != request.user and not isMember(request.user, space.home):
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
	if request.user != inv.space.home.owner and not isMember(request.user, inv.space.home):
		raise Http404
	context = {'inv': inv}
	return render(request, 'home_space/inventory.html', context)

@login_required
def new_inventory(request, room_id):
	room = get_object_or_404(Room, id=room_id)
	if room.home.owner == request.user or isMember(request.user, room.home):
		if request.method =='POST':
			form  = InventoryForm(data=request.POST)
			if form.is_valid():
				new_inv = form.save(commit=False)
				new_inv.space = room
				new_inv.save()
				return HttpResponseRedirect(reverse('room', args=[room.id]))
	else:
		raise Http404

#------------------------ RECIPES ------------------------
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

#------------------------ FOOD ------------------------
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
		form = FoodForm(instance=food, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('space',args=[food.space.id]))
	context = {'form':form,'food':food}
	return render(request,'home_space/edit_food.html', context)
	
#------------------------ ITEMS ------------------------

def item(request, item_id):
	item = get_object_or_404(Item, id=item_id)
	forsale = item.forsale_set.all()
	ismember = isMember(request.user,item.space.space.home)
	if request.user != item.space.space.home.owner and not forsale:
		raise Http404
	context = {'item':item,'forsale':forsale, 'ismember': ismember}
	return render(request, 'home_space/item.html', context)

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
			return HttpResponseRedirect(reverse('room', args=[item.inventory.space.id]))
	context = {'form':form, 'inventory':space}
	return render(request, 'home_space/new_item.html',context)
	
@login_required
def edit_item(request,item):
	item = get_object_or_404(Item,id=item)
	if item.space.space.home.owner != request.user and not isMember(request.user, item.space.space.home):
		raise Http404
	if request.method != 'POST':
		form = ItemForm(instance=item)
	else:
		form = ItemForm(instance=item,data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('item',args=[item.id]))
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

@login_required
def new_garage_sale(request):
	if request.user.is_authenticated:
		if request.method != 'POST':
			form = GarageSaleForm()
		else:
			form = GarageSaleForm(data=request.POST)
			if form.is_valid():
				sale = form.save(commit=False)
				sale.owner = request.user
				form.save()
				return HttpResponseRedirect(reverse('garage_sale', args=[sale.id]))
	else:
		raise Http404
	context = {'form': form}
	return render(request, 'home_space/new_garage_sale.html', context)

def garage_sales(request):
	sales = GarageSale.objects.all()
	context = {'sales':sales}
	return render(request, 'home_space/garage_sales.html', context)

def garage_sale(request, sale_id):
	items = None
	sale = get_object_or_404(GarageSale, id=sale_id)
	image = ForSale.objects.filter(Q(item__itemimage__image__isnull=False)).first().item.itemimage_set.first().image.url
	context = {'sale': sale, 'image':image}
	if request.user.is_authenticated:
		items = Item.objects.filter(space__space__home__owner=request.user, forsale=None)[:5]
		context['item_form'] = GarageSaleForm(instance=sale)
		context['ismember'] = isMember(request.user, sale.home)
	context['items'] = items
	return render(request, 'home_space/garage_sale.html', context)

@login_required
def get_items(request):
	if request.user.is_authenticated and request.is_ajax():
		items = Item.objects.filter(space__space__home__owner__id=request.user.id)
		html = render_to_string(template_name='home_space/item_search_inject.html', context={'items':items})
		data = {"item_results_view":html}
		return JsonResponse(data=data, safe=False)

@login_required
def add_item(request, sale_id, item_id):
	sale = get_object_or_404(GarageSale, id=sale_id)
	item = get_object_or_404(Item, id=item_id)
	if request.is_ajax() and request.user == sale.owner:
		if item.forsale_set.all():
			messages.error(request, "This item is already for sale.")
			return JsonResponse({"error":""}, status=400)
		else:
			new_sale = ForSale.objects.create(vendor=sale, item=item)
			new_sale.save()
			url = reverse('item', args=[item.id])
			serialized = serializers.serialize('json', [ item,])
			return JsonResponse({"item":serialized, "url": url},status=200)
	else:
		return JsonResponse({"error":""}, status=400)

@login_required
def new_item_image(request, item_id):
	item = get_object_or_404(Item, id=item_id)
	if request.method != 'POST':
		data={'item':item}
		form = ItemImageForm(initial=data)
	else:
		if not request.FILES:
			messages.error(request,'No Image was provided')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		form = ItemImageForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			new_image = form.save(commit=False)
			new_image.item = item
			new_image.save()
			messages.success(request, 'The Image has been added')
			return HttpResponseRedirect(reverse('item', args=[item.id]))
	context = {'form':form, 'item': item}
	return render(request, 'home_space/new_item_image.html', context)

@login_required
def edit_sale(request, sale_id):
	sale = get_object_or_404(GarageSale, id=sale_id)
	if request.user.is_authenticated and request.user == sale.home.owner or isMember(request.user, sale.home):
		if request.method != 'POST':
			form = GarageSaleForm(instance=sale)
		else:
			form = GarageSaleForm(instance=sale, data=request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('garage_sale', args=[sale.id]))
	else:
		raise Http404
	context = {'form': form, 'sale': sale}
	return render(request, 'home_space/edit_sale.html', context)

@login_required
def delete_sale(request, sale_id):
	sale = get_object_or_404(GarageSale, id=sale_id)
	if request.user.is_authenticated and request.user == sale.owener:
		sale.delete()
		return HttpResponseRedirect(reverse('garage_sales'))
	else:
		raise Http404