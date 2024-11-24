import django.urls as urls
from . import views

urlpatterns = [
    urls.path('register/', views.register_user_api_view),
    urls.path('auth/', views.authorization_api_view),
    urls.path('confirm/', views.confirmation_code_api_view),
    
]