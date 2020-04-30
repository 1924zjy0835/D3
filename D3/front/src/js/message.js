// 错误信息提示框

function Message() {
    this.isAppended = false;
    this.wrapperHeight = 48;
    this.wrapperWidth = 300;
    this.initStyle();
    this.initElement();
    this.listenCloseEvent();
}

Message.prototype.initStyle = function () {
    var self = this;
    self.errorStyle = {
        'wrapper': {
            'background': '#f2dede',
            'color': '#993d3d',
        },
        'close': {
            'color': '#993d3d'
        }
    };

    self.successStyle = {
        'wrapper': {
            'background': '#dff0d8',
            'color': '#468847',
        },
        'close': {
            'color': "#468847"
        }
    };

    self.infoStyle = {
        'wrapper': {
            'background': '#d9edf7',
            'color': '#5bc0de',
        },
        'close': {
            'color': '#5bc0de',
        }
    };
};


Message.prototype.initElement = function () {
    var self = this;
    self.wrapper = $("<div></div>");
    self.wrapper.css({
        'font-size': '14px',
        'width': '350px',
        'height': '48px',
        'padding': '10px',
        'z-index': '1200',
        'position': 'fixed',
        'box-sizing': 'border-box',
        'border': '1px solid #ddd',
        'border-radius': '4px',
        'left':'50%',
        'top': '0',
        'margin-left': '-150px',
        'line-height': '24px',
        'font-weight': 700
    });


    self.closeBtn = $("<span>×</span>");
    self.closeBtn.css({
        'font-family': 'core_sans_n45_regular, "Avenir Next", "Helvetica Neue", Helvetica, Arial, "PingFang SC", "Source Han Sans SC","Hiragino Sans GB", "Microsoft YaHei", "WengQuanYi MicroHei", sans-serif;',
        'font-weight': '700',
        'float': 'right',
        'cursor': 'pointer',
        'font-size': '18px',
    });

    self.messageSpan = $("<span class='ant-message-group'></span>");

    self.wrapper.append(self.messageSpan);
    self.wrapper.append(self.closeBtn);
};


Message.prototype.listenCloseEvent = function () {
    var self = this;
    self.closeBtn.click(function () {
        self.wrapper.animate({'top': -self.wrapperHeight});
    });
};


Message.prototype.showError = function(message) {
    this.show(message, 'error');
};


Message.prototype.showSuccess = function (message) {
    this.show(message, 'success');
};


Message.prototype.showInfo = function (message) {
    this.show(message, 'info');
};


Message.prototype.show = function (message, type) {
    var self = this;
    if(!self.isAppended) {
        $(document.body).append(self.wrapper);
        self.isAppended = true;
    }

    self.messageSpan.text(message);

    // 后来添加的相关判断
    if (type === 'error') {
        self.wrapper.css(self.errorStyle['wrapper']);
        self.closeBtn.css(self.errorStyle['close']);
    } else if (type === 'info') {
        self.wrapper.css(self.infoStyle['wrapper']);
        self.closeBtn.css(self.infoStyle['close']);
    } else {
        self.wrapper.css(self.successStyle['wrapper']);
        self.closeBtn.css(self.successStyle['close']);
    }

    self.wrapper.animate({"top": 0}, function () {
        setTimeout(function () {
            self.wrapper.animate({"top":-self.wrapperHeight});
        }, 3000);
        // 在显示错误信息之后3s，将当前的页面重新加载
        // window.location.reload();
    });
};


window.messageBox = new Message();