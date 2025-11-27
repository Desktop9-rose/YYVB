[app]
title = MedicalHelper
package.name = medicalhelper
package.domain = com.medical.helper
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,db,key
version = 1.0.0
requirements = python3,kivy==2.3.0,requests==2.31.0,android,pyjnius,plyer,pillow==10.1.0
orientation = portrait
fullscreen = 0
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2