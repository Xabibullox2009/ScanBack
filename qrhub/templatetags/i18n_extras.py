from django import template
from django.conf import settings

register = template.Library()

TRANSLATIONS = {
    "brand_tagline": {
        "uz": "QR yo'qolgan buyumlar xizmati",
        "ru": "QR сервис потерянных вещей",
        "en": "QR Lost and Found",
    },
    "hero_eyebrow": {
        "uz": "Yo'qolgan buyumlar tezroq topiladi",
        "ru": "Потерянные вещи находятся быстрее",
        "en": "Lost items, found faster",
    },
    "hero_title": {
        "uz": "Buyumingiz QR kod oladi. Topgan odam esa bir bosishda qo'ng'iroq qiladi.",
        "ru": "Ваша вещь получает QR-код. Нашедший звонит владельцу в одно нажатие.",
        "en": "Your item gets a QR code. The finder gets one-tap calling.",
    },
    "hero_text": {
        "uz": "ScanBack sumka, kalit, hujjat, qurilma va boshqa buyumlarni admin yaratgan QR kod orqali himoya qiladi. Kimdir kodni skaner qilsa, egasining ismi va tez qo'ng'iroq qilish tugmasi darhol ochiladi.",
        "ru": "ScanBack помогает защищать сумки, ключи, документы, устройства и другие вещи с помощью QR-кодов, которые создает администратор. После сканирования сразу открываются имя владельца и кнопка звонка.",
        "en": "ScanBack helps businesses and clients protect bags, keys, documents, devices, and personal belongings with admin-generated QR codes. When someone scans the code, they instantly see the owner's name and a call button that opens the phone dialer.",
    },
    "trust_1": {
        "uz": "Admin mijozlar uchun QR kod yaratadi",
        "ru": "Администратор создает QR-коды для клиентов",
        "en": "Admin creates QR codes for clients",
    },
    "trust_2": {
        "uz": "Har bir QR alohida xavfsiz sahifani ochadi",
        "ru": "Каждый QR открывает отдельную защищенную страницу",
        "en": "Each QR opens a unique secure slug page",
    },
    "trust_3": {
        "uz": "Telefon orqali egasiga bir bosishda qo'ng'iroq qilinadi",
        "ru": "Владельцу можно позвонить в одно нажатие",
        "en": "Mobile users can call the owner in one tap",
    },
    "scanned_page": {
        "uz": "Skanerlangan QR sahifasi",
        "ru": "Страница после сканирования QR",
        "en": "Scanned QR page",
    },
    "found_item_call": {
        "uz": "Agar bu buyumni topsangiz, egasiga qo'ng'iroq qiling.",
        "ru": "Если вы нашли эту вещь, пожалуйста, позвоните владельцу.",
        "en": "If you found this item, please call the owner.",
    },
    "call_owner": {
        "uz": "Egasiga qo'ng'iroq qilish",
        "ru": "Позвонить владельцу",
        "en": "Call Owner",
    },
    "businesses_title": {
        "uz": "Bizneslar uchun",
        "ru": "Для бизнеса",
        "en": "For businesses",
    },
    "businesses_text": {
        "uz": "Mijoz buyumlarini oddiy QR asosidagi callback tizimi bilan himoya qiling.",
        "ru": "Защитите вещи клиентов с помощью простой QR-системы обратного звонка.",
        "en": "Protect client belongings with a simple QR-based callback system.",
    },
    "clients_title": {
        "uz": "Mijozlar uchun",
        "ru": "Для клиентов",
        "en": "For clients",
    },
    "clients_text": {
        "uz": "Login kerak emas. Kontakt sahifasi QR koddan to'g'ridan-to'g'ri ochiladi.",
        "ru": "Логин не нужен. Контактная страница открывается прямо из QR-кода.",
        "en": "No login needed. Their contact page opens directly from the QR code.",
    },
    "finders_title": {
        "uz": "Topib olgan odam uchun",
        "ru": "Для нашедшего",
        "en": "For finders",
    },
    "finders_text": {
        "uz": "Skaner qiling, egani ko'ring, tugmani bosing va telefondan qo'ng'iroq qiling.",
        "ru": "Сканируйте, посмотрите владельца, нажмите кнопку и позвоните.",
        "en": "Scan, view the owner, tap the button, and call from the mobile dialer.",
    },
    "how_it_works": {
        "uz": "Qanday ishlaydi",
        "ru": "Как это работает",
        "en": "How it works",
    },
    "how_it_works_title": {
        "uz": "Admin paneldan mobil qo'ng'iroqqacha juda sodda jarayon",
        "ru": "Простой путь от админ-панели до звонка с телефона",
        "en": "Simple flow from admin dashboard to mobile call",
    },
    "step_1_title": {
        "uz": "Mijoz QR identifikator oladi",
        "ru": "Клиент получает QR-идентификатор",
        "en": "Client gets a QR identity",
    },
    "step_1_text": {
        "uz": "Har bir himoyalangan buyum egasining saqlangan kontaktlari bilan bog'lanadi.",
        "ru": "Каждая защищенная вещь связывается с сохраненными контактами владельца.",
        "en": "Each protected item is connected to its owner's saved contact details.",
    },
    "step_2_title": {
        "uz": "Tizim QR kod yaratadi",
        "ru": "Система генерирует QR-код",
        "en": "System generates the QR",
    },
    "step_2_text": {
        "uz": "ScanBack unikal slug yaratadi va QR rasmni avtomatik saqlaydi.",
        "ru": "ScanBack создает уникальный slug и автоматически сохраняет изображение QR.",
        "en": "ScanBack creates a unique slug and saves the QR image automatically.",
    },
    "step_3_title": {
        "uz": "Topgan odam kodni skaner qiladi",
        "ru": "Нашедший сканирует код",
        "en": "Finder scans the code",
    },
    "step_3_text": {
        "uz": "QR egasining ismi va qo'ng'iroq tugmasi bor toza sahifani ochadi.",
        "ru": "QR открывает аккуратную страницу с именем владельца и кнопкой звонка.",
        "en": "The QR opens a clean page showing the owner's name and call action.",
    },
    "step_4_title": {
        "uz": "Telefon ilovasi ochiladi",
        "ru": "Открывается приложение телефона",
        "en": "Phone app opens",
    },
    "step_4_text": {
        "uz": "Qo'ng'iroq tugmasi `tel:` ishlatadi va mobil qurilmada dialerni ochadi.",
        "ru": "Кнопка звонка использует `tel:` и сразу открывает номеронабиратель на телефоне.",
        "en": "The call button uses `tel:` so mobile devices open the dialer directly.",
    },
    "best_use_cases": {
        "uz": "Eng yaxshi qo'llanishlar",
        "ru": "Лучшие сценарии",
        "en": "Best use cases",
    },
    "best_use_cases_title": {
        "uz": "Odamlar har kuni yo'qotadigan haqiqiy buyumlar uchun",
        "ru": "Создано для реальных вещей, которые люди теряют каждый день",
        "en": "Made for real items people lose every day",
    },
    "use_case_1": {
        "uz": "Ryukzak va bagaj",
        "ru": "Рюкзаки и багаж",
        "en": "Backpacks and luggage",
    },
    "use_case_2": {
        "uz": "Kalit va hamyon",
        "ru": "Ключи и кошельки",
        "en": "Keys and wallets",
    },
    "use_case_3": {
        "uz": "Kompaniya qurilmalari",
        "ru": "Корпоративные устройства",
        "en": "Company devices",
    },
    "use_case_4": {
        "uz": "ID holder va kartalar",
        "ru": "Бейджи и карты",
        "en": "ID holders and cards",
    },
    "use_case_5": {
        "uz": "Maktab va ofis buyumlari",
        "ru": "Школьные и офисные вещи",
        "en": "School and office items",
    },
    "use_case_6": {
        "uz": "Yetkazib berish va sayohat jihozlari",
        "ru": "Снаряжение для доставки и поездок",
        "en": "Delivery and travel gear",
    },
    "contact_page_label": {
        "uz": "ScanBack aloqa sahifasi",
        "ru": "Контактная страница ScanBack",
        "en": "ScanBack Contact Page",
    },
    "mobile_note": {
        "uz": "Mobil qurilmada tugmani bosish telefon ilovasini avtomatik ochadi.",
        "ru": "На мобильных устройствах нажатие кнопки автоматически открывает приложение телефона.",
        "en": "On mobile devices, tapping the button opens the phone app automatically.",
    },
    "language_label": {
        "uz": "Til",
        "ru": "Язык",
        "en": "Language",
    },
}


@register.simple_tag(takes_context=True)
def tr(context, key):
    language_code = context.get("current_language", settings.LANGUAGE_CODE)
    values = TRANSLATIONS.get(key, {})
    return values.get(language_code) or values.get(settings.LANGUAGE_CODE) or key
