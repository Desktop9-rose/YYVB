[app]
# 应用基础配置
title = 医疗报告助手
package.name = medicalhelper
package.domain = com.medical
package.version = 1.0.0  # 必选：修复版本号缺失报错
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,kv,db

# 依赖（与YAML中安装版本一致）
requirements = python3,kivy==2.3.0,pillow==10.1.0,requests==2.31.0,cryptography==41.0.5,plyer==2.1.0,urllib3==1.26.18

# 界面配置
orientation = portrait
fullscreen = 0

# Android核心配置（适配GitHub Actions环境）
android.api = 33          # 升级到稳定版API
android.minapi = 26       # 兼容更多设备
android.ndk = 25b         # 与buildozer 1.5.0兼容的NDK版本
android.sdk = 33          # 匹配API版本
android.buildtools = 33.0.0
android.arch = armeabi-v7a
android.allow_backup = True
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET,ACCESS_NETWORK_STATE
# 字体/assets打包（关键：确保自定义字体能被加载）
android.add_assets = fonts/
# 存储权限兼容Android 13+
android.add_android_manifest_activities = android:requestLegacyExternalStorage="true"

# 非必要配置（保留但不影响Android构建）
osx.python_version = 3
osx.kivy_version = 2.3.0
p4a.bootstrap = sdl2
p4a.icon.filename = icon.png  # 若无图标可注释，不影响构建
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false

[buildozer]
log_level = 2
warn_on_root = 1
cache_dir = .buildozer/cache  # 缓存依赖，加速重复构建
bin_dir = bin
timeout = 3600               # 延长超时，避免SDK下载中断