from rest_framework import viewsets
from django.shortcuts import render
from .models import Users, Posts, Follows
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse

def all_users(request):
    users = Users.objects.all()
    return render(request, 'all_users.html', {'users': users})

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        users = Users.objects.all().prefectch_related('posts', 'follows')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserInfoView(APIView):
    def get(self, request, username):
        try:
            user = Users.objects.get(username=username)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Users.DoesNotExist:
            return Response({'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)

def get_user_info(request, username, checkInfo):
    # Get the 'info' parameter from the URL (default to 'Follows' if not provided)

    try:
        # Fetch the user object based on the username
        user = Users.objects.get(username__exact=username)
        user_id = user.user_id  # Get the user's ID to use in the queries

        # Determine what data to return based on the 'info' parameter
        if checkInfo == 'Follows':
            # Fetch the list of users who are following the given user (using user_id)
            follows_data = Follows.objects.filter(user_id=user_id)
            data = []
            for follow_data in follows_data:
                user_being_followed = Users.objects.get(user_id=follow_data.following_user_id)
                data.append(user_being_followed.username)
 
        elif checkInfo == 'Following':
            # Fetch the list of users that the given user is following (using user_id)
            following = Follows.objects.filter(following_user_id=user_id)
            data = []
            for follow in following:
                following_user = Users.objects.get(user_id=follow.user_id)
                data.append(following_user.username)

        elif checkInfo == 'Posts':
            # Fetch the user's posts (using user_id)
            posts = Posts.objects.filter(user_id=user_id)
            data = [post.content for post in posts]  # List of posts' content
        else:
            data = []

        return JsonResponse(data, safe=False)

    except Users.DoesNotExist:
        return JsonResponse({"error": "User not found!"}, status=404)
# Create your views here.

import logging

logger = logging.getLogger(__name__)

def get_user_posts(request, username):
    logger.info(f"Received request for username: {username}")

    user = User.objects.filter(username__exact=username).first()
    if not user:
        logger.warning(f"User '{username}' not found.")
        return JsonResponse({'error': 'User not found'}, status=404)

    posts = Post.objects.filter(user=user).values()
    return JsonResponse(list(posts), safe=False)
