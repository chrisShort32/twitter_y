from django.urls import path
from . import views
from .views import UserInfoView, AllUsersView, AllFollowsView
urlpatterns = [
    path('all_users/', views.all_users, name='all_users'),
    path('api/user/<str:username>', UserInfoView.as_view(), name='user-info'),
    path('api/user/<str:username>/<str:checkInfo>/', views.get_user_info, name='get_user_info'),
    path('api/users/', AllUsersView.as_view(), name='all-users-api'),
    path('api/follows/', AllFollowsView.as_view(), name='all-follows-api'),
    path('api/username/<int:user_id>/', views.get_username_by_user_id, name='get-username-by-id'),
    path('api/follow-usernames/<int:follow_id>/', views.get_usernames_for_follow, name='get-follow-usernames'),
]
