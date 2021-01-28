from django.urls import path
from . import views

urlpatterns = [

    path('login/'  ,views.loginPage , name="login"),
    path('registration/', views.registrationPage, name="registration"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/',views.userpage, name="userpage"),
    
    path('', views.home, name="home"),


    


    path('products/', views.products, name="products"),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    # path('order_form/<str:pk>/', views.order_form, name="order_form"),
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    
]