[app]
title = 医疗报告助手
package.name = medicalhelper
package.domain = com.medical
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,kv,db
version = 1.0.0
requirements = python3,kivy==2.3.0,pillow==10.1.0,requests==2.31.0,cryptography==41.0.5,plyer==2.1.0,urllib3==1.26.18
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.3.0
fullscreen = 0
android.api = 21
android.minapi = 21
android.sdk = 28
android.ndk = 25b
android.arch = armeabi-v7a
android.allow_backup = True
android.buildtools = 33.0.0
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET,ACCESS_NETWORK_STATE
android.gradle_dependencies =
android.resources =
p4a.hook =
p4a.bootstrap = sdl2
p4a.icon.filename = icon.png
android.add_src =
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false

[buildozer]
log_level = 2
warn_on_root = 1