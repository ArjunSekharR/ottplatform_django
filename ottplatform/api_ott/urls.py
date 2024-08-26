from django.urls import path
from .import views

urlpatterns = [
    path('signupapi/',views.moviesignup),
    path('loginapi/',views.login_page),
    path('listapi',views.list_Movie),
    path('movieview/<int:id>/', views.movie_views, name='movieview'),
    path('my_plan',views.planlist,name='myplan')
]