from django import forms
from .models import PhotosModel
from django.views.generic.edit import FormMixin


class PhotoForm(forms.ModelForm, FormMixin):

    class Meta:
        model = PhotosModel
        # 指定当前需要验证的fields必须是元组
        fields = ('img_url',)


class ExtractDataForm(forms.ModelForm, FormMixin):

    class Meta:
        model = PhotosModel
        # 指定当前需要验证的field必须是元组
        fields = ('img_url',)


