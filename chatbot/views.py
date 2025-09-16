
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import ChatMessage
from .forms import SignUpForm
import uuid

# ---- Gemini API imports ----
from google import genai

# Gemini client (ye GEMINI_API_KEY environment variable se key lega)
client = genai.Client(api_key="AIzaSyBGO52XDUUILNU2hguc7CnSNiqbg1OM6EM")


# ------------------- SIGNUP -------------------
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "chatbot/signup.html", {"form": form})


# ------------------- HOME / CHAT -------------------
@login_required
def home(request, chat_id=None):
    # New chat id generate karo agar nahi diya gaya
    if chat_id is None:
        chat_id = str(uuid.uuid4())

    # Current chat ke saare messages
    messages = ChatMessage.objects.filter(
        user=request.user,
        chat_id=chat_id
    ).order_by("created_at")

    # Previous chats list (sirf IDs)
    previous_chats = ChatMessage.objects.filter(
        user=request.user
    ).values_list("chat_id", flat=True).distinct()

    if request.method == "POST":
        user_input = request.POST.get("message")
        if user_input:
            # ---- Gemini se real reply ----
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",   # latest fast model
                    contents=user_input
                )
                bot_reply = response.text
            except Exception as e:
                bot_reply = f"API error: {e}"

            # Message database me save karo
            ChatMessage.objects.create(
                user=request.user,
                user_email=request.user.email,  # email bhi store karega
                chat_id=chat_id,
                input_text=user_input,
                output_text=bot_reply,
            )

        return redirect("home", chat_id=chat_id)

    return render(request, "chatbot/home.html", {
        "messages": messages,
        "chat_id": chat_id,
        "previous_chats": previous_chats
    })


# ------------------- LOGOUT -------------------
@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")
