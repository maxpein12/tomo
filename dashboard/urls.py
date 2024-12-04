from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import DeletePostView, add_admin_member, update_price
# from .views import NewPostView

app_name = 'dashboard'


urlpatterns = [
    path('', views.UserList, name='UserList'),
    path('SalesChart/', views.SalesChart, name='SalesChart'),
    path('PostsList/', views.PostsList, name='PostsList'),
    path('SalesReport/', views.SalesReport, name='SalesReport'),
    path('MessageTemplate/', views.MessageTemplate, name='MessageTemplate'),
    path('PurchaseHistory/', views.PurchaseHistory, name='PurchaseHistory'),
    path('ReportList/', views.ReportList, name='ReportList'),
    path('Pricing/', views.Pricing, name='Pricing'),
    path('AdminList/', views.AdminList, name='AdminList'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.clientRegister, name='register'),
    path('logout/', views.logoutpage, name='logout'),
    path('UserProfile/<int:pkuser>/', views.UserProfile, name='UserProfile'),
    path('delete_post/<int:pkpost>/', DeletePostView.as_view(), name='delete_post'),
    path('edit_points_bundle/<pk>/', views.edit_points_bundle, name='edit_points_bundle'),
    path('update_total_users_count/', views.update_total_users_count, name='update_total_users_count'),
    path('edit_post_status/<pk>/', views.edit_post_status, name='edit_post_status'),
    path('delete_user/<int:pkuser>/', views.delete_user, name='delete_user'),
    path('add-admin-member/', add_admin_member, name='add_admin_member'),
    path('update-price/', update_price, name='update_price'),
    path('update_message/<pk>/', views.update_message, name='update_message'),
    path('delete_message/<pk>/', views.delete_message, name='delete_message'),
    path('add_message/', views.add_message, name='add_message'),
    path('delete_admin/<pk>/', views.delete_admin, name='delete_admin'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)