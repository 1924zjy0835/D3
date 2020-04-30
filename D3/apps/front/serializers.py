from rest_framework import serializers
from .models import PhotosModel


class PhotoSerlizer(serializers.ModelSerializer):
    class Meta:
        model = PhotosModel
        fields = ('id', 'position', 'img_url')