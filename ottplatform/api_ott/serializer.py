from rest_framework import serializers # type: ignore
from movieapp.models import AdminLogin,MovieList,PlanModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminLogin
        fields = ['username', 'email', 'password']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieList
        fields = ['id','title','thumbnail','video','description']

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanModel
        fields = ['id','plan_name','description','price','duration']