[app]

# (str) Title of your application
title = VotaFácil Mobile

# (str) Package name
package.name = votafacil

# (str) Package domain (needed for android packaging)
package.domain = org.votafacil

# (str) Source directory where the app lives
source.dir = .

# (str) Application version (requirements check fix)
version = 0.1

# (list) Source files to include (let it match your project)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (let it match your project)
source.exclude_exts = spec

# (list) List of directory to exclude (let it match your project)
source.exclude_dirs = tests, bin, venv

# (list) Application requirements
requirements = python3,kivy,requests,urllib3,idna,certifi,charset-normalizer

# (str) Supported orientations
orientation = portrait

#
# Android specific
#

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) python-for-android branch to use
p4a.branch = master

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) Permissions
android.permissions = INTERNET

# (str) Bootstrap to use for android build
p4a.bootstrap = sdl2

# (bool) Enable AndroidX support
android.androidx = True


[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_root = 1
