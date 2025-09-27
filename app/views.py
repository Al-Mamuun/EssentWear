from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, ChatHistory
from .forms import CustomerRegistrationForm, PasswordChangeForm, CustomerProfileForm, ProductForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
import re


# ----------------- Product Views -----------------
class Productview(View):
 def get(self, request):
  men = Product.objects.filter(category='M')
  women = Product.objects.filter(category='W')
  jwellery = Product.objects.filter(category='J')
  return render(request, 'app/home.html', { 'men' : men, 'women' : women, 'jwellery': jwellery })

class ProductDeatilView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart':item_already_in_cart})


class ProductDeleteView(View):
    def post(self, request, pk):
        if not request.user.is_superuser:
            messages.error(request, "You are not authorized to delete this product.")
            return redirect('product-detail', pk=pk)

        product = get_object_or_404(Product, pk=pk)
        product.delete()
        messages.success(request, f"Product '{product.title}' has been deleted successfully.")
        return redirect('home')  # Redirect to homepage or product list

@user_passes_test(lambda u: u.is_superuser)
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "app/product_edit.html", {"form": form, "product": product})
# ----------------- Cart Views -----------------
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('prod_id')
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('showcart')  
    else:
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('/')

@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shiiping_amount = 100.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shiiping_amount
   return render(request, 'app/addtocart.html', {'cart': cart, 'totalamount': total_amount, 'amount': amount, 'shipingamount': shiiping_amount})
  else:
   return render(request, 'app/emptycart.html')

def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get( Q (product = prod_id) & Q (user=request.user))
  c.quantity += 1
  c.save()
  amount = 0.0
  shiiping_amount = 100.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shiiping_amount
  data = {
     'quantity': c.quantity,
     'amount': amount,
     'totalamount': total_amount
    }
  return JsonResponse(data)

def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get( Q (product = prod_id) & Q (user=request.user))
  c.quantity -= 1
  c.save()
  amount = 0.0
  shiiping_amount = 100.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shiiping_amount
  data = {
     'quantity': c.quantity,
     'amount': amount,
     'totalamount': total_amount
    }
  return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            c.delete()
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)

        amount = 0.0
        shipping_amount = 100.0
        total_amount = 0.0

        cart_product = Cart.objects.filter(user=request.user)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
            total_amount = amount + shipping_amount

        data = {
            'amount': amount,
            'totalamount': total_amount
        }
        return JsonResponse(data)

# ----------------- Profile Views -----------------
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        try:
            profile = Customer.objects.get(user=request.user)
            form = CustomerProfileForm(initial={
                'name': profile.name,
                'phone_no': profile.phone_no,
                'email': profile.email,
                'address': profile.address,
                'gender': profile.gender,
            })
        except Customer.DoesNotExist:
            form = CustomerProfileForm(initial={
                'name': request.user.get_full_name(),
                'email': request.user.email
            })
            profile = None

        # Recent 5 orders
        order_placed = OrderPlaced.objects.filter(user=request.user).order_by('-id')[:5]

        return render(request, 'app/profile.html', {
            'form': form,
            'profile': profile,
            'order_placed': order_placed,
            'active': 'btn-primary'
        })

    def post(self, request):
        try:
            profile = Customer.objects.get(user=request.user)
            form = CustomerProfileForm(request.POST, instance=profile)
        except Customer.DoesNotExist:
            form = CustomerProfileForm(request.POST)
            profile = None

        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()

            # Update auth user email
            request.user.email = form.cleaned_data.get('email')
            request.user.save()

            return redirect('profile')

        order_placed = OrderPlaced.objects.filter(user=request.user).order_by('-id')[:5]
        return render(request, 'app/profile.html', {
            'form': form,
            'profile': profile,
            'order_placed': order_placed,
        })

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)

    if request.method == "POST":
        address_id = request.POST.get("address_id")
        address_obj = get_object_or_404(Customer, id=address_id, user=request.user)
        address_obj.name = request.POST.get("name")
        address_obj.phone_no = request.POST.get("phone_no")
        address_obj.email = request.POST.get("email")
        address_obj.address = request.POST.get("address")
        address_obj.save()

        messages.success(request, "Address updated successfully!")
        return redirect('address')  # Refresh page to show updated address

    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})

@login_required
def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user).order_by('-id')
    return render(request, 'app/orders.html', {'order_placed': order_placed})

class change_password(View):
 def get(self, request):
  form=PasswordChangeForm()
  messages.success(request, 'Congratulations!! Changed Successfully')
  return render(request, 'app/changepassword.html', {'form': form})

# ----------------- Category Views -----------------
def men(request, data=None):
    men = Product.objects.filter(category='M')

    # price range filter
    price = request.GET.get("price")
    if price == "under500":
        men = men.filter(discounted_price__lt=500)
    elif price == "500-1000":
        men = men.filter(discounted_price__gte=500, discounted_price__lte=1000)
    elif price == "1000-2000":
        men = men.filter(discounted_price__gte=1000, discounted_price__lte=2000)
    elif price == "above2000":
        men = men.filter(discounted_price__gt=2000)

    return render(request, 'app/men.html', {'mens': men})

def women(request, data=None):
    women = Product.objects.filter(category='W')

    # price range filter
    price = request.GET.get("price")
    if price == "under500":
        women = women.filter(discounted_price__lt=500)
    elif price == "500-1000":
        women = women.filter(discounted_price__gte=500, discounted_price__lte=1000)
    elif price == "1000-2000":
        women = women.filter(discounted_price__gte=1000, discounted_price__lte=2000)
    elif price == "above2000":
        women = women.filter(discounted_price__gt=2000)

    return render(request, 'app/women.html', {'womens': women})


def jwellery(request, data=None):
    jwellery = Product.objects.filter(category='J')

    # price range filter
    price = request.GET.get("price")
    if price == "under500":
        jwellery = jwellery.filter(discounted_price__lt=500)
    elif price == "500-1000":
        jwellery = jwellery.filter(discounted_price__gte=500, discounted_price__lte=1000)
    elif price == "1000-2000":
        jwellery = jwellery.filter(discounted_price__gte=1000, discounted_price__lte=2000)
    elif price == "above2000":
        jwellery = jwellery.filter(discounted_price__gt=2000)

    return render(request, 'app/jwellery.html', {'jwellerys': jwellery})


# ----------------- Authentication Views -----------------
class CustomerRegistrationView(View):
 def get (self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form': form})

 def post(self, request):
  form=CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully')
   form.save()
  return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user = user)
  amount = 0.0
  shiiping_amount = 60.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
      total_amount = amount + shiiping_amount

  return render(request, 'app/checkout.html', {'add': add, 'totalamount': total_amount, 'cart_items': cart_items})

@login_required
def order_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id = custid)
  cart = Cart.objects.filter(user = user)
  for c in cart:
    OrderPlaced(user=user, customer = customer, product=c.product, quantity = c.quantity).save()
    c.delete()
  return redirect("orders")

# ----------------- Other Views -----------------
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')

        try:
            # Use regular expressions to extract the product query
            search_pattern = r'(search for|find) (.+)'  # Match "search for" followed by any text
            match = re.search(search_pattern, user_message, re.IGNORECASE)

            if match:
                search_phrase = match.group(1)
                product_query = match.group(2).strip()

                search_results = Product.objects.filter(title__icontains=product_query)

                if search_results:
                    # Initialize an empty response
                    bot_response = "Here are some products I found:<br><br>"

                    # Iterate through the search results and format them
                    for product in search_results:
                        image_url = product.p_image.url
                        bot_response += f"<img src='{image_url}' alt='{product.title} Image' class='small-image'><br>"
                        bot_response += f"<strong>Name:</strong> {product.title}<br>"
                        bot_response += f"<strong>Description:</strong> {product.description}<br>"
                        bot_response += f"<strong>Price:</strong> TK.{product.selling_price}<br>"
                        bot_response += f"<strong>Discounted Price:</strong> TK.{product.discounted_price}<br><br><br>"

                else:
                    bot_response = "I couldn't find any products matching your query."

            else:
                bot_response = generate_bot_response(user_message)  # Define this function for other responses

            return JsonResponse({'bot_response': bot_response})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


    return render(request, 'app/try.html')


def generate_bot_response(user_message):
    user_message = user_message.lower()
    if 'hello' in user_message:
        return 'Hello! How can I assist you today?'
    elif 'how are you' in user_message :
        return 'I am fine. How can I assist you today?'
    elif 'what is your name' in user_message or 'whats your name' in user_message or 'who are you' in user_message:
        return 'I am Alice. I am here to assist you. How can I assist you?'
    elif "bye" in user_message:
        return "Goodbye. See you."
    elif "women" in user_message or 'ladies' in user_message  or 'woman' in user_message :
       return "Here is the link of women section: <a href='http://127.0.0.1:8000/women/'>Click here</a> <br> Please checkout"
    elif "gents" in user_message or 'men' in user_message  or 'man' in user_message:
       return "Here is the link of men section: <a href='http://127.0.0.1:8000/men/'>Click here</a><br>Please checkout"
    elif "jwellery" in user_message or 'jwellry' in user_message  or 'jewellery' in user_message :
       return "Here is the link of jwellery section: <a href='http://127.0.0.1:8000/jwellery/'>Click here</a> <br> Please checkout"
    elif "for summer" in user_message :
       return "Light and breathable fabrics like cotton and linen are perfect choices for comfortable summer wear."
    elif "my size" in user_message :
       return "Refer to our size chart for accurate measurements and fitting guidelines to determine the right size for you."
    elif "latest colours for this season" in user_message :
       return "This season's trending colours include soft pastels, earthy tones, and classic neutrals that are perfect for any wardrobe.<a href='http://127.0.0.1:8000/'>Click here</a><br>Please checkout"
    elif "change the dress" in user_message :
       return "Yes, you can. Reach our customer support team via email at support@clothingmart.com or call us."
    elif "winter clothes" in user_message :
       return "Stay warm and stylish with our cozy sweaters, comfortable jackets, and fashionable boots for a perfect winter day out.<a href='http://127.0.0.1:8000/'>Click here</a><br>Please checkout"
    elif "wash" in user_message :
       return "Follow the care instructions on the label, generally suggesting a gentle cycle with cold water and a low-heat tumble dry."
    elif "back my purchase" in user_message :
       return "Our return policy allows you to send back unworn items within 7 days of purchase for a refund or exchange."
    elif "delivery time" in user_message :
       return "Our standard delivery time is usually between 3 to 5 business days, depending on your location."
    elif "track my order" in user_message :
       return "You can track your order by using the tracking number provided in the shipping confirmation email."
    elif "customer support" in user_message or 'customer care' in user_message:
       return "You can reach our customer support team via email at support@clothingmart.com or call."
    elif "interview outfit" in user_message :
       return "For a job interview, consider wearing a well-fitted suit or a professional dress paired with subtle accessories for a polished look."
    elif "storing delicate clothes?" in user_message :
       return "Store delicate clothes in a cool, dry place, ideally in a breathable garment bag or a drawer away from direct sunlight."
    elif "sales info?" in user_message :
       return "Stay tuned for our upcoming seasonal sale event next month, where you can enjoy exciting discounts on various products."
    elif 'payment methods' in user_message :
        return 'We accept various payment methods, including credit/debit cards, PayPal, Bkash, Nagad, and other major online payment platforms for your convenience.'
    elif 'cancel order' in user_message or 'cancel my order' in user_message:
        return 'You can cancel your order within 24 hours of placing it. After that, we recommend contacting our customer support team for further assistance.'
    elif "hi" in user_message or 'hola' in user_message:
       return "Hello! How can I assist you today?"
    else:
        return "I'm sorry, I didn't understand that."


def search_products(request):
    query = request.GET.get('q', '').strip()  # Get search query
    search_results = []

    if query:
        # Split query into words
        words = query.split()
        # Build regex for exact word match, case-insensitive
        regex_pattern = r'\b(?:' + '|'.join(map(re.escape, words)) + r')\b'

        # Filter products whose title contains any of the words exactly
        search_results = Product.objects.filter(title__iregex=regex_pattern)

    return render(request, 'app/search_results.html', {'search_results': search_results, 'query': query})

# ----------------- Static/Other Pages -----------------

def contactus(request):
  return render(request, 'app/contact.html')

def tryon(request):
    return render(request, 'app/try.html')

def mamun(request):
    return render(request, 'app/mamun.html')

def faq(request):
    return render(request, 'app/faq.html')

def return_policy(request):
    return render(request, 'app/return_policy.html')

def size_guide(request):
    return render(request, 'app/size_guide.html')

def shipping_info(request):
    return render(request, 'app/shipping_info.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    if request.method == "POST":
        title = request.POST.get("title")
        category = request.POST.get("category")
        selling_price = request.POST.get("selling_price")
        discounted_price = request.POST.get("discounted_price")
        description = request.POST.get("description")
        image = request.FILES.get("p_image")

        Product.objects.create(
            title=title,
            category=category,
            selling_price=selling_price,
            discounted_price=discounted_price,
            description=description,
            p_image=image
        )
        return redirect("home")  # নতুন প্রোডাক্ট দিলে home এ ফিরবে

    return redirect("home")