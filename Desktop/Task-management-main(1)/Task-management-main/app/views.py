from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from .models import Teachers
from .models import Task
from .serializers import Taskserializers


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def signup(request):
    name = request.data.get('name')
    school = request.data.get('school')
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password or not name or not school:
        return Response({"error": "Please provide all required fields"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new User object with automatic password hashing
    user = User.objects.create_user(username=username, password=password)

    # Create a new Teacher and link to the User
    teacher = Teachers(user=user, name=name, school=school)
    teacher.save()

    tokens = get_tokens_for_user(user)

    return Response({"success": True, "tokens": tokens})



@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    print(f"Username: {username}")
    print(f"Password: {password}")

    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_task(request):
    serializer = Taskserializers(data=request.data)

    if serializer.is_valid():
        teacher = request.user.teachers #authenticated teacher

        task = serializer.save(Teachers=teacher)

        return Response(Taskserializers(task).data)
    else:
        return Response(serializer.errors)
    
@api_view(['GET'])
def get_task_bydate(request,date):
        task = Task.objects.filter(date=date)
        serializer = Taskserializers(task,many=True)
        return Response(serializer.data)
    
