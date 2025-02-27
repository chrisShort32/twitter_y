from django.urls import path
from . import views
from .views import UserInfoView
urlpatterns = [
    path('all_users/', views.all_users, name='all_users'),
    path('api/user/<str:username>', UserInfoView.as_view(), name='user-info'),
    path('api/user/<str:username>/<str:checkInfo>/', views.get_user_info, name='get_user_info'),

]
