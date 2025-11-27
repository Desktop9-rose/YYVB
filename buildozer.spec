# Buildozer spec file (UTF-8编码，无BOM，语法严格兼容Buildozer 1.5.0)
[app]
# 基础必填配置（核心：版本号行无多余空格/符号）
title = 医疗报告助手
package.name = medicalhelper
package.domain = com.medical
version = 1.0.0
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,kv,db

# 依赖（版本固化，避免兼容问题）
requirements = python3,kivy==2.3.0,pillow==10.1.0,requests==2.31.0,cryptography==41.0.5,plyer==2.1.0,urllib3==1.26.18

# 界面配置
orientation = portrait
fullscreen = 0

# Android核心配置（适配GitHub Actions环境）
android.api = 33
android.minapi = 26
android.ndk = 25b
android.sdk = 33
android.buildtools = 33.0.0
android.arch = armeabi-v7a
android.allow_backup = True
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET,ACCESS_NETWORK_STATE
# 字体/assets打包（确保自定义字体加载）
android.add_assets = fonts/
# Android 13+存储权限兼容
android.add_android_manifest_activities = android:requestLegacyExternalStorage="true"
# 跳过字节编译，加速构建
android.skip_byte_compile = 1
# 自动接受SDK许可证
android.accept_sdk_license = True

# 非必要配置（仅保留Android相关，移除iOS/OSX无关配置减少解析风险）
p4a.bootstrap = sdl2
p4a.icon.filename = icon.png

[buildozer]
# 日志级别（调试用）
log_level = 2
# 根用户警告
warn_on_root = 1
# 缓存配置（加速重复构建）
cache_dir = .buildozer/cache
bin_dir = bin
# 超时配置（避免SDK下载中断）
timeout = 3600
# 强制使用指定配置文件路径（解决路径解析问题）
spec_file = buildozer.spec