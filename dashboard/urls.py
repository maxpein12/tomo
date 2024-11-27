from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import DeletePostView
# from .views import NewPostView




urlpatterns = [
    path('', views.AdminList, name='AdminList'),
    path('SalesChart/', views.SalesChart, name='SalesChart'),
    path('PostsList/', views.PostsList, name='PostsList'),
    path('SalesReport/', views.SalesReport, name='SalesReport'),
    path('MessageTemplate/', views.MessageTemplate, name='MessageTemplate'),
    path('PurchaseHistory/', views.PurchaseHistory, name='PurchaseHistory'),
    path('ReportList/', views.ReportList, name='ReportList'),
    path('Pricing/', views.Pricing, name='Pricing'),
    path('AdminList/', views.AdminList, name='AdminList'),
    path('UserList/', views.UserList, name='UserList'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.clientRegister, name='register'),
    path('logout/', views.logoutpage, name='logout'),
    path('UserList/<int:pkuser>/', views.UserProfile, name='UserList'),
    path('delete_post/<int:pkpost>/', DeletePostView.as_view(), name='delete_post'),
    path('edit-points-bundle/<int:pk>/', views.edit_points_bundle, name='edit_points_bundle'),
    path('update_total_users_count/', views.update_total_users_count, name='update_total_users_count'),
    #  path('new_post/', NewPostView.as_view(), name='new_post'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)