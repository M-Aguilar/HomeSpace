from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard',views.dashboard,name='dashboard'),

    #SPACE PAGES
    path('space/<space>',views.space,name='space'),
    path('new_space',views.new_space,name='new_space'),
    path('<space>/new_space', views.new_space,name='new_space'),
    path('edit/<space>',views.edit_space,name='edit_space'),

    #ITEM
    path('<space>/new_item',views.new_item,name='new_item'),
    path('edit_item/<item>',views.edit_item,name='edit_item'),
    path('<item>/delete',views.delete_item,name='delete_item'),

    #FOOD
    path('<space>/new_food',views.new_food,name='new_food'),
    path('edit/<food>',views.edit_food ,name='edit_food'),

    #RECIPES
    path('recipes',views.recipes, name='recipes'),
    path('recipes/<recipe>',views.recipe,name='recipe'),
    path('new_recipe',views.new_recipe, name='new_recipe'),

    #INGREDIENTS
    path('new_ingredient',views.new_ingredient,name='new_ingredient'),

    #ABOUT
    path('about',views.about,name='about'),
]
