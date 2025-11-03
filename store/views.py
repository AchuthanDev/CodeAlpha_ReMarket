# --- Cleaned Up Imports ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
import firebase_admin
from firebase_admin import auth

from .models import Product, Category, Order
from .forms import ProductForm
# --- End of Imports ---


def home(request):
    """
    The homepage - Shows all available products.
    Handles search and category filtering.
    """
    products = Product.objects.filter(is_sold=False).order_by('-created_at')
    categories = Category.objects.all()
    
    search_query = request.GET.get('q')
    category_id = request.GET.get('category')
    current_category = None
    
    # --- Handle Category Filtering ---
    if category_id:
        try:
            current_category = Category.objects.get(id=category_id)
            products = products.filter(category=current_category)
        except Category.DoesNotExist:
            pass # Just show all products if category is invalid
            
    # --- Handle Search Query ---
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'current_category': current_category,
    }
    return render(request, 'store/home.html', context)

def product_detail(request, product_id):
    """Show the details for a single product."""
    product = get_object_or_404(Product, id=product_id, is_sold=False)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)

def category_page(request, category_id):
    """Show all products for a specific category."""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(
        category=category, 
        is_sold=False
    ).order_by('-created_at')
    
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'store/category_page.html', context)

# --- Authentication Views ---

@csrf_exempt
def firebase_login(request):
    """Handles token from Firebase to log in or create a Django user."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')

            if not token:
                return JsonResponse({'status': 'error', 'message': 'Token not provided'}, status=400)

            decoded_token = auth.verify_id_token(token)
            
            uid = decoded_token['uid']
            email = decoded_token.get('email')
            name = decoded_token.get('name', '') 

            if not email:
                return JsonResponse({'status': 'error', 'message': 'Email not found in token'}, status=400)

            # --- ROBUST USER CHECKING (This fixes Google Login) ---
            try:
                # 1. Try to find the user by their verified email
                user = User.objects.get(email=email)
                created = False
            except User.DoesNotExist:
                try:
                    # 2. Try to find by username (if email was blank on an old account)
                    user = User.objects.get(username=email)
                    user.email = email # Update the blank email
                    user.save()
                    created = False
                except User.DoesNotExist:
                    # 3. If no user exists, create one
                    user = User.objects.create_user(username=email, email=email)
                    created = True
            # --- END OF ROBUST LOGIC ---
            
            if created:
                # If the user is new, set their first/last name if Google provided it
                if name:
                    name_parts = name.split(' ')
                    user.first_name = name_parts[0]
                    if len(name_parts) > 1:
                        user.last_name = ' '.join(name_parts[1:])
                user.save()
            
            # Log the user into the Django session
            login(request, user)
            
            return JsonResponse({'status': 'success', 'username': user.username})

        except auth.InvalidIdTokenError:
            return JsonResponse({'status': 'error', 'message': 'Invalid ID token'}, status=401)
        except Exception as e:
            # This will catch any error (like IntegrityError) and report it
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)

def custom_logout(request):
    """Log the user out of the Django session."""
    logout(request)
    return redirect('home')

# --- Seller/User Views ---

@login_required
def my_account(request):
    """Show the user's account page."""
    return render(request, 'store/my_account.html')

@login_required
def create_product(request):
    """View for creating a new product listing."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) 
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user 
            product.save()
            return redirect('my_listings') 
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'store/product_form.html', context)

@login_required
def my_listings(request):
    """Show all products listed by the current user."""
    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    context = {'products': products}
    return render(request, 'store/my_listings.html', context)

@login_required
def edit_product(request, product_id):
    """View for editing an existing product listing."""
    product = get_object_or_404(Product, id=product_id)

    if product.seller != request.user:
        return redirect('home') 

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('my_listings')
    else:
        form = ProductForm(instance=product)
    context = {'form': form}
    return render(request, 'store/product_form.html', context)

@login_required
def delete_product(request, product_id):
    """View to delete a product. Must be a POST request."""
    product = get_object_or_404(Product, id=product_id)

    if product.seller != request.user:
        return redirect('home')

    if request.method == 'POST':
        product.delete()
        return redirect('my_listings')
    else:
        return redirect('my_listings')

# --- Cart & Order Views ---
    
@login_required
def add_to_cart(request, product_id):
    """Add a product to the user's cart in the session."""
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    # FIX: Session keys must be strings
    product_id_str = str(product_id) 

    if product_id_str not in cart:
        cart[product_id_str] = {'quantity': 1}
    
    request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def view_cart(request):
    """Display the user's shopping cart."""
    cart = request.session.get('cart', {})
    products_in_cart = []
    total_price = 0

    # FIX: Use list() to allow modification during iteration
    for product_id_str in list(cart.keys()): 
        try:
            product = Product.objects.get(id=int(product_id_str))
            
            # FIX: Check if item was sold *after* being added to cart
            if product.is_sold:
                del request.session['cart'][product_id_str]
                request.session.modified = True
                continue # Skip to next item

            item_data = cart[product_id_str]
            subtotal = product.price * item_data['quantity']
            
            products_in_cart.append({
                'product': product,
                'quantity': item_data['quantity'],
                'subtotal': subtotal
            })
            total_price += subtotal
            
        except Product.DoesNotExist:
            # Product was deleted, remove it from cart
            del request.session['cart'][product_id_str]
            request.session.modified = True
            
    context = {
        'products_in_cart': products_in_cart,
        'total_price': total_price
    }
    return render(request, 'store/view_cart.html', context)

@login_required
def remove_from_cart(request, product_id):
    """Remove a product from the user's cart in the session."""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id) 

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        
    return redirect('view_cart')

@login_required
def checkout(request):
    """Process the order and create Order objects."""
    cart = request.session.get('cart', {})
    
    # Use list() for safe iteration
    for product_id_str in list(cart.keys()): 
        product_id = int(product_id_str)
        product = get_object_or_404(Product, id=product_id)

        if not product.is_sold:
            Order.objects.create(
                buyer=request.user,
                product=product
            )
            product.is_sold = True
            product.save()

    request.session['cart'] = {}
    request.session.modified = True
    
    return redirect('order_success')

@login_required
def order_success(request):
    """Show a success message after checkout."""
    return render(request, 'store/order_success.html')

@login_required
def my_orders(request):
    """Show all orders for the current user."""
    orders = Order.objects.filter(buyer=request.user).order_by('-ordered_at')
    context = {'orders': orders}
    return render(request, 'store/my_orders.html', context)