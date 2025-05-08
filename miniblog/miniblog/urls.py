from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),  # ← сіздің blog app маршруты
    path('api/auth/', obtain_auth_token),  # ← МІНЕ ОСЫ МАҢЫЗДЫ
]
