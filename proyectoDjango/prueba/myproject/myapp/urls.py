from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views
from .views import CustomLoginView, register_view, registro

urlpatterns = [
    path('', views.index, name='index'),
    path('hombre/', views.hombre, name='hombre'),  
    path('nosotros/', views.nosotros, name='nosotros'),  
    path('formu/', views.formu, name='formu'),  
    path('ticket/', views.ticket, name='ticket'),  
    path('register/', register_view, name='register'),  
    path('crear_ticket/', views.crear_ticket, name='crear_ticket'),
    path('register/', register_view, name='register'),
    path('registro/', registro, name='registro'),
    path('logout/', views.logout_view, name='logout'), 
    path('micuenta/', views.micuenta, name='micuenta'),
    path('productos/', views.productos, name='productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('eliminar-producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('buscar-producto/', views.buscar_producto, name='buscar_producto'),
    path('editar_producto/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('carrito/', views.carrito_compras, name='carrito_compras'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('comprar/', views.comprar, name='comprar'),
    path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar-del-carrito/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Usa la vista de Django para el login
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
