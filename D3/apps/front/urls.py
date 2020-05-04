from django.urls import path
from .import views

app_name = "front"

urlpatterns = [
    path('',views.index, name='front_index'),
    path('storage/room/',views.StorageRoom, name='storage_room'),
    path('photo/fit/',views.photoFit, name='photoFit'),
    path('model/fit/room/',views.ModelFittingRoom, name='model_fit_room'),
    path('photo/list/',views.photo_list, name='photoList'),
    path('upload/file/',views.upload_file, name='upload_file'),
    path('save/photo/',views.photoSave, name='photo_save'),
    path('del/photo/',views.photo_del, name='photo_del'),
    path('extract/data/',views.extract_data, name='extract_data'),
    path('model/serialize/', views.modelPhoto_serialize, name='model_serialize'),
    path('del/model/', views.model_del, name='model_del'),
]
