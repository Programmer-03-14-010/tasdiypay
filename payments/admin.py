from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.html import format_html

from .models import PaymentCard, Receipt
from .forms import RejectReceiptForm

admin.site.site_header = "TasdiqPay — Admin panel"
admin.site.site_title = "TasdiqPay Admin"
admin.site.index_title = "Boshqaruv paneli"


@admin.register(PaymentCard)
class PaymentCardAdmin(admin.ModelAdmin):
    list_display = ("card_number", "card_holder", "bank_name", "updated_at")

    def has_add_permission(self, request):
        # Faqat 1 ta karta yozuvi bo'lishi kerak
        return not PaymentCard.objects.exists()


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "created_at", "reviewed_at", "image_preview", "actions_column")
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)
    readonly_fields = ("user", "image", "created_at", "image_preview_large")
    fields = ("user", "image", "image_preview_large", "status", "reject_reason", "created_at", "reviewed_at")

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Rasm"

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:400px;" />', obj.image.url)
        return "-"
    image_preview_large.short_description = "Chek rasmi (katta)"

    def actions_column(self, obj):
        if obj.status == Receipt.STATUS_PENDING:
            approve_url = reverse("admin:payments_receipt_approve", args=[obj.pk])
            reject_url = reverse("admin:payments_receipt_reject", args=[obj.pk])
            return format_html(
                '<a class="button" style="background:#28a745;color:#fff;padding:4px 8px;border-radius:4px;" href="{}">Qabul qilish</a>&nbsp;'
                '<a class="button" style="background:#dc3545;color:#fff;padding:4px 8px;border-radius:4px;" href="{}">Bekor qilish</a>',
                approve_url, reject_url,
            )
        elif obj.status == Receipt.STATUS_REJECTED:
            return format_html('<span style="color:#dc3545;">Bekor qilindi: {}</span>', obj.reject_reason)
        return format_html('<span style="color:#28a745;">Qabul qilindi</span>')
    actions_column.short_description = "Amallar / Holat"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("<int:pk>/approve/", self.admin_site.admin_view(self.approve_receipt), name="payments_receipt_approve"),
            path("<int:pk>/reject/", self.admin_site.admin_view(self.reject_receipt), name="payments_receipt_reject"),
        ]
        return custom + urls

    def approve_receipt(self, request, pk):
        receipt = get_object_or_404(Receipt, pk=pk)
        receipt.status = Receipt.STATUS_APPROVED
        receipt.reject_reason = ""
        receipt.reviewed_at = timezone.now()
        receipt.save()
        self.message_user(request, f"{receipt.user.username} ning cheki qabul qilindi.")
        return redirect("admin:payments_receipt_changelist")

    def reject_receipt(self, request, pk):
        receipt = get_object_or_404(Receipt, pk=pk)
        if request.method == "POST":
            form = RejectReceiptForm(request.POST)
            if form.is_valid():
                receipt.status = Receipt.STATUS_REJECTED
                receipt.reject_reason = form.cleaned_data["reason"]
                receipt.reviewed_at = timezone.now()
                receipt.save()
                self.message_user(request, f"{receipt.user.username} ning cheki bekor qilindi.")
                return redirect("admin:payments_receipt_changelist")
        else:
            form = RejectReceiptForm()
        return render(request, "admin/payments/reject_receipt.html", {
            "form": form, "receipt": receipt, "opts": self.model._meta,
        })
