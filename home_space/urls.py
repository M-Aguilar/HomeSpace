from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('new_space',views.new_space,name='new_space'),
    path('<space>/new_space', views.new_space,name='new_space'),
    path('space/<space>',views.space,name='space'),
    path('edit/<space>',views.edit_space,name='edit_space'),
    path('<space>/new_item',views.new_item,name='new_item'),

    path('about',views.about,name='about'),
]
