from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard',views.dashboard,name='dashboard'),

    #SPACE PAGES
    path('new_home', views.new_home, name='new_home'),
    path('<home_id>/new_room', views.new_room, name='new_room'),
    path('<room_id>/edit', views.edit_room, name='edit_room'),
    path('room/<room_id>', views.room, name='room'),
    path('room/<room_id>/delete', views.delete_room, name='delete_room'),
    path('room/<room_id>/add_inventory', views.new_inventory, name='new_inventory'),

    path('inventory/<inventory_id>', views.inventory, name='inventory'),

    path('new_garage_sale', views.new_garage_sale, name='new_garage_sale'),

    path('<inventory_id>/new_item',views.new_item,name='new_item'),
    path('edit_item/<item>',views.edit_item,name='edit_item'),
    path('<item>/delete',views.delete_item,name='delete_item'),

    #FOOD
    path('<inventory_id>/new_food',views.new_food,name='new_food'),
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
