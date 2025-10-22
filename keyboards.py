from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup,InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import emoji

btn_info = KeyboardButton(f"{emoji.INFORMATION} Info")
btn_games = KeyboardButton(f"{emoji.VIDEO_GAME} Games")
btn_profile = KeyboardButton(f"{emoji.PERSON} Profile")
btn_time = KeyboardButton(f"{emoji.WATCH} Time")

btn_rps = KeyboardButton(f"{emoji.SCISSORS} Rock, Paper, Scissors")
btn_quest = KeyboardButton(f"{emoji.POSTBOX} Quest")
btn_back = KeyboardButton(f"{emoji.BACK_ARROW} Back")

btn_rps_rock = KeyboardButton(f"{emoji.ROCK} Rock")
btn_rps_paper = KeyboardButton(f"{emoji.BOOKS} Paper")
btn_rps_scissors = KeyboardButton(f"{emoji.SCISSORS} Scissors")

# Quest
# Starting choice
inline_kb_start_mission = InlineKeyboardMarkup([
    [InlineKeyboardButton("🚀 Start the mission", callback_data='start_mission')]
])

# First decision
inline_kb_first_path = InlineKeyboardMarkup([
    [InlineKeyboardButton("🌌 Explore the dark cave", callback_data='dark_cave')],
    [InlineKeyboardButton("🌿 Follow the glowing plants", callback_data='glowing_plants')]
])

# Dark cave options
inline_kb_dark_cave = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔫 Use your laser blaster", callback_data='laser')],
    [InlineKeyboardButton("🪨 Hide behind the rocks", callback_data='hide')]
])

# Glowing plant path
inline_kb_alien_shrine = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔮 Crystal orb", callback_data='crystal_orb')],
    [InlineKeyboardButton("⚡ Energy blade", callback_data='energy_blade')],
    [InlineKeyboardButton("📜 Encrypted scroll", callback_data='bad_scroll')]  # BAD ENDING
])

inline_kb_start_quest = InlineKeyboardMarkup([[InlineKeyboardButton("Start a quest", callback_data="Start quest")]])

btn_image = KeyboardButton(f"{emoji.FRAMED_PICTURE} Image Generation")

btn_size = KeyboardButton(f"{emoji.UP_ARROW} Size")
btn_width = KeyboardButton(f"{emoji.RIGHT_ARROW} Width")
btn_height = KeyboardButton(f"{emoji.DOWN_ARROW} Height")
btn_style = KeyboardButton(f"{emoji.ARTIST} Style")

btn_leaderboard = KeyboardButton("🏆 Leaderboard")

# New inline keyboards for image generation
kb_style = InlineKeyboardMarkup([
    [InlineKeyboardButton("Kandinsky", callback_data="style_kandinsky")],
    [InlineKeyboardButton("Anime", callback_data="style_anime")],
])

kb_size = InlineKeyboardMarkup([
    [InlineKeyboardButton("Small (248p)", callback_data="size_small")],
    [InlineKeyboardButton("Medium (496p)", callback_data="size_medium")],
    [InlineKeyboardButton("Big (1080p)", callback_data="size_big")],
])

# Combined keyboard for initial image prompt
kb_image_start = InlineKeyboardMarkup([
    [InlineKeyboardButton("Set Style", callback_data="set_style")],
    [InlineKeyboardButton("Set Size", callback_data="set_size")],
    [InlineKeyboardButton("Generate", callback_data="generate_image")]
])

kb_main = ReplyKeyboardMarkup(
    keyboard=[
                [btn_info, btn_games, btn_profile, btn_time, btn_image],
            ],
    resize_keyboard=True,
)

kb_games = ReplyKeyboardMarkup(
    keyboard=[
                [btn_rps],
                [btn_quest, btn_back],
    ],
    resize_keyboard=True,
)

kb_rps = ReplyKeyboardMarkup(
    keyboard=[
                [btn_rps_rock, btn_rps_paper, btn_rps_scissors],
                [btn_leaderboard, btn_back]
    ],
    resize_keyboard=True,

)

kb_images = ReplyKeyboardMarkup(
    keyboard=[
        [btn_size], [btn_width], [btn_height], [btn_style],
    ],
    resize_keyboard=True,
)

