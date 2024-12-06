from django.urls import path
from .views import ad_list, ad_create, ad_edit, ad_detail, ad_delete, my_responses, responce_create, \
    subscribe_newsletter, send_newsletter

urlpatterns = [
    path('', ad_list, name='ad_list'),
    path('delete/<int:pk>/', ad_delete, name='ad_delete'),
    path('create/', ad_create, name='ad_create'),
    path('edit/<int:ad_id>/', ad_edit, name='ad_edit'),
    path('ad/<int:ad_id>/', ad_detail, name='ad_detail'),
    path('my-responses/', my_responses, name='my_responses'),
    path('responce/<int:ad_id>/', responce_create),
    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    path('send-newsletter/', send_newsletter, name='send_newsletter'),

]