"""
URL configuration for thumbnails_service project.

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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from thumbnails_app import views

urlpatterns = [
    path('', views.submit_thumbnail_request, name='submit_thumbnail'),
    path('account/', views.account_page, name='account_page'),
    
    # Include Django's authentication URLs (for login, logout, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('accounts/signup/', views.signup, name='signup'),     

    path('admin/', admin.site.urls), 

    path('payment/create/', views.create_payment, name='create_payment'),
    path('payment/execute/', views.execute_payment, name='execute_payment'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
