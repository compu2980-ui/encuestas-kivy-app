[app]

# (str) Title of your application
title = VotaFácil Mobile

# (str) Package name
package.name = votafacil

# (str) Package domain (needed for android packaging)
package.domain = org.votafacil

# (list) Source files to include (let it match your project)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (let it match your project)
source.exclude_exts = spec

# (list) List of directory to exclude (let it match your project)
source.exclude_dirs = tests, bin, venv

# (list) Application requirements
# Note: charset-normalizer is included here safely
requirements = python3,kivy,requests,urllib3,idna,certifi,charset-normalizer,supabase

# (str) Supported orientations
orientation = portrait

# (list) List of services to declare
#services = NAME:ENTRYPOINT_TO_PYTHON_SCRIPT,NAME2:ENTRYPOINT_TO_PYTHON_SCRIPT

#
# Android specific
#

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use (Requerido por p4a moderno)
android.ndk = 25b

# (str) python-for-android branch to use (Corrige incompatibilidades de compilación)
p4a.branch = master

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) Permissions
android.permissions = INTERNET

# (list) pyjnius gnu classpath extra classes
#android.add_jars = foo.jar,bar.jar,path/to/dependency/

# (list) python-for-android git clone to use (optional)
#p4a.fork = 

# (str) Bootstrap to use for android build
p4a.bootstrap = sdl2

# (str) XML misc to add to AndroidManifest.xml
#android.manifest_application_props = 

# (str) Extra XML to add to AndroidManifest.xml manifest section
#android.manifest_manifest_props = 

# (str) Presplash background color
#android.presplash_color = #FFFFFF

# (list) The orientation for the app
#android.orientation = portrait

# (bool) Indicate whether the application is a game or not
#android.game = False

# (str) Gradle dependencies to add
#android.gradle_dependencies = 

# (bool) Enable AndroidX support
android.androidx = True


[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_root = 1
