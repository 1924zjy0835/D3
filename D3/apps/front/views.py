from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_GET, require_POST

import os
from django.conf import settings

from utils.captcha import restful

from .models import PhotosModel, User, PersonModelsModel
from .forms import PhotoForm, ExtractDataForm

from .serializers import PhotoSerlizer, ModelPhotoSerlizer

import numpy as np
import cv2 as cv
import urllib.request as urllib

from apps.algorithm import CNN
from apps.algorithm import canny
from apps.algorithm import skeletonize
from apps.algorithm import Harris
from apps.algorithm import ShiTomasi
from apps.algorithm import SIFT
from apps.algorithm import FAST
from apps.algorithm import ORB

from datetime import datetime


def index(request):
    return render(request, 'front/index.html')


def photoFit(request):
    return render(request, 'front/photofit.html')


def StorageRoom(request):
    models = PersonModelsModel.objects.all()
    for model in models:
        print(model)

    context = {
        'models': models
    }
    return render(request, 'front/storageRoom.html', context=context)


def ModelFittingRoom(request):
    return render(request, 'front/modelFittingRoom.html')


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
    PhotosModel.objects.filter(pk=photo_id).delete()
    return restful.httpResult(message="您要删除的照片已经删除成功了~~")


# 定义提取照片视图函数
def extract_data(request):
    form = ExtractDataForm(request.POST)
    if form.is_valid():
        img_url = form.cleaned_data.get('img_url')
        # resp = urllib.urlopen(img_url)
        # image = np.asarray(bytearray(resp.read()), dtype="uint8")
        # image = cv.imdecode(image, cv.IMREAD_COLOR)
        # dst_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # dst_image = CNN.imread_image(img_url)
        #
        # # 自定义卷积核
        # # kernel 是一个3*3的边缘特征提取器，可以提取各个方向上的边缘
        # # kernel2 是一个5*5的浮雕特征提取器
        #
        # # kernel 之和为0、或小于0的时候，为黑色
        # # kernel 之和大于0的时候为彩色
        # kernel = np.array([
        #     [1, 1, 1],
        #     [1, -8, 1],
        #     [1, 1, 1]
        # ])
        #
        # res = CNN.conv(dst_image, kernel, 'fill')


        # 使用canny算法对图像进行处理
        # dst_img = canny.canny_imread(img_url)

        # OpenCV库计算生态骨架（morphological  skeleton）
        dst_img = skeletonize.read_image(img_url)


        # 检测骨架的关键点
        # dst_img = Harris.Harris(img)
        # img = ShiTomasi.ShiTomasi(img_url)
        # dst_img = SIFT.sift(img_url)
        # dst_img = FAST.fast(img_url)
        # dst_img = ORB.orb(img_url)

        ROOT = settings.MEDIA_ROOT

        cv.imwrite(os.path.join(ROOT, 'modelPerson04.jpg'), dst_img)
        url = request.build_absolute_uri(settings.MEDIA_URL + 'modelPerson04.jpg')

        # cv.imshow("dst_image", dst_image)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        # 保存经过处理的照片
        PersonModelsModel.objects.create(model_url=url)

        # modelPhotos = PhotosModel.objects.all()
        # serializers = ModelPhotoSerlizer(modelPhotos, many=True)
        # dataSer = serializers.data
        # dataSer['model_url'] = url
        return restful.httpResult(message="图片处理完成，已保存！")
    else:
        return restful.params_error(message=form.errors.get_json_data())


# 将模型图片进行序列化
def modelPhoto_serialize(request):
    modelPhotos = PersonModelsModel.objects.all()
    serializers = ModelPhotoSerlizer(modelPhotos, many=True)
    return restful.httpResult(data=serializers.data)


# 删除创建的Person模型
def model_del(request):
    model_id = request.POST.get("model_id")
    print("hhhhhh")
    PersonModelsModel.objects.filter(pk=model_id).delete()
    return restful.httpResult(message="您要删除的模型已经删除成功了~~")