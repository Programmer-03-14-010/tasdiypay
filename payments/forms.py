from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Receipt, PaymentCard


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Ism", max_length=150, required=True)
    last_name = forms.CharField(label="Familiya", max_length=150, required=True)
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Bu email bilan hisob allaqachon mavjud.")
        return email

    def clean_first_name(self):
        # Ism tizimga kirish uchun identifikator sifatida ishlatiladi,
        # shuning uchun har bir foydalanuvchida noyob bo'lishi shart.
        first_name = self.cleaned_data["first_name"].strip()
        if User.objects.filter(first_name__iexact=first_name).exists():
            raise forms.ValidationError(
                "Bu ism bilan hisob allaqachon mavjud. Kirish uchun ism ishlatilgani "
                "sabab, boshqa ism kiriting yoki oxiriga raqam qo'shing (masalan: Aziz2)."
            )
        return first_name

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"]
        user.username = email
        user.email = email
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class NameLoginForm(AuthenticationForm):
    username = forms.CharField(label="Ism", widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(label="Parol", strip=False, widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": "Bunday ism va parolga ega hisob topilmadi.",
        "inactive": "Bu hisob faol emas.",
    }


class ReceiptUploadForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ["image"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }


class PaymentCardForm(forms.ModelForm):
    class Meta:
        model = PaymentCard
        fields = ["card_number", "card_holder", "bank_name"]


class RejectReceiptForm(forms.Form):
    reason = forms.CharField(
        label="Bekor qilish sababi",
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Masalan: chek soxta, summa mos emas..."}),
        required=True,
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
        labels = {"first_name": "Ism", "last_name": "Familiya"}
