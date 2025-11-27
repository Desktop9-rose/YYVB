[app]
# 基础配置（参考成功版简化，移除冗余）
title = 医疗报告助手
package.name = medicalhelper
package.domain = com.medical.helper
version = 1.0.0  # 改用简化的version（成功版用此写法，解析更稳定）
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,db

# 依赖配置（参考成功版轻量化，固化核心版本）
requirements = python3,kivy==2.3.0,pillow==10.1.0,requests==2.31.0,cryptography==41.0.7,android,pyjnius,plyer

# 界面/权限配置（对齐成功版）
orientation = portrait
fullscreen = 0
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE
android.private_storage = True  # 成功版核心配置，提升存储权限兼容性

# Android 核心配置（修复SDK/NDK适配问题）
android.api = 33
android.minapi = 26
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a  # 替换旧架构armeabi-v7a，适配新版SDK
# 关键：指定cmdline-tools路径，解决sdkmanager找不到的问题
android.cmdline_tools_dir = latest
android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk

# (bool) 自动接受SDK许可证（避免交互卡住）
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
# 增加SDK下载超时配置，避免下载中断
timeout = 7200
cache_dir = .buildozer/cache
bin_dir = bin