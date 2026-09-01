from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
import joblib
import os
from django.conf import settings

# Load model + vectorizer
model_path = os.path.join(settings.BASE_DIR, 'models/best_phishing_model.pkl')
vectorizer_path = os.path.join(settings.BASE_DIR, 'models/best_vectorizer.pkl')

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

def home(request):
    return render(request, 'home.html')


from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User

def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match"})

        # Check if email exists
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already registered"})

        hashed_password = make_password(password)
        User.objects.create(name=name, email=email, password=hashed_password)

        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Email not found"})

        if check_password(password, user.password):
            request.session["user_id"] = user.id
            request.session["user_name"] = user.name
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid password"})

    return render(request, "login.html")


def dashboard(request):
    if "user_id" not in request.session:
        return redirect("login")
    return render(request, "dashboard.html", {"name": request.session["user_name"]})

def prediction(request):
    prediction_text = None

    if request.method == "POST":
        input_data = request.POST['input_data']
        vect = vectorizer.transform([input_data]).toarray()
        prediction = model.predict(vect)[0]

        prediction_text = "Safe Email" if prediction == 0 else "Phishing Email"

    return render(request, "prediction.html", {"prediction": prediction_text})


def logout_view(request):
    logout(request)
    return render(request, "logout.html")