import time
from aiogram import executor, types
from aiogram.dispatcher.filters import AdminFilter, IsReplyFilter

from config import adminId
from random import randint
from misc import bot, dp
import utils

words = ['сука', 'блять', 'хуй', 'педарас', 'пизда', 'говно', 'похуй', 'сука ня', 'suka nya', 'ебать', 'ебаний', 'дебил', 'педик', 'дурак', 'долбаеб']

bot_id = 5375004283

# Send admin message about bot started
async def send_adm(dp):
    await bot.send_message(chat_id=adminId, text='Bot restarted!')


# info tour
@dp.message_handler(commands=["start"], commands_prefix="!/")
async def welcome_send_info(message: types.Message):
    await message.answer(f"{message.from_user.full_name}, Привет {message.from_user.full_name}\n"
                         f"Я бот созданный для модерации чата)\n\n"
                         f"Команди бота  /commands\n"
                         f"Что то не понял? /help\n"
                         f"Поддержка по боту @MasterStroke777")

# info tour
@dp.message_handler(commands=["help"], commands_prefix="!/")
async def welcome_send_info(message: types.Message):
    await message.answer(f"Я бот для модерации чата и я помогаю админам чата\nДля начала добавь меня в чат и дай мне фулл админку (что би я мог делать всё в чате) тогда ти сможеж использовать весь мой функционал\nМои команди /commands\nПоддержка по боту @MasterStroke777")  

# info tour
@dp.message_handler(commands=['commands'])
async def welcome_send_info(message: types.Message):
    await message.answer(f"Команди бота доступни всем:\n\n"
                         f"/start - Старт бота\n"
                         f"/help - Помощь по боту\n"
                         f"/commands - Команди бота\n"
                         f"/me - Мои дание\n"
                         f"/dont_click_me - Выдать мут себе на рандомное число от 1 до 10 минут\n"
                         f"/bots - Боти нашей комании\n\n"
                         f"Команди для админов чата:\n\n"
                         f"/ban - Бан пользователя\n"
                         f"/unban - Разбан пользователя\n"
                 #        f"/kick - Кик пользователя\n"
                #         f"/unkick - Разкик пользователя\n"
                         f"/mute - Мут пользователя\n"
                         f"/unmute - Размут пользователя\n"
                         f"/del - Удалить собщенния\n"
                         f"/pin - Закрепить собщенния\n"
                         f"/unpin - Открепить собщенния\n\n"
                         f"Поддержка по боту @MasterStroke777")                                                

# new chat member
@dp.message_handler(content_types=["new_chat_members"])
async def new_chat_member(message: types.Message):
    await message.reply(f"Привет {message.new_chat_members[0].full_name},\nПожалуста не спамь и не пиши маты в чат!\nМои команды /commands")


# delete message user leave chat
@dp.message_handler(content_types=["left_chat_member"])
async def leave_chat(message: types.Message):
    await message.reply("Пока!")

#@dp.message_handler(commands = ["reply"])
#async def repl(message: types.Message):
#    await bot.send_message(int(message.text.split()[1]), message.text.replace(message.text.split()[1], "").replace("/reply", ""))

# user get info about him
@dp.message_handler(commands=["me"], commands_prefix="!/")
async def welcome(message: types.Message):
    if message.from_user.username is None:
        await message.reply(f"Имя - {message.from_user.full_name}\nID - {message.from_user.id}\n")
    else:
        await message.reply(f"Имя - {message.from_user.full_name}\n"
                            f"ID - <code>{message.from_user.id}</code>\n"
                            f"Username - @{message.from_user.username}\n")


# ban user
@dp.message_handler(is_chat_admin=True, commands=['ban'], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение")
        return

    user = await message.bot.get_chat_member(message.chat.id,
                                             message.reply_to_message.from_user.id)

    if message.reply_to_message.from_user.id == message.from_user.id:
        await message.reply("Нельзя забанить самого себя =)")
        return

    if user.is_chat_admin():
        await message.reply("Нельзя изменять права администраторов!")
        return

    user = message.reply_to_message.from_user
    if user.last_name is not None:
        await message.reply(f"Пользователь {user.first_name} {user.last_name} (@{user.username}) забанен навсегда!")
    else:
        await message.reply(f"Пользователь {user.first_name} (@{user.username}) забанен навсегда!")
    await message.bot.delete_message(message.chat.id, message.message_id)  # remove admin message
    await message.bot.kick_chat_member(chat_id=message.chat.id,
                                       user_id=message.reply_to_message.from_user.id
                                       )


@dp.message_handler(is_chat_admin=True, commands=["unban"], commands_prefix="!/")
async def cmd_unban(message: types.Message):
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение")
        return

    user = await message.bot.get_chat_member(message.chat.id,
                                             message.reply_to_message.from_user.id
                                             )
    if user.is_chat_admin():
        await message.reply("Нельзя изменять права администраторов")
        return

    user = message.reply_to_message.from_user
    if user.last_name is not None:
        await message.reply(f"Пользователь {user.first_name} {user.last_name} (@{user.username}) разбанен")
    else:
        await message.reply(f"Пользователь {user.first_name} (@{user.username}) разбанен")
    await message.bot.delete_message(message.chat.id, message.message_id)  # remove admin message
    await message.bot.unban_chat_member(chat_id=message.chat.id,
                                        user_id=message.reply_to_message.from_user.id)

# random mute chat member
@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['dont_click_me'],
commands_prefix='!/')
async def mute_random(message: types.Message):
    now_time = int(time.time())
    replied_user_id = message.from_user.id
    replied_user = message.from_user.full_name
    random_m = randint(1, 10)
    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=replied_user_id, can_send_messages=False,
                                   can_send_media_messages=False, can_send_other_messages=False,
                                   until_date=now_time + 60 * random_m)
    if not message.from_user.username == None:
        await message.reply(f"Пользователю @{message.reply_to_message.from_user.username} видан мут на рандомное число, {random_m} минут.")   
    if message.from_user.username == None:
        await message.reply(f"Пользователю [<code>{message.from_user.id}</code>] <code>{message.from_user.full_name}</code> видан мут на рандомное число, {random_m} минут.")

# unmute user in chat
@dp.message_handler(is_chat_admin=True, commands="mute", commands_prefix="!/")
async def cmd_readonly(message: types.Message):
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение")
        return

    # Admins cannot be restricted
    user = await message.bot.get_chat_member(message.chat.id,
                                             message.reply_to_message.from_user.id
                                             )
    if user.is_chat_admin():
        await message.reply("Нельзя изменять права администраторов")
        return

    words = message.text.split()
    if len(words) > 1:  # !mute with arg
        restriction_time = utils.get_restriction_time(words[1])
        if not restriction_time:
            await message.reply(
                "Неправильный формат времени!\nИспользуйте число + символ m, h или d.\nНапример: <code>!mute 7d</code>"
            )
            return
    else:
        restriction_time = 86400 * 367

    now_time = int(time.time())

    await message.bot.restrict_chat_member(message.chat.id,
                                           message.reply_to_message.from_user.id,
                                           types.ChatPermissions(),
                                           until_date=now_time + restriction_time
                                           )

    user = message.reply_to_message.from_user
    if len(words) > 1:
            await message.reply(f"Пользователю {user.full_name} (@{user.username}) выдан мут на " + (
                "{restriction_time}").format(restriction_time=words[1]))
    else:
            await message.reply(
                f"Пользователю {user.full_name} (@{user.username}) выдан мут навсегда")


@dp.message_handler(is_chat_admin=True, commands="unmute", commands_prefix="!/")
async def cmd_unreadonly(message: types.Message):
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение")
        return

    user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply("Нельзя изменять права администраторов!")
        return

    await message.bot.restrict_chat_member(message.chat.id,
                                           message.reply_to_message.from_user.id,
                                           types.ChatPermissions(
                                               can_send_messages=True,
                                               can_send_media_messages=True,
                                               can_send_polls=True,
                                               can_send_other_messages=True,
                                               can_add_web_page_previews=True,
                                               can_change_info=True,
                                               can_invite_users=True,
                                               can_pin_messages=True)
                                           )

    user = message.reply_to_message.from_user
    await message.reply(f"Пользователь {user.full_name} (@{user.username}) размучен")

# pin chat message
@dp.message_handler(AdminFilter(is_chat_admin=True), IsReplyFilter(is_reply=True),
                    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['pin'], commands_prefix='!/')
async def pin_message(message: types.Message):
    msg_id = message.reply_to_message.message_id
    await bot.pin_chat_message(message_id=msg_id, chat_id=message.chat.id)

@dp.message_handler(AdminFilter(is_chat_admin=True), IsReplyFilter(is_reply=False), commands=['pin'],
                    commands_prefix='!/', chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def ban(message: types.Message):
    await message.reply("Команда должна быть ответом на собщенния!")

# unpin chat message
@dp.message_handler(AdminFilter(is_chat_admin=True), IsReplyFilter(is_reply=True), commands_prefix='!/',
                    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['unpin'])
async def unpin_message(message: types.Message):
    msg_id = message.reply_to_message.message_id
    await bot.unpin_chat_message(message_id=msg_id, chat_id=message.chat.id)

@dp.message_handler(AdminFilter(is_chat_admin=True), IsReplyFilter(is_reply=False), commands=['unpin'],
                    commands_prefix='!/', chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def ban(message: types.Message):
    await message.reply("Команда должна бить ответом на собщенния!")          

# delete user message
@dp.message_handler(AdminFilter(is_chat_admin=True), IsReplyFilter(is_reply=True), commands_prefix='!/',
                    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['del'])
async def delete_message(message: types.Message):
    msg_id = message.reply_to_message.message_id
    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@dp.message_handler(AdminFilter(is_chat_admin=True), IsReplyFilter(is_reply=False), commands=['del'],
                    commands_prefix='!/', chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def ban(message: types.Message):
    await message.reply("Команда должна быть ответом на собщенния!")
# get chat admins list
@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['admins'],
                    commands_prefix='!/')
async def get_admin_list(message: types.Message):
    admins_id = [(admin.user.id, admin.user.full_name) for admin in await bot.get_chat_administrators(
        chat_id=message.chat.id)]
    admins_list = []
    for ids, name in admins_id:
        admins_list.append("".join(f"[{name}]"))
    result_list = ""
    for admins in admins_list:
        result_list += "".join(admins) + '\n'
    await message.reply("Админи чата:\n" + result_list, parse_mode=types.ParseMode.MARKDOWN)


# report about spam or something else
@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['report'],
                      commands_prefix='!/')
async def report_by_user(message: types.Message):
    msg_id = message.reply_to_message.message_id
    user_id = message.from_user.id
    admins_list = [admin.user.id for admin in await bot.get_chat_administrators(chat_id=message.chat.id)]
    try:
      for adm_id in admins_list:
       await bot.send_message(text=f"🆘Жалоба в чате\nПользователь <code>{message.from_user.full_name}</code> [<code>{message.from_user.id}</code>] @{message.from_user.username} отправил жалобу на <code>{message.reply_to_message.from_user.username}</code> [<code>{message.reply_to_message.from_user.id}</code>] <code>{message.reply_to_message.from_user.full_name}</code>\nПричина жалобы: {message.text[8:]}",
                                   chat_id=adm_id, parse_mode=types.ParseMode.HTML,
                                   disable_web_page_preview=True)
    except:
        pass

    await message.reply(f"Жалоба на пользователя @{message.reply_to_message.from_user.username}\nПричина: {message.text[8:]}\nОтправлено админам!")


# # delete links and tags from users, allow for admins
@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], content_types=['text'])
async def delete_links(message: types.Message):
    await bot.send_message(837817771, f'[@{message.from_user.username}] [<code>{message.from_user.id}</code>] [<code>{message.from_user.full_name}</code>], chat_id=[<code>{message.chat.id}</code>]\n{message.text[0:]}')    
    for word in words:
            if word in message.text.lower():
                await message.delete()
                till_date = "1m"

                if till_date[-1] == "m":
                    ban_for = int(till_date[:-1]) * 60

                now_time = int(time.time())
                await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.from_user.id, can_send_messages=False,
                                   can_send_media_messages=False, can_send_other_messages=False,
                                   until_date=now_time + ban_for)                
                if not message.from_user.username == None:                                   
                    await message.answer(f"Пользователь @{message.from_user.username} нарушив правила чата и написав мат в чате и поетому получил мут на 1 минуту.")
                if message.from_user.username == None:   
                    await message.answer(f"Пользователь [<code>{message.from_user.id}</code>] <code>{message.from_user.full_name}</code> нарушив правила чата и написав мат в чате и поетому получил мут на 1 минуту.")   

# Polling
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=send_adm, skip_updates=True)
