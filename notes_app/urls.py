from django.urls import path 

from . import views

urlpatterns = [

   # path('upload_file', views.upload_file, name='upload_file'),
   path('download/<str:file_name>/', views.download_file, name='download_file'),
   path('views_files/', views.view_files, name='view_files'),
   path('base', views.base, name='base'),
   path('settings/', views.setts, name='settings'),
   # path('fetch_data/', views.fetch_data, name='fetch_data'),
   path('new-table/', views.new_table, name='new-table'),
   path('contact/', views.contact, name='contact'),
   path('post/<int:pk>/', views.post_detail, name='post_detail'),
   path('', views.home, name='home'),


]