"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.urls import include, path
from config.settings import MEDIA_ROOT, MEDIA_URL
urlpatterns = [
    path('message/', include('apps.message.urls'), name="message"),
    path('chat/', include('apps.chat.urls'), name="chat"),
    path('users/', include('apps.users.urls'), name="user"),
    path('auth/', include('apps.auth.urls'),   name="auth"),
    path('', include('core.swagger.swagger'),  name="swagger")
]
urlpatterns+= static(MEDIA_URL, document_root=MEDIA_ROOT)
