from django.shortcuts import render
from django.contrib.auth import get_user_model
from datetime import datetime
from rest_framework import filters, generics, permissions, viewsets, permissions, status
from .models import Post
from .permissions import IsAuthorOrReadOnly, IsAssigned
from .serializers import PostSerializer, UserSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import HTMLFormRenderer,JSONRenderer,BrowsableAPIRenderer
from rest_framework.response import Response

class PostList(APIView):
    serializer_class = PostSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        snippets = Post.objects.all()
        serializer = PostSerializer(snippets,many=True)
        html = Response(serializer.data)
        if request.COOKIES.get('visits'):
            html.set_cookie('dataflair', 'Witaj z powrotem!')
            value = int(request.COOKIES.get('visits'))
            html.set_cookie('visits', value + 1)
            return html
        else:
            value = 1
            text = "Witaj po raz 1!"
            html.set_cookie('visits', value)
            html.set_cookie('dataflair', text)
            return html

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,IsAuthorOrReadOnly)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter ,filters.OrderingFilter]
    search_fields = ['title']

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,IsAuthorOrReadOnly)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter ,filters.OrderingFilter]
    search_fields = ['username']

class UserList(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer