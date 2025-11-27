[app]
title = MedicalHelper
package.name = medicalhelper
package.domain = com.medical.helper
version = 1.0.0
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,db
requirements = python3,kivy==2.3.0,pillow==10.1.0,requests==2.31.0,android,pyjnius,plyer
orientation = portrait
fullscreen = 0
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE
android.private_storage = True
android.api = 33
android.minapi = 26
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.sdkmanager_path = /home/runner/.buildozer/android/platform/android-sdk/cmdline-tools/latest/bin/sdkmanager

presplash.filename = %(source.dir)s/assets/presplash.png
icon.filename = %(source.dir)s/assets/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
timeout = 7200
cache_dir = .buildozer/cache
bin_dir = bin