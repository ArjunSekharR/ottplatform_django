from django.contrib import admin
from django.urls import path,include
from movieapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.loginpage, name='loginpage'),
    path('movielist/', views.homepage, name='movielist'),
    path('passwordreset/<str:key>/', views.forgotpassword, name='pswd_forgot'),
    path('confirmpassword', views.confirmpassword, name='reset_password'),
    path('subs_plan', views.subs_plan, name='plans'),
    path('add_movie', views.addnew_movie, name='add'),
    path('edit_movie/<int:id>/', views.movie_edit, name='movie_edit'),
    path('delete_movie/<int:id>/', views.delete_movie, name='delete_movie'),
    path('search',views.search_movies,name='search_movies'),
    path('logout', views.movie_logout, name='logout'),
    path('movieview/<int:id>/', views.movie_views, name='movie_view'),
    path('view_plan/<int:id>/', views.plan_views, name='plan_view'),
    path('userlist', views.user_list, name='userlist'),
    path('month_subs', views.monthly_subs, name='subscibers'),
    path('revenue', views.total_revenue, name='revenue'),
    path('viewed_most', views.most_viewed, name='viewed_most'),
    path('rated', views.rated_movie, name="rate"),
    path('add_plan', views.add_plan, name='add_plan'),
    path('history/<int:id>/', views.watch_history, name='watch'),
    path('api_ott/',include('api_ott.urls')),
    path('plantoogle/<int:pk>/',views.plantoogle,name='plantoogle'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)

