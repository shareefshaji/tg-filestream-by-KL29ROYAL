import datetime
import math
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums.parse_mode import ParseMode
from WebStreamer import __version__
from WebStreamer.bot import StreamBot
from WebStreamer.utils.bot_utils import file_format
from WebStreamer.vars import Var
from WebStreamer.utils.Translation import Language, BUTTON
from WebStreamer.utils.database import Database
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.server.exceptions import FIleNotFound

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


@StreamBot.on_callback_query()
async def cb_data(bot, update: CallbackQuery):
    lang = Language(update)
    usr_cmd = update.data.split("_")

    if usr_cmd[0] == "home":
        await update.message.edit_text(
            text=lang.START_TEXT.format(update.from_user.mention),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=BUTTON.START_BUTTONS
        )

    elif usr_cmd[0] == "help":
        await update.message.edit_text(
            text=lang.HELP_TEXT.format(Var.UPDATES_CHANNEL),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=BUTTON.HELP_BUTTONS
        )

    elif usr_cmd[0] == "about":
        await update.message.edit_text(
            text=lang.ABOUT_TEXT.format(__version__),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=BUTTON.ABOUT_BUTTONS
        )

    elif usr_cmd[0] == "info":
        user = await db.get_user(update.from_user.id)
        files = await db.total_files(update.from_user.id)
        links = "N/A"
        if (user.get("Plan") == "Free") and Var.LINK_LIMIT:
            links = Var.LINK_LIMIT - files
        await update.message.edit_text(
            text=lang.INFO_TEXT.format(update.from_user.id, user.get("Plan"), files, links),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Home", callback_data="home"),
                 InlineKeyboardButton("❌ Close", callback_data="close")]
            ])
        )

    elif usr_cmd[0] == "N/A":
        await update.answer("N/A", True)

    elif usr_cmd[0] == "close":
        await update.message.delete()

    elif usr_cmd[0] == "msgdelconf2":
        await update.message.edit_caption(
            caption=(
                "🗑️ <b>Confirm Delete</b>\n\n"
                "Are you sure you want to delete this file link?\n\n"
                + update.message.caption
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Yes, Delete", callback_data=f"msgdelyes_{usr_cmd[1]}_{usr_cmd[2]}"),
                    InlineKeyboardButton("❌ Cancel", callback_data=f"myfile_{usr_cmd[1]}_{usr_cmd[2]}")
                ]
            ])
        )

    elif usr_cmd[0] == "msgdelyes":
        await delete_user_file(usr_cmd[1], update)
        return

    elif usr_cmd[0] == "userfiles":
        file_list, total_files = await gen_file_list_button(int(usr_cmd[1]), update.from_user.id)
        await update.message.edit_caption(
            caption=f"📁 <b>My Files</b>\n\n📊 Total: <code>{total_files}</code> file(s)",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(file_list)
        )

    elif usr_cmd[0] == "myfile":
        await gen_file_menu(usr_cmd[1], usr_cmd[2], update)
        return

    elif usr_cmd[0] == "accepttos":
        await db.agreed_tos(int(usr_cmd[1]))
        await update.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ TOS Accepted", callback_data="N/A")]
            ])
        )

    elif usr_cmd[0] == "sendfile":
        myfile = await db.get_file(usr_cmd[1])
        await update.answer(f"📤 Sending: {myfile['file_name']}")
        await update.message.reply_cached_media(myfile['file_id'])

    else:
        await update.message.delete()


async def gen_file_list_button(file_list_no: int, user_id: int):
    file_range = [file_list_no * 10 - 10 + 1, file_list_no * 10]
    user_files, total_files = await db.find_files(user_id, file_range)

    file_list = []
    async for x in user_files:
        file_list.append([
            InlineKeyboardButton(f"📄 {x['file_name']}", callback_data=f"myfile_{x['_id']}_{file_list_no}")
        ])

    if total_files > 10:
        total_pages = math.ceil(total_files / 10)
        file_list.append([
            InlineKeyboardButton(
                "⬅️", callback_data="userfiles_" + str(file_list_no - 1) if file_list_no > 1 else "N/A"
            ),
            InlineKeyboardButton(f"📄 {file_list_no}/{total_pages}", callback_data="N/A"),
            InlineKeyboardButton(
                "➡️", callback_data="userfiles_" + str(file_list_no + 1) if total_files > file_list_no * 10 else "N/A"
            )
        ])

    if not file_list:
        file_list.append([InlineKeyboardButton("📭 No Files Found", callback_data="N/A")])

    return file_list, total_files


async def gen_file_menu(_id, file_list_no, update: CallbackQuery):
    try:
        myfile_info = await db.get_file(_id)
    except FIleNotFound:
        await update.answer("⚠️ File not found!")
        return

    file_type = file_format(myfile_info['file_id'])
    page_link = f"{Var.URL}watch/{myfile_info['_id']}"
    stream_link = f"{Var.URL}dl/{myfile_info['_id']}"

    TiMe = myfile_info['time']
    if isinstance(TiMe, float):
        date = datetime.datetime.fromtimestamp(TiMe)
        date_str = str(date.date())
        time_str = date.time().strftime("%I:%M:%S %p")
    else:
        date_str = str(TiMe)
        time_str = "N/A"

    caption = (
        f"📂 <b>File Details</b>\n\n"
        f"📄 <b>Name:</b> <code>{myfile_info['file_name']}</code>\n"
        f"📦 <b>Size:</b> <i>{humanbytes(int(myfile_info['file_size']))}</i>\n"
        f"🎞️ <b>Type:</b> <i>{file_type}</i>\n"
        f"📅 <b>Date:</b> <i>{date_str}</i>\n"
        f"🕐 <b>Time:</b> <i>{time_str}</i>"
    )

    await update.edit_message_caption(
        caption=caption,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⬅️ Back", callback_data=f"userfiles_{file_list_no}"),
                InlineKeyboardButton("🗑️ Delete Link", callback_data=f"msgdelconf2_{myfile_info['_id']}_{file_list_no}")
            ],
            [
                InlineKeyboardButton("🖥️ Watch Online", url=page_link),
                InlineKeyboardButton("📥 Download", url=stream_link)
            ],
            [
                InlineKeyboardButton("📤 Get File", callback_data=f"sendfile_{myfile_info['_id']}")
            ]
        ])
    )


async def delete_user_file(_id, update: CallbackQuery):
    try:
        myfile_info = await db.get_file(_id)
    except FIleNotFound:
        await update.answer("⚠️ File not found!")
        return

    await db.delete_one_file(myfile_info['_id'])
    await update.message.edit_caption(
        caption=(
            "✅ <b>Link Deleted Successfully</b>\n\n"
            + update.message.caption.replace("Do You Want to Delete the file", "").strip()
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back to My Files", callback_data="userfiles_1")]
        ])
    )