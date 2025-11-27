# Buildozer spec file
[app]

# (str) Title of your application
title = Medical Helper

# (str) Package name (小写、无空格，符合Android包名规范)
package.name = medicalhelper

# (str) Package domain (建议改为更规范的格式，如 org.你的名称.medicalhelper，也可保留test)
package.domain = org.test

# (必填) 应用版本号（解决构建时报错的核心项）
package.version = 1.0.0

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) Application requirements (补充版本兼容性，避免依赖下载失败)
requirements = python3,kivy==2.3.0,requests==2.31.0,pillow==10.1.0,cryptography==41.0.7,android

# (list) Permissions (适配Android 13+权限规范，补充权限描述)
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE
# Android 13+ 存储权限兼容
android.add_android_manifest_activities = android:requestLegacyExternalStorage="true"

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 26

# (str) Android NDK version to use (指定完整版本，避免自动下载错误版本)
android.ndk = 25b

# (bool) Skip byte compile for .py files
android.skip_byte_compile = 1

# (新增) 解决kivy字体缺失问题（可选，根据你的项目是否使用自定义字体调整）
android.add_assets = fonts/

# (新增) 启用日志输出，方便调试
android.logcat_filters = *:S python:D

# (新增) 构建模式（debug用于测试，release用于发布）
android.release = False

# (list) 排除不需要打包的文件/目录（可选，根据你的项目调整）
source.exclude_dirs = venv,.git,.github,__pycache__

# (list) 排除不需要打包的文件后缀
source.exclude_exts = spec,md,log

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (新增) 缓存构建依赖（加速后续构建）
cache_dir = .buildozer/cache

# (新增) 构建输出目录
bin_dir = bin

# (新增) 超时时间（避免Android SDK下载超时）
timeout = 3600