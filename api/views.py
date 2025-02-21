from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser

from api.serializers import TodoSerializer
from todo.models import Todo


# Create your views here.

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data =  JSONParser().parse(request)
            user = User.objects.create_user(data['username'], data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error':'username is already taken'}, status=400)

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data =  JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password = data['password'])
        if user is None:
            return JsonResponse({'error':'invalid credentials'}, status=401)

        else:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)




class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer
    #make sure the user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        objects_filter = Todo.objects.filter(user=user, datecompleted__isnull=False).order_by("-datecompleted")
        return objects_filter

class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    #make sure the user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        objects_filter = Todo.objects.filter(user=user, datecompleted__isnull=True)
        return objects_filter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    #make sure the user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        objects_filter = Todo.objects.filter(user=user)
        return objects_filter
