from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('api/clothing/', views.AddClothingWithImageView.as_view(), name='add-clothing'),
    path('api/get_clothing/', views.get_clothes, name='get_clothing'),  # NEW GET endpoint
    path('api/create_user/', views.create_user, name='create_user'),
    path('api/get_closets/', views.get_closets, name='get_closets'),
    path('api/login/', views.login_user, name='login_user'),
    path('api/csrf_token/', views.get_csrf_token, name='csrf_token'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
