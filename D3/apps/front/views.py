from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_GET, require_POST

import os
from django.conf import settings

from utils.captcha import restful

from .models import PhotosModel, User
from .forms import PhotoForm, ExtractDataForm

from .serializers import PhotoSerlizer

import numpy as np
import cv2 as cv
import urllib.request as urllib


def index(request):
    return render(request, 'front/index.html')


def photoFit(request):
    return render(request, 'front/photofit.html')


def StorageRoom(request):
    return render(request, 'front/storageRoom.html')


# 将图片数据进行序列化操作
def photo_list(request):
    photos = PhotosModel.objects.all()
    serializers = PhotoSerlizer(photos, many=True)

    return restful.httpResult(data=serializers.data)


# 定义上传图片到本地服务器的视图函数
@require_POST
def upload_file(request):
    # 从request.FILES中获取真实的文件，这个字典的me以一个输入都是Uploadfile的对象
    # 一个上传文件的简单包装
    files = request.FILES.get("file")
    name = files.name

    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in files.chunks():
            fp.write(chunk)
        fp.close()

    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return restful.httpResult(data={"url": url})


# 将前端提交的数据保存到数据库中
def photoSave(request):
    form = PhotoForm(request.POST)
    if form.is_valid():
        img_url = form.cleaned_data.get("img_url")
        photo = PhotosModel.objects.create(img_url=img_url)
        return restful.httpResult(data={'photo_id': photo.pk})
    else:
        return restful.params_error(message=form.errors.get_json_data())


# 定义删除photo视图函数
def photo_del(request):
    photo_id = request.POST.get('photo_id')
    print(photo_id)
    PhotosModel.objects.filter(pk=photo_id).delete()
    return restful.httpResult(message="您要删除的照片已经删除成功了~~")


# 定义提取照片数据视图函数
def extract_data(request):
    form = ExtractDataForm(request.POST)
    if form.is_valid():
        img_url = form.cleaned_data.get('img_url')
        resp = urllib.urlopen(img_url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv.imdecode(image, cv.IMREAD_COLOR)
        dst_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        return restful.httpResult(data={'dst_image': dst_image})
    else:
        return restful.params_error(message=form.errors.get_json_data())

