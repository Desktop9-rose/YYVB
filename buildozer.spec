[app]
# 基础配置（彻底删除行内注释，仅保留纯配置）
title = 医疗报告助手
package.name = medicalhelper
package.domain = com.medical.helper
version = 1.0.0
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,db

# 依赖配置（无行内注释）
requirements = python3,kivy==2.3.0,pillow==10.1.0,requests==2.31.0,cryptography==41.0.7,android,pyjnius,plyer

# 界面/权限配置
orientation = portrait
fullscreen = 0
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE
android.private_storage = True

# Android核心配置（关键：删除所有行内注释！）
android.api = 33
android.minapi = 26
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a  # 注释单独换行（或直接删除注释）
android.accept_sdk_license = True
android.sdkmanager_path = /home/runner/.buildozer/android/platform/android-sdk/cmdline-tools/latest/bin/sdkmanager

[buildozer]
log_level = 2
warn_on_root = 1
timeout = 7200
cache_dir = .buildozer/cache
bin_dir = bin