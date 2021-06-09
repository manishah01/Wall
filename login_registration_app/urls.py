from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('user/create', views.create_user),
    path('wall',views.wall),
    path('user/signon',views.log_in),
    path('user/signoff',views.log_out),
    path('wall/post_message',views.post_message),
    path('wall/post_comment/<int:message_id>',views.post_comment),
]