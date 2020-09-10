from django.shortcuts import render, redirect
from .models import Space, Item, Food
from .forms import SpaceForm, ItemForm, FoodForm
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

def about(request):
	return render(request,'home_space/about.html')

@login_required
def space(request, space):
	space = Space.objects.get(id=space)
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

@login_required
def edit_space(request, space):
	space = Space.objects.get(id=space)
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