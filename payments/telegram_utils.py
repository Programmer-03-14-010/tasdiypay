"""Telegram bot orqali xabarnoma yuborish uchun yordamchi funksiyalar.

Tashqi kutubxonalarsiz (faqat standart `urllib`) ishlaydi, shuning uchun
loyihaga qo'shimcha `requests` kabi paket o'rnatish shart emas.
"""
import json
import logging
import urllib.request
import urllib.error

from django.conf import settings

logger = logging.getLogger(__name__)


def _send_telegram_message(text: str) -> bool:
    """Berilgan matnni sozlamalardagi TELEGRAM_CHAT_ID ga yuboradi.

    Xato yuz bersa, dasturni to'xtatmaydi - faqat logga yozadi va False qaytaradi,
    chunki bildirishnoma yuborilmasligi foydalanuvchi uchun to'lov jarayonini
    buzmasligi kerak.
    """
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "")
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", "")

    if not token or not chat_id:
        logger.warning(
            "Telegram bildirishnomasi yuborilmadi: TELEGRAM_BOT_TOKEN yoki "
            "TELEGRAM_CHAT_ID sozlanmagan."
        )
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status == 200
    except urllib.error.URLError as exc:
        logger.error("Telegramga xabar yuborishda xatolik: %s", exc)
        return False


def notify_new_payment(receipt) -> bool:
    """Yangi to'lov cheki yuklanganda Telegram botga bildirishnoma yuboradi."""
    user = receipt.user
    full_name = f"{user.first_name} {user.last_name}".strip() or user.username

    text = (
        "💳 <b>Yangi to'lov!</b>\n\n"
        f"👤 Foydalanuvchi: {full_name}\n"
        f"📧 Email/Login: {user.username}\n"
        f"🕒 Vaqti: {receipt.created_at:%Y-%m-%d %H:%M}\n"
        f"🧾 Chek ID: #{receipt.pk}\n"
        f"📌 Holati: {receipt.get_status_display()}"
    )
    return _send_telegram_message(text)
