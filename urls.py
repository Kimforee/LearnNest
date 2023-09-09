from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('flash_message/',views.flashMessage,name='flash-message'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerPage,name='register'),
    path('nest/<str:pk>/',views.nest,name='nest'),
    path('profile/<str:pk>/',views.userProfile,name='user-profile'),
    path('create-nest/',views.createNest,name='create-nest'),
    path('update-nest/<str:pk>/',views.updateNest,name='update-nest'),
    path('delete-nest/<str:pk>/',views.deleteNest,name='delete-nest'),
    path('all-requests/<str:pk>/',views.allRequests,name='all-requests'),
    path('accept-join-request/<str:pk>/',views.acccept_join_request,name='accept-join-request'),
    path('reject-join-request/<str:pk>/',views.reject_join_request,name='reject-join-request'),
    path('delete-message/<str:pk>/',views.deleteMessage,name='delete-message'),
]