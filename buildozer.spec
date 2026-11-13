[app]

# (str) Title of your application
title = VotaFácil Mobile

# (str) Package name
package.name = votafacil

# (str) Package domain (needed for android packaging)
package.domain = org.compu2980

# (str) Source files to include (let it default or specify extensions)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to include (let it default to all files matching the source.include_exts filter)
source.include_patterns = assets/*,*.py

# (list) Application requirements
# Incluye Kivy, Python y todas las librerías necesarias para conectar con Supabase
requirements = python3,kivy,requests,urllib3,idna,certifi,charset-normalizer,supabase

# (str) Supported orientations (portrait, landscape or all)
orientation = portrait

# (list) List of service to declare
#services = 

#
# Android specific
#

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use AndroidX support
android.androidx = True

# (str) The format used to package the app for android
android.presplash_color = #FFFFFF
