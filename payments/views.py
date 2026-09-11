from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

from .forms import RegisterForm, ReceiptUploadForm, NameLoginForm, ProfileForm
from .models import PaymentCard, Receipt
from .telegram_utils import notify_new_payment


def landing_view(request):
    """Ommaviy bosh sahifa (marketing) - login qilmagan foydalanuvchilar uchun."""
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "payments/landing.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="payments.backends.FirstNameBackend")
            messages.success(request, "Xush kelibsiz! Hisobingiz muvaffaqiyatli yaratildi.")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "payments/register.html", {"form": form})


class NameLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = NameLoginForm

    def get_success_url(self):
        return "/dashboard/"


@login_required
def dashboard_view(request):
    """To'lov holati va tezkor statistikani ko'rsatadigan asosiy panel."""
    receipts = request.user.receipts.all()
    stats = {
        "pending": receipts.filter(status=Receipt.STATUS_PENDING).count(),
        "approved": receipts.filter(status=Receipt.STATUS_APPROVED).count(),
        "rejected": receipts.filter(status=Receipt.STATUS_REJECTED).count(),
    }
    last_receipt = receipts.first()
    card = PaymentCard.objects.first()
    return render(request, "payments/dashboard.html", {
        "stats": stats,
        "last_receipt": last_receipt,
        "card": card,
        "recent": receipts[:5],
    })


@login_required
def pay_view(request):
    """Karta ma'lumotlari va chek yuklash sahifasi."""
    card = PaymentCard.objects.first()

    if request.method == "POST":
        form = ReceiptUploadForm(request.POST, request.FILES)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.user = request.user
            receipt.save()
            notify_new_payment(receipt)
            messages.success(request, "Chek yuborildi. Hozir tekshirilmoqda.")
            return redirect("pay")
    else:
        form = ReceiptUploadForm()

    last_receipt = request.user.receipts.first()

    return render(request, "payments/pay.html", {
        "card": card,
        "form": form,
        "last_receipt": last_receipt,
    })


@login_required
def my_payments_view(request):
    """Mening to'lovlarim sahifasi - foydalanuvchining barcha cheklari va holati."""
    receipts = request.user.receipts.all()
    return render(request, "payments/my_payments.html", {"receipts": receipts})


@login_required
def payment_detail_view(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk, user=request.user)
    return render(request, "payments/payment_detail.html", {"receipt": receipt})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "payments/profile.html", {"form": form})


@login_required
def staff_login_redirect(request):
    """Sayt ichidagi tugma orqali admin panelga o'tish - faqat staff/admin uchun."""
    if request.user.is_staff:
        return redirect("/admin/")
    messages.error(request, "Sizda admin panelga kirish huquqi yo'q.")
    return redirect("dashboard")
