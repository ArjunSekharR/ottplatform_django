from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view, permission_classes # type: ignore
from rest_framework.permissions import AllowAny # type: ignore
from .serializer import UserSerializer,MovieSerializer,PlanSerializer
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND # type: ignore
from django.contrib.auth.hashers import make_password
from movieapp.models import AdminLogin,MovieList,PlanModel
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token # type: ignore # 

@api_view(['POST'])
@permission_classes((AllowAny,))
def moviesignup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user_data = serializer.validated_data
        if AdminLogin.objects.filter(email=user_data['email']).exists():
            return Response({'errors': {'email': 'Email already exists'}}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        user.password = make_password(user_data['password'])
        user.save()
        return Response({'message': 'You have successfully signed up'}, status=status.HTTP_201_CREATED)
    return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login_page(request):
    username = request.data.get('email')
    password = request.data.get('password')
    if username is None or password is None:
        return Response({'error':'please provide username and password'},
                        status = HTTP_400_BAD_REQUEST)
    user = authenticate(username = username, password=password)
    if not  user:
        return Response({'error':'Invalid Credentials'},
                        status = HTTP_400_BAD_REQUEST)
    token, _=Token.objects.get_or_create(user=user)
    return Response({'token':token.key},status = HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_Movie(request):
    movies = MovieList.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_views(request, id):
    print("movieview")
    print(id)
    movie = get_object_or_404(MovieList, pk=id)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

@api_view
@permission_classes([AllowAny])
def planlist(request):
    plans =  PlanModel.objects.all()
    serializer = PlanSerializer(plans, many = True)
    return Response(serializer.data)








