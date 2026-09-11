from django.db import models
from django.contrib.auth.models import User


class PaymentCard(models.Model):
    """Admin panel orqali tahrirlanadigan to'lov kartasi ma'lumoti.
    Har doim faqat 1 ta yozuv ishlatiladi (saytda ko'rsatiladigan asosiy karta)."""
    card_number = models.CharField("Karta raqami", max_length=19, help_text="Masalan: 8600 1234 5678 9012")
    card_holder = models.CharField("Karta egasi", max_length=100, blank=True)
    bank_name = models.CharField("Bank nomi", max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "To'lov kartasi"
        verbose_name_plural = "To'lov kartasi"

    def __str__(self):
        return f"{self.card_number} ({self.bank_name})"


class Receipt(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Tekshirilmoqda"),
        (STATUS_APPROVED, "Qabul qilindi"),
        (STATUS_REJECTED, "Bekor qilindi"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receipts", verbose_name="Foydalanuvchi")
    image = models.ImageField("Chek rasmi", upload_to="receipts/%Y/%m/")
    status = models.CharField("Holati", max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    reject_reason = models.TextField("Bekor qilish sababi", blank=True)
    created_at = models.DateTimeField("Yuklangan vaqti", auto_now_add=True)
    reviewed_at = models.DateTimeField("Ko'rib chiqilgan vaqti", null=True, blank=True)

    class Meta:
        verbose_name = "To'lov cheki"
        verbose_name_plural = "To'lov cheklari"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()} ({self.created_at:%Y-%m-%d %H:%M})"
