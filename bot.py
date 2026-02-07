import os
import openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from parser import load_menu
from dotenv import load_dotenv  

load_dotenv()

TOKEN = "8327223380:AAHJ2_zpjgo9_atO3611J5s9yI4ExQnO8OM"


menu = load_menu()




def main_menu_buttons():
    keyboard = []
    for cat_key, cat in menu.items():
        keyboard.append(
            [InlineKeyboardButton(cat["title"], callback_data=f"cat:{cat_key}")]
        )
    return InlineKeyboardMarkup(keyboard)


def quantity_buttons(cat_key, item_key):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("1️⃣", callback_data=f"qty:{cat_key}:{item_key}:1"),
            InlineKeyboardButton("2️⃣", callback_data=f"qty:{cat_key}:{item_key}:2"),
            InlineKeyboardButton("3️⃣", callback_data=f"qty:{cat_key}:{item_key}:3")
        ],
        [InlineKeyboardButton("🔙 Վերադառնալ մենյու", callback_data="back")]
    ])



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "☕ Coffee House\nԸնտրիր category 👇",
        reply_markup=main_menu_buttons()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Գրիր /start՝ մենյուն տեսնելու համար ☕")




async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # CATEGORY
    if data.startswith("cat:"):
        cat_key = data.split(":")[1]
        category = menu[cat_key]

        keyboard = []
        for item_key, item in category["items"].items():
            keyboard.append(
                [InlineKeyboardButton(item["name"], callback_data=f"item:{cat_key}:{item_key}")]
            )

        keyboard.append([InlineKeyboardButton("🔙 Վերադառնալ մենյու", callback_data="back")])

        await query.edit_message_text(
            text=f"{category['title']}\nԸնտրիր տեսակը 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ITEM
    elif data.startswith("item:"):
        _, cat_key, item_key = data.split(":")
        item = menu[cat_key]["items"][item_key]

        await query.edit_message_text(
            text=(
                f"☕ {item['name']}\n"
                f"💵 Գին՝ {item['price']} AMD\n\n"
                f"Քանի հատ եք ուզում?"
            ),
            reply_markup=quantity_buttons(cat_key, item_key)
        )

    # QUANTITY
    elif data.startswith("qty:"):
        _, cat_key, item_key, qty = data.split(":")
        qty = int(qty)

        item = menu[cat_key]["items"][item_key]
        total = item["price"] * qty

        await query.edit_message_text(
            text=(
                f"✅ Պատվերը ընդունված է\n\n"
                f"☕ {item['name']}\n"
                f"🔢 Քանակ՝ {qty}\n"
                f"💰 Ընդհանուր՝ {total} USD"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("☕ Նոր պատվեր", callback_data="back")]
            ])
        )

    # BACK
    elif data == "back":
        await query.edit_message_text(
            text="☕ Coffee House\nԸնտրիր category 👇",
            reply_markup=main_menu_buttons()
        )



def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
