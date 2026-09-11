# TasdiqPay — To'lovni tasdiqlash tizimi (Django)

Chiroyli, ko'p sahifali Django ilova: foydalanuvchi ro'yxatdan o'tadi (ism,
familiya, email, istalgan parol), kartaga to'lov qiladi, chek yuklaydi,
admin esa uni tasdiqlaydi yoki sababi bilan bekor qiladi.

## Sahifalar
- `/` — ommaviy bosh sahifa (landing)
- `/register/` — ro'yxatdan o'tish (Ism, Familiya, Email, Parol — cheklovsiz)
- `/login/` — kirish (Ism + parol)
- `/dashboard/` — shaxsiy boshqaruv paneli (statistikalar, karta, so'nggi faoliyat)
- `/pay/` — to'lov qilish sahifasi (karta ma'lumoti + chek yuklash)
- `/my-payments/` — to'lovlar tarixi
- `/my-payments/<id>/` — bitta to'lov haqida batafsil
- `/profile/` — profil (ism/familiya tahrirlash)
- `/admin/` — admin panel (faqat is_staff foydalanuvchilar; saytdagi "Admin panel"
  tugmasi orqali ham kirish mumkin)

## O'rnatish
```
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
`createsuperuser` so'raganda username o'rniga ham xohlagan email/parol yozishingiz
mumkin — u faqat admin/ panelga kirish uchun ishlatiladi.

## Admin ishi
1. Admin panelga kirib, "To'lov kartasi" bo'limida karta raqami/bank nomini kiriting.
2. "To'lov cheklari" bo'limida yuklangan cheklar, kim yuklaganini ko'rasiz.
3. "Tekshirilmoqda" holatidagi har bir chek qarshisida "Qabul qilish" va
   "Bekor qilish" tugmalari bor. Bekor qilishda sababni yozish majburiy — u
   keyin foydalanuvchining "Mening to'lovlarim" sahifasida ko'rinadi.

## Dizayn
Slab-serif sarlavhalar, chek/ledger uslubidagi kartalar, to'q ko'k (ink) +
teal aksent rang palitrasi. Barcha uslub `payments/static/payments/css/style.css`
faylida — bitta joydan boshqariladi.

## Diqqat
- Parol validatorlari o'chirilgan (`AUTH_PASSWORD_VALIDATORS = []`) — bu foydalanuvchi
  so'roviga ko'ra amalga oshirilgan, lekin ishlab chiqarish (production) muhitida
  xavfsizlik nuqtai nazaridan kuchliroq parol talab qilish tavsiya etiladi.
- Foydalanuvchilar tizimga **ism** va parol bilan kiradi (email o'rniga). Buning
  uchun ism har bir foydalanuvchida noyob bo'lishi shart — ro'yxatdan o'tishda
  bir xil ism band bo'lsa, tizim xato beradi va boshqa ism/variant so'raydi
  (masalan, "Aziz2"). Email hamon saqlanadi (admin panelda ko'rish uchun), lekin
  login uchun ishlatilmaydi.
- Admin (superuser) panelga hamon email + parol bilan kiradi — bu o'zgarmagan.
