from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Ticket, Producto, Carrito
from .forms import LoginForm, ProductoForm
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm,UpdateForm 
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Profile
from .forms import CustomRegisterForm, CustomAuthenticationForm, ProductoForm, LoginForm, CustomUserCreationForm
from .models import Producto, PurchaseReceipt, PurchaseDetail

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'

def index(request):
    return render(request, 'index.html')

def hombre(request):
    productos = Producto.objects.all()

    # Obtener el contenido del carrito para el usuario actual
    if request.user.is_authenticated:
        carrito_items = Carrito.objects.filter(usuario=request.user)
        total = sum(item.producto.precio * item.cantidad for item in carrito_items)
    else:
        carrito_items = []
        total = 0

    return render(request, 'hombre.html', {'productos': productos, 'carrito_items': carrito_items, 'total': total})

def nosotros(request):
    return render(request, 'nosotros.html')

def formu(request):
    form = CustomRegisterForm()
    return render(request, 'formu.html', {'form': form})

def ticket(request):
    return render(request, 'ticket.html')

def formu(request):
    return render(request, 'registration/formu.html')

def logout_view(request):
    auth_logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('index')

@login_required
def micuenta(request):
    user = request.user
    form = UpdateForm(instance=user)
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tus datos han sido actualizados correctamente.')
            return redirect('micuenta')
    return render(request, 'micuenta.html', {'user': user, 'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Por favor inicia sesión.')
            return redirect('index')  # Redirige al index.html después de un registro exitoso
        else:
            messages.error(request, 'Ha ocurrido un error en el registro. Por favor verifica los datos ingresados.')
    else:
        form = CustomRegisterForm()

    return render(request, 'formu.html', {'form': form})

def crear_ticket(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')

        if not nombre or not correo or not categoria or not descripcion:
            messages.error(request, 'Todos los campos son obligatorios.')
        else:
            ticket = Ticket(
                nombre=nombre,
                email=correo,
                categoria=categoria,
                descripcion=descripcion,
                imagen=imagen
            )
            ticket.save()
            messages.success(request, 'Ticket creado exitosamente.')
            return redirect('index')

    return render(request, 'index.html')

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos')
        else:
            print(form.errors)
    else:
        form = ProductoForm()
    return render(request, 'crear.html', {'productoform': form})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos')
    return render(request, 'eliminar_producto.html', {'producto': producto})

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})

def buscar_producto(request):
    producto_id = request.GET.get('id')
    if producto_id:
        try:
            producto = Producto.objects.get(id=producto_id)
            data = {
                'success': True,
                'producto': {
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'descripcion': producto.descripcion,
                    'precio': producto.precio,
                    'categoria': producto.categoria,
                    'stock': producto.stock,
                    'imagen': producto.imagen.url if producto.imagen else '',
                }
            }
        except Producto.DoesNotExist:
            data = {
                'success': False,
                'message': 'Producto no encontrado'
            }
    else:
        data = {
            'success': False,
            'message': 'ID de producto no proporcionado'
        }
    return JsonResponse(data)

def obtener_productos(request):
    productos = Producto.objects.all()
    data = [{'id': producto.id, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'precio': producto.precio, 'imagen': producto.imagen.url} for producto in productos]
    
    return JsonResponse({'productos': data})

def carrito_compras(request):
    user = request.user
    carrito_items = Carrito.objects.filter(usuario=user)
    total = sum(item.producto.precio * item.cantidad for item in carrito_items)
    return render(request, 'carrito.html', {'carrito_items': carrito_items, 'total': total})

@login_required
def agregar_al_carrito(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_ids')
        quantities = request.POST.getlist('quantities')

        for product_id, quantity in zip(product_ids, quantities):
            product = Producto.objects.get(pk=product_id)
            if product.stock >= int(quantity):
                carrito, created = Carrito.objects.get_or_create(usuario=request.user, producto=product)
                if not created:
                    carrito.cantidad += int(quantity)
                    carrito.save()
                else:
                    carrito.cantidad = int(quantity)
                    carrito.save()
                # Descontar el stock
                product.stock -= int(quantity)
                product.save()
                messages.success(request, f'Producto {product.nombre} agregado al carrito.')
            else:
                messages.error(request, f'No hay suficiente stock para el producto {product.nombre}.')

        return redirect('hombre')

    return HttpResponseBadRequest('Bad request')

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            auth_login(request , user)
            messages.success(request , "Te has registrado correctamente")
        data['form'] = formulario    

    return render(request, 'registration/registro.html', data)



@login_required
def comprar(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_ids')
        quantities = request.POST.getlist('quantities')

        if len(product_ids) != len(quantities):
            messages.error(request, 'Error en la solicitud de compra. Por favor, inténtalo de nuevo.')
            return redirect('hombre')

        try:
            # Convertir los IDs de productos y cantidades a enteros
            product_ids = [int(id) for id in product_ids]
            quantities = [int(qty) for qty in quantities]
        except ValueError:
            messages.error(request, 'Error en la solicitud de compra. Por favor, inténtalo de nuevo.')
            return redirect('hombre')

        total_amount = 0
        details = []

        for product_id, quantity in zip(product_ids, quantities):
            product = Producto.objects.get(pk=product_id)
            if product.stock >= quantity:
                total_price = product.precio * quantity
                detail = PurchaseDetail(product=product, quantity=quantity, total_price=total_price)
                details.append(detail)
                total_amount += total_price
                # Descontar el stock
                product.stock -= quantity
                product.save()
            else:
                messages.error(request, f'No hay suficiente stock para el producto {product.nombre}.')
                return redirect('hombre')

        # Crear la boleta de compra
        purchase_receipt = PurchaseReceipt.objects.create(user=request.user, total_amount=total_amount)
        purchase_receipt.details.set(details)

        # Marcar la compra como recibida
        purchase_receipt.status = "received"
        purchase_receipt.save()

        # Limpiar el carrito después de la compra
        Carrito.objects.filter(usuario=request.user).delete()

        messages.success(request, 'Compra realizada con éxito.')
        return redirect('purchase_history')

    else:
        # Si la solicitud no es POST, redirigir al carrito de compras
        return redirect('hombre')

@login_required
def purchase_history(request):
    purchases = PurchaseReceipt.objects.filter(user=request.user)
    return render(request, 'purchase_history.html', {'purchases': purchases})


def eliminar_del_carrito(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Carrito, id=item_id)
        
        # Restaurar el stock del producto eliminado
        item.producto.stock += item.cantidad
        item.producto.save()
        
        # Eliminar el item del carrito
        item.delete()

        messages.success(request, 'Producto eliminado del carrito.')
        return redirect('hombre')

    return HttpResponseBadRequest('Bad request')
