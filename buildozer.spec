[app]
title = Comandas Coreano
package.name = comandas
package.domain = org.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.ndk = 25b
android.allow_backup = True
android.logcat_filters = *:S python:D