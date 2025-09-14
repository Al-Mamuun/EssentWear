from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Product, Review, Category

# ---------------------------
# User Signup Form
# ---------------------------
class UserSignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLES, widget=forms.Select())
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    
    # প্রথমে পাসওয়ার্ড ফিল্ডগুলো হাইড করি (ঐচ্ছিক)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'role', 'password1', 'password2']
        
        # উইজেটস যোগ করা (ঐচ্ছিক কিন্তু UI উন্নত করে)
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number (optional)'}),
        }
    
    # ইমেইল ভেরিফিকেশন (ঐচ্ছিক)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

# ---------------------------
# User Login Form
# ---------------------------
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={'placeholder': 'Enter username or email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

# ---------------------------
# Product Form (Seller)
# ---------------------------
class ProductForm(forms.ModelForm):
    # ক্যাটাগরির জন্য সাজানো ড্রপডাউন (ঐচ্ছিক)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category"
    )
    
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'stock_quantity', 'category', 'is_active']
        
        # UI উন্নত করার জন্য উইজেটস
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Product title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Product description', 'rows': 4}),
            'price': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01'}),
            'stock_quantity': forms.NumberInput(attrs={'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }
    
    # ভ্যালিডেশন - দাম যেন নেগেটিভ না হয়
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price
    
    # স্টক কোয়ান্টিটি ভ্যালিডেশন
    def clean_stock_quantity(self):
        stock = self.cleaned_data.get('stock_quantity')
        if stock < 0:
            raise forms.ValidationError("Stock quantity cannot be negative.")
        return stock

# ---------------------------
# Review Form (Buyer)
# ---------------------------
class ReviewForm(forms.ModelForm):
    # রেটিংকে স্টার রেটিং হিসেবে দেখানোর জন্য (ঐচ্ছিক)
    rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5', 'step': '1'})
    )
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Share your experience...', 'rows': 3}),
        }
    
    # রেটিং ভ্যালিডেশন (1-5 এর মধ্যে)
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

# ---------------------------
# User Profile Update Form (নতুন যোগ করা)
# ---------------------------
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),  # ইউজারনেম সাধারণত এডিট করা যায় না
            'email': forms.EmailInput(),
            'phone': forms.TextInput(),
            'address': forms.Textarea(attrs={'rows': 3}),
        }