from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import DeletePostView
# from .views import NewPostView




urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('favorites/', views.favorites, name='favorites'),
    path('inbox/', views.inbox, name='inbox'),
    path('orders/', views.orders, name='orders'),
    path('stock/', views.stock, name='stock'),
    path('pricing/', views.pricing, name='pricing'),
    path('ui/', views.ui, name='ui'),
    path('team/', views.team, name='team'),
    path('table/', views.table, name='table'),
    path('invoice/', views.invoice, name='invoice'),
    path('contact/', views.contact, name='contact'),
    path('calendar/', views.calendar, name='calendar'),
    path('todo/', views.todo, name='todo'),
    path('stock/', views.stock, name='stock'),
    path('orders/', views.orders, name='orders'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.clientRegister, name='register'),
    path('logout/', views.logoutpage, name='logout'),
    path('contact/<int:pkuser>/', views.test, name='contact'),
    path('delete_post/<int:pkpost>/', DeletePostView.as_view(), name='delete_post'),
    #  path('new_post/', NewPostView.as_view(), name='new_post'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)