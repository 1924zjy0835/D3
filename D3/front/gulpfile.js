var gulp = require('gulp');
var cssnano = require('gulp-cssnano');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var bs = require('browser-sync').create();
var imagemin = require('gulp-imagemin');
var cache = require('gulp-cache');
var connect = require('gulp-connect');
var concat = require('gulp-concat');
// 将scss文件转换为css
var scss = require('gulp-sass');
// 定位出错的文件的未经压缩过的源文件的行数
var sourcemaps = require("gulp-sourcemaps");
// gulp-util插件中的log方法可以打印出错误信息，而不是直接退出gulp
var util = require("gulp-util");


//Define the path
var path = {
    'html': './templates/**/',
    'css': './src/css/**/',
    'js': './src/js/**/',
    'images': './src/images/**/',
    'css_dist': './dist/css/',
    'js_dist': './dist/js/',
    'images_dist': './dist/images/'
};


//Define a html task
gulp.task('html', function () {
    gulp.src(path.html + '*.html')
        .pipe(bs.stream())
});


// Define a css task
gulp.task('css', function () {
    gulp.src(path.css + '*.scss')
        .pipe(scss().on('error', scss.logError))
        .pipe(cssnano())
        .pipe(rename({"suffix": ".min"}))
        .pipe(gulp.dest(path.css_dist))
        .pipe(bs.stream())
});


//Define a js task
gulp.task('js', function () {
    gulp.src(path.js + '*.js')
        .pipe(sourcemaps.init())
        .pipe(uglify().on("error", util.log))
        .pipe(rename({'suffix': '.min'}))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream())
});


//Define a images task
gulp.task('images', function () {
    gulp.src(path.images + '*.*')
        .pipe(cache(imagemin()))
        .pipe(rename({"suffix": ".min"}))
        .pipe(gulp.dest(path.images_dist))
        .pipe(bs.stream())
});


//Define a watch task
gulp.task('watch', function () {
    gulp.watch(path.html + '*.html', ['html']);
    gulp.watch(path.css + '*.scss', ['css']);
    gulp.watch(path.js + '*.js', ['js']);
    gulp.watch(path.images + '*.*', ['images']);
});


// Init a servser's task
gulp.task('bs', function () {
    bs.init({
        'server': {
            'baseDir': './'
        }
    });
});


// Define a default task
// gulp.task('default', ['bs','watch']);
gulp.task("default", ["watch"]);