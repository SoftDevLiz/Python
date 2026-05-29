from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Store, Product, Review, Purchase


def reg_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if not username or not password or not role:
            messages.error(request, "All fields are required!")
            return render(request, 'shop/register.html')

        new_user = User.objects.create_user(
            username=username, email=email, password=password)

        try:
            group = Group.objects.get(name=role)
            new_user.groups.add(group)
            messages.success(request, f"Account created! You are now a {role}")
            return redirect('login')
        except Group.DoesNotExist:
            messages.error(
                request, "Error: Role group does not exist in the database")

    return render(request, 'shop/register.html')


def home(request):
    # 1. Get ALL products from ALL stores
    all_products = Product.objects.all()

    # 2. Keep our existing "has_store" logic for the header/buttons
    has_store = False
    if request.user.is_authenticated:
        has_store = Store.objects.filter(owner=request.user).exists()

    # 3. Pass everything to the template
    return render(request, 'shop/home.html', {
        'has_store': has_store,
        'products': all_products
    })


@login_required
def create_store(request):
    if not request.user.groups.filter(name='Sellers').exists():
        messages.error(request, "Only Sellers can create a store.")
        return redirect('home')

    if request.method == "POST":
        store_name = request.POST.get('store_name')

        new_store = Store.objects.create(
            name=store_name, owner=request.user
        )

        messages.success(request, f"{store_name} has been created!")
        return redirect('home')

    return render(request, 'shop/create_store.html')


@login_required
def store_dashboard(request):
    try:
        my_store = Store.objects.get(owner=request.user)
        products = Product.objects.filter(store=my_store)
    except Store.DoesNotExist:
        return redirect('create_store')

    return render(request, 'shop/dashboard.html', {'store': my_store,
                                                   'products': products})


@login_required
def add_product(request):

    try:
        my_store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        messages.error(
            request, "You need to create a store before adding products")
        return redirect('create_store')

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        Product.objects.create(
            store=my_store,
            name=name,
            description=description,
            price=price,
            stock=stock
        )

        messages.success(
            request, f"Successfully added {name} to your inventory!")
        return redirect('dashboard')

    return render(request, 'shop/add_product.html', {'store': my_store})


@login_required
def edit_product(request, product_id):
    # 1. Find the product or 404 if it doesn't exist
    product = get_object_or_404(Product, id=product_id)

    # 2. Security: Make sure this product actually belongs to the user's store!
    if product.store.owner != request.user:
        messages.error(request, "You don't have permission to edit this.")
        return redirect('dashboard')

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.save()  # This updates the existing row in HeidiSQL

        messages.success(request, f"{product.name} updated!")
        return redirect('dashboard')

    return render(request, 'shop/edit_product.html', {'product': product})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the person deleting it actually owns it!
    if product.store.owner == request.user:
        if request.method == "POST":  # Security best practice
            product.delete()
            messages.success(request, "Product deleted.")

    return redirect('dashboard')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Grab all reviews for this product
    reviews = Review.objects.filter(product=product)

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews
    })


@login_required
def leave_review(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)

        # Check if this user has ever purchased this product
        has_purchased = Purchase.objects.filter(
            user=request.user, product=product).exists()

        Review.objects.create(
            product=product,
            author=request.user,
            content=request.POST.get('comment'),
            is_verified=has_purchased  # True if they bought it, False if not!
        )
        messages.success(request, "Review submitted!")
    return redirect('product_detail', product_id=product_id)


def add_to_cart(request, product_id):
    # 1. Get the cart from the session, or create an empty one if it doesn't exist
    cart = request.session.get('cart', {})

    # 2. Add the product (or increase quantity)
    # We use strings for keys because session JSON likes strings
    p_id = str(product_id)
    if p_id in cart:
        cart[p_id] += 1
    else:
        cart[p_id] = 1

    # 3. Save the cart back to the session
    request.session['cart'] = cart
    messages.success(request, "Added to cart!")

    return redirect('home')


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('home')

    cart_items = []
    total_price = 0
    invoice_text = "INVOICE - EMPORIUM MARKETPLACE\n\nItems Purchased:\n"

    # 1. Process items and build Invoice string
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total_price += subtotal

        # Record the purchase for "Verified Review" logic later
        Purchase.objects.create(user=request.user, product=product)

        invoice_text += f"- {product.name} (x{quantity}): R{subtotal}\n"

    invoice_text += f"\nTOTAL PAID: R{total_price}\n\nThank you for shopping at Emporium!"

    # 2. Send the Email
    send_mail(
        'Your Emporium Invoice',
        invoice_text,
        'noreply@emporium.com',
        [request.user.email],
        fail_silently=False,
    )

    # 3. Clear the Cart
    request.session['cart'] = {}

    return render(request, 'shop/checkout_success.html', {'cart_items': cart_items, 'total': total_price, 'order_id': request.user.id + 1000})


@login_required
def delete_store(request):
    # Ensure the user actually has a store to delete
    store = get_object_or_404(Store, owner=request.user)

    if request.method == "POST":
        store.delete()
        messages.success(
            request, "Your store and all its products have been removed.")
        return redirect('home')

    return redirect('dashboard')
