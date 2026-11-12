[app]
title = VotaFacil Mobile
package.name = votafacil
package.domain = org.votafacil
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,requests,urllib3,idna,certifi,charset-normalizer,supabase,httpx,httpcore,anyio,sniffio,h11,pydantic,pydantic_core,typing_extensions,annotated_types,postgrest,gotrue,realtime,storage3,supafunc
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
