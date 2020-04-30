from rest_framework import serializers
from .models import PhotosModel, PersonModelsModel


class PhotoSerlizer(serializers.ModelSerializer):
    class Meta:
        model = PhotosModel
        fields = ('id', 'position', 'img_url')


class ModelPhotoSerlizer(serializers.ModelSerializer):

    class Meta:
        model = PersonModelsModel
        fields = ('id', 'model_url')