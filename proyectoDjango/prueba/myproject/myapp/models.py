from django.db import models
from django.contrib.auth.models import User  # Importa el modelo User estándar de Django
from django.utils import timezone

class Ticket(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    categoria = models.CharField(max_length=50)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='images/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')
    categoria = models.CharField(max_length=100, default='General')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Utiliza el modelo User estándar de Django
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.producto.nombre}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    region = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username} Profile'
    
class PurchaseDetail(models.Model):
    product = models.ForeignKey('Producto', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class PurchaseReceipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default="received")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.ManyToManyField(PurchaseDetail)    