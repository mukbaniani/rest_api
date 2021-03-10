from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Category, Comment, Post
from .serializers import CommentSerializer, PostSerializers, CategorySerializer, RegistrationSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework import generics, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class CommentMain(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk']
        comments = Comment.objects.filter(post_id=post_id)
        return comments


class CommentListView(CommentMain, mixins.ListModelMixin):

    def get(self, request, pk):
        return self.list(request, pk)


class CommentSave(CommentMain, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        return self.create(request)


class CommentPutAndDeleteReqeust(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.user != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return self.update(request, pk)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.user != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, pk)


class PostListView(APIView):
    
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializers(posts, many=True)
        return Response(serializer.data)


class PostSave(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
        return Response(serializer.data)


class PostPutAndDeleteRequest(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializers(instance=post, data=request.data)
        if post.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response('post deleted')


@api_view(['GET'])
def home(request):
    categories = Category.objects.all().annotate(post_sum = Count('post'))
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(instance=category, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return Response('category deleted')


@api_view(['POST'])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        token = Token.objects.get(user=account).key
        data['token'] = token
    return Response(data)


@api_view(['GET'])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)