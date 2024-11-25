import django.urls as urls
from . import views

urlpatterns = [
    urls.path('register/', views.RegisterUserView.as_view()),
    urls.path('auth/', views.AuthorizationView.as_view()),
    urls.path('confirm/', views.ConfirmationCodeView.as_view()),
    
]