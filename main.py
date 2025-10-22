from pyrogram import Client, filters
import config
import datetime
import keyboards
import random
import json
from FusionBrain_AI import generate
import base64
from pyrogram.types import ForceReply

# Initialize Telegram bot client
bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="WreckedBot"
)

# Store user states for image generation (prompt, style, size)
user_states = {}

def button_filter(button):
    """Create a filter for button text matching."""
    async def func(_, __, msg):
        return msg.text == button.text
    return filters.create(func, "ButtonFilter", button=button)

# Helper Functions
def load_users():
    """Load user data from users.json."""
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    """Save user data to users.json."""
    with open("users.json", "w") as file:
        json.dump(users, file, indent=2)

# Command Handlers
@bot.on_message(filters.command("start"))
async def start(client, message):
    """Handle /start command: Initialize user and show welcome message."""
    user_id = str(message.from_user.id)
    users = load_users()
    if user_id not in users:
        users[user_id] = 100  # Initialize with 100 funds
        save_users(users)
    await message.reply("Nice to meet you!")
    await bot.send_sticker(
        message.chat.id,
        "CAACAgIAAxkBAAEOvUhoVYMKUEUGcSxIWswhOTH5CKCYYQACAQADwDZPExguczCrPy1RNgQ",
        reply_markup=keyboards.kb_main
    )

## 1
@bot.on_message(filters.command("info") | button_filter(keyboards.btn_info))
async def info(client, message):
    """Handle /info command: Display available commands."""
    await message.reply(
        "Here are all of the available commands :)\n"
        "/start - Start the Conversation\n"
        "/games - Play games\n"
        "/leaderboard - View top players\n"
        "/image - Generate an image\n"
        "/profile - View bot profile",
        reply_markup=keyboards.kb_main
    )

@bot.on_message(filters.command("time") | button_filter(keyboards.btn_time))
async def time(client, message):
    """Handle /time command: Show current time."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    await message.reply(f"Your current time is {current_time} (HH:mm:ss).", reply_markup=keyboards.kb_main)

@bot.on_message(filters.command("profile") | button_filter(keyboards.btn_profile))
async def profile(bot, message):
    """Handle /profile command: Display bot's biography."""
    bot_name = "Virtual Assistant made by Antypas"
    description = (
        "The best ever virtual assistant!\n"
        "This Virtual Assistant was made by Antypas Aintinidis for their Python Project. "
        "This project will be showcased to professionals for RocketCoins. "
        "I hope you like this biography."
    )
    await message.reply(f"{bot_name}\n{description}", reply_markup=keyboards.kb_main)

# Game Handlers
@bot.on_message(filters.command("games") | button_filter(keyboards.btn_games))
async def games(client, message):
    """Handle /games command: Show game selection menu."""
    await message.reply("Choose a game: )", reply_markup=keyboards.kb_games)

@bot.on_message(button_filter(keyboards.btn_rps))
async def rps(client, message):
    """Handle rock-paper-scissors game: Check funds and start game."""
    user_id = str(message.from_user.id)
    users = load_users()
    if users.get(user_id, 0) >= 10:
        users[user_id] -= 10  # Deduct 10 funds to play
        save_users(users)
        await message.reply("Your turn: ", reply_markup=keyboards.kb_rps)
    else:
        await message.reply(
            f"Not enough funds. You have {users.get(user_id, 0)}. The minimum to play is 10.",
            reply_markup=keyboards.kb_games
        )

@bot.on_message(
    button_filter(keyboards.btn_rps_rock) |
    button_filter(keyboards.btn_rps_paper) |
    button_filter(keyboards.btn_rps_scissors)
)
async def choice_rps(bot, message):
    """Handle rock-paper-scissors choice: Process game logic and update funds."""
    user_id = str(message.from_user.id)
    users = load_users()
    rock = keyboards.btn_rps_rock.text
    paper = keyboards.btn_rps_paper.text
    scissors = keyboards.btn_rps_scissors.text
    user = message.text
    pc = random.choice([rock, scissors, paper])
    if user == pc:
        await message.reply("Draw")
    elif (user == rock and pc == scissors) or (user == paper and pc == rock) or (user == scissors and pc == paper):
        users[user_id] = users.get(user_id, 0) + 20
        await message.reply(f"You have won! Congratulations! The bot chose {pc}. You earned 20 funds!")
        save_users(users)
    else:
        await message.reply(f"You have lost! The bot chose {pc}")
    await message.reply("Choose a game: )", reply_markup=keyboards.kb_games)

@bot.on_message(filters.command("quest") | button_filter(keyboards.btn_quest))
async def quest(bot, message):
    """Handle /quest command: Start interactive story."""
    await message.reply_text(
        "Would you like to go on an exciting journey full of adventure and mystery?",
        reply_markup=keyboards.inline_kb_start_quest
    )

# Image Generation Handlers
@bot.on_message(filters.command("image") | button_filter(keyboards.btn_image))
async def image_command(bot, message):
    """Handle /image command: Initialize image generation flow."""
    user_id = str(message.from_user.id)
    user_states[user_id] = {"prompt": None, "style": "kandinsky", "size": "medium"}
    await message.reply("Choose an option for image generation:", reply_markup=keyboards.kb_image_start)

@bot.on_message(filters.reply)
async def reply(bot, message):
    """Handle replies: Process image generation prompt."""
    user_id = str(message.from_user.id)
    if message.reply_to_message.text == "Enter a prompt to generate an image:" and user_id in user_states:
        user_states[user_id]["prompt"] = message.text.strip()
        await generate_image(bot, message, user_id)
    else:
        await message.reply_text("Please use the image generation flow to set a prompt.", reply_markup=keyboards.kb_main)

async def generate_image(bot, message, user_id):
    """Generate and send an image using FusionBrain AI API."""
    state = user_states.get(user_id, {"prompt": None, "style": "kandinsky", "size": "medium"})
    prompt, style, size = state["prompt"], state["style"], state["size"]
    if not prompt:
        await message.reply_text("No prompt provided. Please set a prompt.", reply_markup=keyboards.kb_image_start)
        return
    await message.reply_text(f"Generating image with prompt '{prompt}', style '{style}', size '{size}'... Please wait.")
    try:
        images = await generate(prompt, style, size)
        if images:
            image_data = base64.b64decode(images[0])
            img_num = random.randint(1, 99)
            with open(f"images/image{img_num}.jpg", "wb") as file:
                file.write(image_data)
            await bot.send_photo(
                message.chat.id,
                f"images/image{img_num}.jpg",
                caption=f"Generated image with prompt '{prompt}', style '{style}', size '{size}'",
                reply_to_message_id=message.id,
                reply_markup=keyboards.kb_main
            )
            user_states.pop(user_id, None)
        else:
            await message.reply_text("Failed to generate image. Please try again.", reply_markup=keyboards.kb_main)
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}. Please try again.", reply_markup=keyboards.kb_main)

# Leaderboard Handler
@bot.on_message(filters.command("leaderboard") | button_filter(keyboards.btn_leaderboard))
async def leaderboard(bot, message):
    """Handle /leaderboard command: Display top 5 players by funds."""
    users = load_users()
    sorted_list = sorted(users.items(), key=lambda x: x[1], reverse=True)
    msg_text = "🏆 Top 5 Players 🏆\n\n"
    for pos, (user_id, funds) in enumerate(sorted_list[:5], 1):
        try:
            user = await bot.get_users(int(user_id))
            username = user.username or user.first_name or user_id
        except:
            username = user_id
        msg_text += f"{pos}. {username} — {funds} funds\n"
    if not sorted_list:
        msg_text = "No players in the leaderboard yet!"
    await message.reply(msg_text, reply_markup=keyboards.kb_main)

# Callback Query Handler
@bot.on_callback_query()
async def handle_query(bot, query):
    """Handle inline keyboard callbacks for quest and image generation."""
    user_id = str(query.from_user.id)
    if query.data == "Start quest":
        await bot.answer_callback_query(query.id, text="Welcome to the quest: Stranded with a Spaceship!", show_alert=True)
        await query.message.reply_text(
            "Captain, your ship has crash-landed on an unknown planet. Do you want to explore the area?",
            reply_markup=keyboards.inline_kb_first_path
        )
    elif query.data == "dark_cave":
        await query.message.reply_text(
            "You enter the cave and hear growling. A wild alien creature appears!",
            reply_markup=keyboards.inline_kb_dark_cave
        )
    elif query.data == "glowing_plants":
        await query.message.reply_text(
            "You find an ancient alien shrine with three glowing items. You can pick one.",
            reply_markup=keyboards.inline_kb_alien_shrine
        )
    elif query.data == "laser":
        await bot.answer_callback_query(query.id, text="Use blaster - You fight bravely and defeat the alien!", show_alert=True)
    elif query.data == "hide":
        await bot.answer_callback_query(query.id, text="Hide → The alien sniffs around and leaves. You survive, barely.", show_alert=True)
    elif query.data == "crystal_orb":
        await bot.answer_callback_query(query.id, text="Crystal orb → You see visions of the planet’s secrets. You now know the safe route.", show_alert=True)
    elif query.data == "energy_blade":
        await bot.answer_callback_query(query.id, text="Energy blade → You gain a powerful weapon to defend yourself!", show_alert=True)
    elif query.data == "bad_scroll":
        await bot.answer_callback_query(
            query.id,
            text="You try to decrypt the scroll... But it's a trap! The scroll emits a blinding pulse, and you lose consciousness. When you wake up, everything is gone - even your memory. You are lost",
            show_alert=True
        )
    elif query.data == "set_style":
        await bot.answer_callback_query(query.id)
        await query.message.reply_text("Select a style:", reply_markup=keyboards.kb_style)
    elif query.data == "set_size":
        await bot.answer_callback_query(query.id)
        await query.message.reply_text("Select a size:", reply_markup=keyboards.kb_size)
    elif query.data in ["style_kandinsky", "style_anime"]:
        style = "kandinsky" if query.data == "style_kandinsky" else "anime"
        user_states[user_id]["style"] = style
        await bot.answer_callback_query(query.id, text=f"Style set to {style.capitalize()}")
        await query.message.reply_text(f"Style set to {style.capitalize()}. Choose an option:", reply_markup=keyboards.kb_image_start)
    elif query.data in ["size_small", "size_medium", "size_big"]:
        size = query.data.replace("size_", "")
        user_states[user_id]["size"] = size
        await bot.answer_callback_query(query.id, text=f"Size set to {size.capitalize()}")
        await query.message.reply_text(f"Size set to {size.capitalize()}. Choose an option:", reply_markup=keyboards.kb_image_start)
    elif query.data == "generate_image":
        if user_id not in user_states or user_states[user_id]["prompt"] is None:
            await bot.answer_callback_query(query.id)
            await query.message.reply_text("Enter a prompt to generate an image:", reply_markup=ForceReply(True))
        else:
            await bot.answer_callback_query(query.id)
            await generate_image(bot, query.message, user_id)

@bot.on_message(filters.command("back") | button_filter(keyboards.btn_back))
async def back(client, message):
    """Handle /back command: Return to main menu."""
    await message.reply("Back to main menu.", reply_markup=keyboards.kb_main)

bot.run()