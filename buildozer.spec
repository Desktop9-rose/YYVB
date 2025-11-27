[app]
# 基础配置（简化+标准化）
title = 医疗报告助手
package.name = medicalhelper
package.domain = com.medical.helper
version = 1.1.0
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,db

# 依赖配置（轻量化+版本固化）
requirements = python3,kivy==2.3.0,pillow==10.1.0,requests==2.31.0,cryptography==41.0.7,android,pyjnius,plyer

# 界面/权限配置
orientation = portrait
fullscreen = 0
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE
android.private_storage = True

# Android核心配置（适配SDK/NDK）
android.api = 33
android.minapi = 26
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a  # 新版架构，适配性强
android.accept_sdk_license = True
# 强制指定sdkmanager路径（兜底兼容）
android.sdkmanager_path = /home/runner/.buildozer/android/platform/android-sdk/cmdline-tools/latest/bin/sdkmanager

[buildozer]
log_level = 2
warn_on_root = 1
timeout = 7200
cache_dir = .buildozer/cache
bin_dir = bin