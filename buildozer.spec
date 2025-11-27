[app]
title = MedicalHelper
package.name = medicalhelper
package.domain = com.medical.helper
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,db,key
version = 9.0.0
requirements = python3,kivy==2.3.0,requests==2.31.0,android,pyjnius,plyer,pillow==10.1.0
orientation = portrait
fullscreen = 0

# Android 特定配置
android.api = 33
android.minapi = 21
android.sdk = 26
android.ndk = 25b
android.gradle_download = True

# 权限
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.wakelock = False

# 构建配置
android.accept_sdk_license = True

[buildozer]
log_level = 2