
// 添加照片
function PhotoFit() {
    this.photoListGroup = $(".photos-list-group");
}

// 加载所有photo事件
PhotoFit.prototype.listenLoadAllDataEvent = function () {
    var self = this;
    antajax.get({
        'url': '/photo/list/',
        'success': function (result) {
            if (result['code'] === 200) {
                var photos = result['data'];
                for (var i=0; i<photos.length; i++) {
                    var photo = photos[i];
                    var tpl = template('photos-item', {'photo': photo});
                    self.photoListGroup.append(tpl);

                    // 为新添加的photo添加关闭、保存事件
                    var photoItem = self.photoListGroup.find(".photos-item:last");
                    self.listenAddImageEvent(photoItem);
                    self.listenCloseBtnEvent(photoItem);
                    self.listenSavePhotoBtnEvent(photoItem);
                }
            }
        }
    });
};

// 限制只能上传6张轮播图事件
PhotoFit.prototype.listenAddBannerUpEvent = function () {
    var self = this;
    var addBtn = $("#add-photo-btn");
    addBtn.click(function () {
        var photoLength = self.photoListGroup.children().length;
        if (photoLength >= 6) {
            window.messageBox.showInfo("只能添加6张图片哦~~");
            return;
        }
        self.createPhotoBtnEvent();
    });
};

// 创建卡片的按钮事件
PhotoFit.prototype.createPhotoBtnEvent = function () {
    var self = this;
    // template()函数返回的是字符串，不能够其添加点击事件，
    // 需要将其添加大网页中，成为网页中的标签
    var tpl = template("photos-item");
    self.photoListGroup.prepend(tpl);

    // 添加点击事件必须在添加tpl到网页中之后
    var photoItem = self.photoListGroup.find(".photos-item:first");

    self.listenAddImageEvent(photoItem);
    self.listenCloseBtnEvent(photoItem);
    self.listenSavePhotoBtnEvent(photoItem);
};

// 添加点击添加图片事件
PhotoFit.prototype.listenAddImageEvent = function (photoItem) {
    var thumbnail = photoItem.find(".thumbnail");
    var imageInput = photoItem.find(".image-input");
    // 也可以通过以下方式照当当前thumbnail同级的image-input
    // var imageInput = thumbnail.siblings(".image-input");

    // 为当前的图片添加点击事件
    thumbnail.click(function () {
        imageInput.click();
    });

    // 为当前选中的图片添加打开事件，即change()事件
    imageInput.change(function () {
        // 获取当前选中的文件
        // this.代表当前的image-input
        var file = this.files[0];
        // 通过FormData()函数创建一个空的对象，之后就可以通过append(),set(),get()等对该对象进行添加，设置，获取操作
        var formData = new FormData();
        // 上传到本地服务器的接口是通过'file'
        formData.append("file", file);
        antajax.post({
            'url': "/upload/file/",
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    var url = result['data']['url'];
                    thumbnail.attr('src',url);
                }
            }
        });
    });
};


// 监听删除卡片的关闭按钮
PhotoFit.prototype.listenCloseBtnEvent = function (photoItem) {
    var self = this;
    // var closeBtn = $(".close-btn");
    var closeBtn = photoItem.find(".close-btn");

    closeBtn.click(function () {
        // var photoItem = $(".photos-item");
        // photoItem.remove();
        var photoId = photoItem.attr("data-photo-id");

        if (photoId) {
            antalert.alertConfirm({
                'text': '您确定要删除该照片吗？无法撤销哦！~~~',
                'confirmCallback': function () {
                    antajax.post({
                        'url': '/del/photo/',
                        'data': {
                            'photo_id': photoId,
                        },
                        'success': function (result) {
                            photoItem.remove();
                            window.messageBox.showSuccess(result['message']);
                        }
                    });
                }
            });
        }else {
            photoItem.remove();
        }
    });
};

// 监听保存卡片的事件
PhotoFit.prototype.listenSavePhotoBtnEvent = function (photoItem) {
    var saveBtn = photoItem.find(".save-btn");
    var thumbnailTag = photoItem.find(".thumbnail");
    saveBtn.click(function () {
        // 获取img图片的src属性对应的值，只需要调用attr()函数就可以了，并不需要调用val()
        var img_url = thumbnailTag.attr("src");
        antajax.post({
            'url': '/save/photo/',
            'data': {
                'img_url': img_url,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    window.messageBox.showSuccess("图片保存成功！");
                } else {
                    console.log(result['code']);
                    console.log(result['message']);
                }
            },
            'fail': function (error) {
                console.log(error['message']);
            }
        });
    });
};


PhotoFit.prototype.listenAddBannerEvent = function () {
    var self = this;
    var addPhotoBtn = $("#add-photo-btn");
    addPhotoBtn.click(function () {
        self.createPhotoBtnEvent();
    });
};


// 提取数据
// function ExtractData() {
//      this.dataListGroup = $(".data-list-group");
// }
//
// // 监听创建模型事件
// ExtractData.prototype.listenAddModelEvent = function () {
//     var self = this;
//
// };
//
// // 提交当前照片
// ExtractData.prototype.listenExtractDataEvent = function () {
//     var self = this;
//
//     var dataItem = self.dataListGroup.find(".data-item:last");
//     var extractDataBtn = dataItem.find(".extract-data-btn");
//
//     extractDataBtn.click(function () {
//         console.log("hello--------");
//         var tpl = template("data-item");
//         self.dataListGroup.prepend(tpl);
//         var thumbnailTag = dataItem.find(".thumbnail");
//
//         // 获取img图片的src属性对应的值，只需要调用attr()函数就可以了，并不需要调用val()
//         var img_url = thumbnailTag.attr("src");
//
//         antajax.post({
//             'url': '/extract/data/',
//             'data': {
//                 'img_url': img_url,
//             },
//             'success': function (result) {
//                 if (result['code'] === 200) {
//                     window.messageBox.showSuccess("图片处理成功！！");
//                     console.log(result['data']['dst_image']);
//                 }
//             }
//         });
//     });
//
// };
//
// ExtractData.prototype.run = function() {
//     this.listenExtractDataEvent();
// };
//
PhotoFit.prototype.run = function () {
    this.listenAddBannerEvent();
    this.listenLoadAllDataEvent();
};

$(function () {
    var photo = new PhotoFit();
    photo.run();

    // var data = new ExtractData();
    // data.run();
});