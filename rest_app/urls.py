from django.urls import path
from . import views
from .views import PostShowSaveView, PostPutAndDeleteRequest, CommentGetPostRequest, CommentPutAndDeleteReqeust
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [ 
    path('', views.home, name='home-page'),
    path('create-category', views.create_category, name='create-category'),
    path('update-category/<int:pk>', views.update_category, name='update-catogory'),
    path('delete-category/<int:pk>', views.delete_category, name='delete-category'),
    path('register-user', views.register_user, name='register-user'),
    path('login/', obtain_auth_token, name='login'),
    path('logout', views.logout, name='logout'),
    path('post-list', PostShowSaveView.as_view(), name='post-show-save'),
    path('post-delete-put/<int:pk>', PostPutAndDeleteRequest.as_view(), name='post-delete-put-request'),
    path('comment-show-save/<int:pk>', CommentGetPostRequest.as_view(), name='comment-show-save'),
    path('comment-delete-put-request/<int:pk>', CommentPutAndDeleteReqeust.as_view(), name='comment-put-delete-request')
]