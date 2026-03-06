import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, \
    InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, \
    ConversationHandler
import re

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

RUSSIAN_OFFER_URL = 'https://telegra.ph/PUBLICHNAYA-OFERTA-KLUBA-03-05'
UZBEK_OFFER_URL = 'https://telegra.ph/IKKINCHI-KELIN-KLUBINING-Ommaviy-OFERI-03-06'
CHANNEL_ID = '@secondbride_uz'  # ID канала для публикации
CHANNEL_LINK = 'https://t.me/secondbride_uz'  # Ссылка на канал

# Состояния для ConversationHandler
(CATEGORY, CUSTOM_NAME, CONDITION, SIZE, COMMENT, BRAND, PRICE, PRICE_CONFIRM, PHOTO, PHONE) = range(10)

user_language = {}
user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Добро пожаловать в Second Bride! 👗\n"
        "Пожалуйста, выберите язык.\n\n"
        "Second Bride’ga xush kelibsiz! 👗\n"
        "Iltimos, tilni tanlang."
    )

    keyboard = [
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'),
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='lang_uz')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )
    return ConversationHandler.END


async def show_offer(update: Update, context: ContextTypes.DEFAULT_TYPE, language):
    query = update.callback_query

    if language == 'ru':
        welcome_text = (
            "👗 <b>Привет!</b> Я помогу тебе быстро пристроить свадебное платье или декор.\n\n"
            "Сначала нажми кнопку ниже, чтобы подтвердить, "
            "что ты согласна с <b>правилами нашего клуба</b> (Оферта)."
        )
        button_text = "📄 Прочитать Оферту"
        offer_url = RUSSIAN_OFFER_URL

        reply_keyboard = [
            [KeyboardButton("✅ Принимаю условия")]
        ]
        reply_text = "Нажмите кнопку 'Принять', чтобы продолжить:"
    else:
        welcome_text = (
            "👗 <b>Salom!</b> Men sizga to'y libosini yoki dekoratsiyani tezda sotishda yordam beraman.\n\n"
            "Avval <b>klub qoidalari</b> (Oferta) bilan roziligingizni tasdiqlash uchun quyidagi tugmani bosing."
        )
        button_text = "📄 Ofertani o'qish"
        offer_url = UZBEK_OFFER_URL

        reply_keyboard = [
            [KeyboardButton("✅ Shartlarni qabul qilaman")]
        ]
        reply_text = "Davom etish uchun 'Qabul qilaman' tugmasini bosing:"

    inline_keyboard = [
        [InlineKeyboardButton(button_text, url=offer_url)]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    user_language[update.effective_user.id] = language

    await query.edit_message_text(
        welcome_text,
        reply_markup=inline_markup,
        parse_mode='HTML'
    )

    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=reply_text,
        reply_markup=reply_markup
    )


async def show_main_menu(user_id, context, language):
    if language == 'ru':
        menu_text = "Рад тебя видеть! 👋\n\nТвое главное меню:"
        keyboard = [
            [KeyboardButton("🛒 Продать")],
            [KeyboardButton("💰 Купить")],
            [KeyboardButton("⚙️ Настройки")]
        ]
    else:
        menu_text = "Sizni ko'rganimdan xursandman! 👋\n\nSizning asosiy menyuingiz:"
        keyboard = [
            [KeyboardButton("🛒 Sotish")],
            [KeyboardButton("💰 Sotib olish")],
            [KeyboardButton("⚙️ Sozlamalar")]
        ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await context.bot.send_message(
        chat_id=user_id,
        text=menu_text,
        reply_markup=reply_markup
    )


async def show_sell_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    language = user_language.get(user_id, 'ru')

    if language == 'ru':
        categories_text = "Выберите категорию товара:"
        keyboard = [
            [KeyboardButton("👗 Платье")],
            [KeyboardButton("👠 Туфли")],
            [KeyboardButton("🕶 Аксессуары")],
            [KeyboardButton("🏮 Декор")],
            [KeyboardButton("📦 Другое")],
            [KeyboardButton("🔙 Назад в меню")]
        ]
    else:
        categories_text = "Mahsulot toifasini tanlang:"
        keyboard = [
            [KeyboardButton("👗 Ko'ylak")],
            [KeyboardButton("👠 Tufli")],
            [KeyboardButton("🕶 Aksessuarlar")],
            [KeyboardButton("🏮 Dekor")],
            [KeyboardButton("📦 Boshqa")],
            [KeyboardButton("🔙 Menyuga qaytish")]
        ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        text=categories_text,
        reply_markup=reply_markup
    )
    return CATEGORY


async def buy_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    language = user_language.get(user_id, 'ru')

    if language == 'ru':
        await update.message.reply_text(
            f"🛍 Все актуальные объявления в нашем канале:\n\n{CHANNEL_LINK}\n\n"
            f"Подписывайтесь и выбирайте! 👗"
        )
    else:
        await update.message.reply_text(
            f"🛍 Barcha dolzarb e'lonlar bizning kanalimizda:\n\n{CHANNEL_LINK}\n\n"
            f"Obuna bo'ling va tanlang! 👗"
        )

    # Возвращаемся в главное меню
    await show_main_menu(user_id, context, language)
    return ConversationHandler.END


async def category_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    language = user_language.get(user_id, 'ru')

    if user_id not in user_data:
        user_data[user_id] = {}

    if text in ["👗 Платье", "👗 Ko'ylak"]:
        user_data[user_id]['category'] = 'платье' if language == 'ru' else 'ko\'ylak'
        user_data[user_id]['category_emoji'] = '👗'
    elif text in ["👠 Туфли", "👠 Tufli"]:
        user_data[user_id]['category'] = 'туфли' if language == 'ru' else 'tufli'
        user_data[user_id]['category_emoji'] = '👠'
    elif text in ["🕶 Аксессуары", "🕶 Aksessuarlar"]:
        user_data[user_id]['category'] = 'аксессуары' if language == 'ru' else 'aksessuarlar'
        user_data[user_id]['category_emoji'] = '🕶'
    elif text in ["🏮 Декор"]:
        user_data[user_id]['category'] = 'декор' if language == 'ru' else 'dekor'
        user_data[user_id]['category_emoji'] = '🏮'
    elif text in ["📦 Другое", "📦 Boshqa"]:
        user_data[user_id]['category'] = 'другое' if language == 'ru' else 'boshqa'
        user_data[user_id]['category_emoji'] = '📦'

        if language == 'ru':
            await update.message.reply_text("Напишите название вашего товара:")
        else:
            await update.message.reply_text("Mahsulotingiz nomini yozing:")
        return CUSTOM_NAME
    elif text in ["🔙 Назад в меню", "🔙 Menyuga qaytish"]:
        await show_main_menu(user_id, context, language)
        return ConversationHandler.END

    if language == 'ru':
        keyboard = [
            [KeyboardButton("✨ Идеальное")],
            [KeyboardButton("🧼 После химчистки")],
            [KeyboardButton("🔍 Есть небольшие нюансы")],
            [KeyboardButton("🏷 Новое с биркой")]
        ]
        await update.message.reply_text(
            "Состояние:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    else:
        keyboard = [
            [KeyboardButton("✨ Mukammal")],
            [KeyboardButton("🧼 Kimyoviy tozalashdan keyin")],
            [KeyboardButton("🔍 Kichik nuqsonlari bor")],
            [KeyboardButton("🏷 Yangi, teg bilan")]
        ]
        await update.message.reply_text(
            "Holati:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    return CONDITION


async def custom_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    language = user_language.get(user_id, 'ru')

    user_data[user_id]['custom_name'] = update.message.text

    if language == 'ru':
        keyboard = [
            [KeyboardButton("✨ Идеальное")],
            [KeyboardButton("🧼 После химчистки")],
            [KeyboardButton("🔍 Есть небольшие нюансы")],
            [KeyboardButton("🏷 Новое с биркой")]
        ]
        await update.message.reply_text(
            "Состояние:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    else:
        keyboard = [
            [KeyboardButton("✨ Mukammal")],
            [KeyboardButton("🧼 Kimyoviy tozalashdan keyin")],
            [KeyboardButton("🔍 Kichik nuqsonlari bor")],
            [KeyboardButton("🏷 Yangi, teg bilan")]
        ]
        await update.message.reply_text(
            "Holati:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    return CONDITION


async def condition_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    language = user_language.get(user_id, 'ru')

    user_data[user_id]['condition'] = text

    if language == 'ru':
        await update.message.reply_text(
            "Размер (для одежды/обуви):",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙 Отмена")]], resize_keyboard=True)
        )
    else:
        await update.message.reply_text(
            "O'lcham (kiyim/poyabzal uchun):",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙 Bekor qilish")]], resize_keyboard=True)
        )
    return SIZE


async def size_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    language = user_language.get(user_id, 'ru')

    if text in ["🔙 Отмена", "🔙 Bekor qilish"]:
        await show_main_menu(user_id, context, language)
        return ConversationHandler.END

    user_data[user_id]['size'] = text

    if language == 'ru':
        await update.message.reply_text(
            "Комментарий (не больше 100 символов):\n"
            "Например: есть потайной дефект, особенности фасона и т.д."
        )
    else:
        await update.message.reply_text(
            "Izoh (100 ta belgidan oshmasin):\n"
            "Masalan: yashirin nuqsonlar, uslub xususiyatlari va h.k."
        )
    return COMMENT


async def comment_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    language = user_language.get(user_id, 'ru')

    if len(text) > 100:
        if language == 'ru':
            await update.message.reply_text("Комментарий слишком длинный! Не больше 100 символов. Попробуйте еще раз:")
        else:
            await update.message.reply_text("Izoh juda uzun! 100 ta belgidan oshmasin. Qaytadan urinib ko'ring:")
        return COMMENT

    user_data[user_id]['comment'] = text

    if language == 'ru':
        await update.message.reply_text(
            "Бренд (если нет или не знаете, так и напишите):"
        )
    else:
        await update.message.reply_text(
            "Brend (agar yo'q yoki bilmasangiz, shunday yozing):"
        )
    return BRAND


async def brand_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    language = user_language.get(user_id, 'ru')

    user_data[user_id]['brand'] = text

    if language == 'ru':
        await update.message.reply_text("Цена (в суммах):")
    else:
        await update.message.reply_text("Narxi (so'mda):")
    return PRICE


async def price_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    language = user_language.get(user_id, 'ru')

    price_text = re.sub(r'\s+', '', text)
    if not price_text.isdigit():
        if language == 'ru':
            await update.message.reply_text("Пожалуйста, введите число (только цифры):")
        else:
            await update.message.reply_text("Iltimos, raqam kiriting (faqat sonlar):")
        return PRICE

    price = int(price_text)
    user_data[user_id]['price'] = price
    recommended_price = int(price * 0.6)

    if language == 'ru':
        keyboard = [
            [KeyboardButton("✅ Принять рекомендованную цену")],
            [KeyboardButton("❌ Отказаться и оставить свою цену")]
        ]
        await update.message.reply_text(
            f"У нас клуб быстрых продаж. Чтобы объявление залетало, "
            f"рекомендуем цену {recommended_price} сум (это на 60% меньше вашей).\n\n"
            f"Выберите действие:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    else:
        keyboard = [
            [KeyboardButton("✅ Tavsiya etilgan narxni qabul qilish")],
            [KeyboardButton("❌ Rad etish va o'z narximni qoldirish")]
        ]
        await update.message.reply_text(
            f"Biz tez sotish klubimiz. E'lon tez sotilishi uchun "
            f"tavsiya etilgan narx {recommended_price} so'm (bu sizning narxingizdan 60% kam).\n\n"
            f"Harakatni tanlang:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

    user_data[user_id]['recommended_price'] = recommended_price
    return PRICE_CONFIRM


async def price_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    language = user_language.get(user_id, 'ru')

    if text in ["✅ Принять рекомендованную цену", "✅ Tavsiya etilgan narxni qabul qilish"]:
        user_data[user_id]['final_price'] = user_data[user_id]['recommended_price']
    elif text in ["❌ Отказаться и оставить свою цену", "❌ Rad etish va o'z narximni qoldirish"]:
        user_data[user_id]['final_price'] = user_data[user_id]['price']

    # Инициализируем список для фото
    if 'photos' not in user_data[user_id]:
        user_data[user_id]['photos'] = []

    category_emoji = user_data[user_id].get('category_emoji', '📦')
    category_name = user_data[user_id].get('custom_name', user_data[user_id]['category'])

    if language == 'ru':
        await update.message.reply_text(
            f"📸 Отправьте ваше великолепное {category_emoji} {category_name}!\n\n"
            f"Пришли 3–5 лучших фото. Обязательно:\n"
            f"• 1 фото на тебе (как сидит)\n"
            f"• 1 фото в текущем состоянии\n\n"
            f"💡 Подсказка от бота: «Качественные фото при дневном свете "
            f"продают в 5 раз быстрее!»\n\n"
            f"После отправки всех фото нажмите 'Готово'"
        )
        keyboard = [[KeyboardButton("✅ Готово")]]
    else:
        await update.message.reply_text(
            f"📸 Ajoyib {category_emoji} {category_name}ingizni yuboring!\n\n"
            f"3–5 ta eng yaxshi rasm yuboring. Majburiy:\n"
            f"• 1 ta sizdagi rasm (qanday qotishini ko'rsatish)\n"
            f"• 1 ta hozirgi holatdagi rasm\n\n"
            f"💡 Bot maslahati: «Kunduzgi yorug'likdagi sifatli rasmlar "
            f"5 marta tezroq sotiladi!»\n\n"
            f"Barcha rasmlarni jo'natgandan so'ng 'Tayyor' tugmasini bosing"
        )
        keyboard = [[KeyboardButton("✅ Tayyor")]]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await context.bot.send_message(
        chat_id=user_id,
        text="Загрузите фото:" if language == 'ru' else "Rasmlarni yuklang:",
        reply_markup=reply_markup
    )
    return PHOTO


async def photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    language = user_language.get(user_id, 'ru')

    if update.message.text in ["✅ Готово", "✅ Tayyor"]:
        # Проверяем количество фото
        photo_count = len(user_data[user_id].get('photos', []))

        if photo_count < 3:
            if language == 'ru':
                await update.message.reply_text(
                    f"Нужно минимум 3 фото. Сейчас загружено: {photo_count}. Отправьте еще фото:")
            else:
                await update.message.reply_text(
                    f"Kamida 3 ta rasm kerak. Hozir yuklangan: {photo_count}. Yana rasm yuboring:")
            return PHOTO

        # Переходим к запросу телефона
        if language == 'ru':
            await update.message.reply_text(
                "Оставьте номер телефона для связи:"
            )
        else:
            await update.message.reply_text(
                "Bog'lanish uchun telefon raqamingizni qoldiring:"
            )
        return PHONE

    # Получаем фото
    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()

        if 'photos' not in user_data[user_id]:
            user_data[user_id]['photos'] = []

        user_data[user_id]['photos'].append(photo_file)
        photo_count = len(user_data[user_id]['photos'])

        if language == 'ru':
            if photo_count >= 5:
                await update.message.reply_text(
                    f"✅ Фото {photo_count}/5 получено. Максимум 5 фото. Нажмите 'Готово' для продолжения."
                )
            else:
                await update.message.reply_text(
                    f"✅ Фото {photo_count}/5 получено. Можете отправить еще или нажмите 'Готово'."
                )
        else:
            if photo_count >= 5:
                await update.message.reply_text(
                    f"✅ Rasm {photo_count}/5 qabul qilindi. Maksimum 5 rasm. Davom etish uchun 'Tayyor' tugmasini bosing."
                )
            else:
                await update.message.reply_text(
                    f"✅ Rasm {photo_count}/5 qabul qilindi. Yana yuborishingiz mumkin yoki 'Tayyor' tugmasini bosing."
                )
    else:
        if language == 'ru':
            await update.message.reply_text("Пожалуйста, отправьте фото или нажмите 'Готово'")
        else:
            await update.message.reply_text("Iltimos, rasm yuboring yoki 'Tayyor' tugmasini bosing")

    return PHOTO


async def phone_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    language = user_language.get(user_id, 'ru')

    user_data[user_id]['phone'] = text

    # Публикуем объявление в канал
    if language == 'ru':
        post_text = (
            f"👗 НОВОЕ ОБЪЯВЛЕНИЕ\n\n"
            f"📌 Категория: {user_data[user_id].get('custom_name', user_data[user_id]['category'])}\n"
            f"📊 Состояние: {user_data[user_id]['condition']}\n"
            f"📏 Размер: {user_data[user_id]['size']}\n"
            f"📝 Комментарий: {user_data[user_id]['comment']}\n"
            f"🏷 Бренд: {user_data[user_id]['brand']}\n"
            f"💰 Цена: {user_data[user_id]['final_price']} сум\n"
            f"📞 Телефон: {user_data[user_id]['phone']}\n\n"
            f"Свяжитесь с продавцом для покупки! 🤍"
        )
    else:
        post_text = (
            f"👗 YANGI E'LON\n\n"
            f"📌 Kategoriya: {user_data[user_id].get('custom_name', user_data[user_id]['category'])}\n"
            f"📊 Holati: {user_data[user_id]['condition']}\n"
            f"📏 O'lcham: {user_data[user_id]['size']}\n"
            f"📝 Izoh: {user_data[user_id]['comment']}\n"
            f"🏷 Brend: {user_data[user_id]['brand']}\n"
            f"💰 Narxi: {user_data[user_id]['final_price']} so'm\n"
            f"📞 Telefon: {user_data[user_id]['phone']}\n\n"
            f"Sotuvchi bilan bog'lanib xarid qiling! 🤍"
        )

    # Отправляем фото в канал
    media_group = []
    for i, photo in enumerate(user_data[user_id]['photos'][:5]):  # Максимум 5 фото
        if i == 0:
            # Первое фото с подписью
            media_group.append(InputMediaPhoto(media=photo.file_id, caption=post_text))
        else:
            media_group.append(InputMediaPhoto(media=photo.file_id))

    # Отправляем в канал
    await context.bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)

    # Получаем ссылку на последнее сообщение в канале
    channel_post = await context.bot.send_message(chat_id=CHANNEL_ID, text="СПАСИБО!")
    message_link = f"https://t.me/secondbride_uz/{channel_post.message_id - 1}"

    # Отправляем подтверждение пользователю
    if language == 'ru':
        await update.message.reply_text(
            f"✅ Отлично! Ваше объявление опубликовано!\n\n"
            f"Ссылка на объявление: {message_link}\n\n"
            f"СПАСИБО!"
        )
    else:
        await update.message.reply_text(
            f"✅ Ajoyib! Sizning e'loningiz e'lon qilindi!\n\n"
            f"E'lon havolasi: {message_link}\n\n"
            f"RAHMAT!"
        )

    await show_main_menu(user_id, context, language)

    # Очищаем данные пользователя
    del user_data[user_id]

    return ConversationHandler.END


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'lang_ru':
        await show_offer(update, context, 'ru')
    elif query.data == 'lang_uz':
        await show_offer(update, context, 'uz')
    return ConversationHandler.END


async def handle_reply_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    language = user_language.get(user_id, 'ru')

    if text in ["✅ Принимаю условия", "✅ Shartlarni qabul qilaman"]:
        await show_main_menu(user_id, context, language)
        return ConversationHandler.END


def main():
    TOKEN = '8723040450:AAF6jRNVDUhuk74jGpeHnZAFwUGBQRnvtdQ'
    application = Application.builder().token(TOKEN).build()

    sell_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^(🛒 Продать|🛒 Sotish)$'), show_sell_categories)],
        states={
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, category_selected)],
            CUSTOM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, custom_name)],
            CONDITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, condition_selected)],
            SIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, size_entered)],
            COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, comment_entered)],
            BRAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, brand_entered)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, price_entered)],
            PRICE_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, price_confirm)],
            PHOTO: [MessageHandler(filters.PHOTO, photo_received),
                    MessageHandler(filters.Regex('^(✅ Готово|✅ Tayyor)$'), photo_received)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_entered)],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(
        MessageHandler(filters.Regex('^(✅ Принимаю условия|✅ Shartlarni qabul qilaman)$'), handle_reply_buttons))
    application.add_handler(MessageHandler(filters.Regex('^(💰 Купить|💰 Sotib olish)$'), buy_button))
    application.add_handler(sell_conv_handler)

    print("Бот запущен с новым токеном и каналом @secondbride_uz...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()