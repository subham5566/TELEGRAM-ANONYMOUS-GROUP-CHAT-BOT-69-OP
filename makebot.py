#!/usr/bin/env python3
# -*- coding: utf8 -*-
# Made by Make http://github.com/mak3e
#

# Imports
from telegram.ext import Updater, CommandHandler, MessageHandler  # python-telegram-bot
from threading import Thread
from datetime import datetime
import threading
import sqlite3
import animals

# Variables
ids = []
token = ""  # Bot token here
token = open("TOKEN").read().split("\n")[0]
print(token)
if not token:
    raise ValueError('please add token')
todo = []  # Used for storing send jobs
conn = sqlite3.connect('data.db', check_same_thread=False, isolation_level=None)  # Init sqlite db
c = conn.cursor()  # Database cursor
lock = threading.Lock()  # Lock used for threading
custom_names = {1: "admin"}  # Used for special names

# Strings
bot_name = "BOT"  # Bot name show in bot messages
with open("BUILD", "r") as f:
    build = f.read()  # Get build number from BUILD file
version = "0.3_" + str(build)  # Version is version+build
author = "Make"  # Author
help_text = "Untergrund Chat @TheVillageChats Chat-Netzwerks.\n\nHier kannst du Anonym mit anderen schreiben.\n\n/help - Help\n/license - Shows the license\n/info - Information about your identity and the server\n/renew - Renews your identity\n/stop - Stops the bot"
license_text = "The Bot is hosted by @GeloMyrtol. It's free software (like in freedom not in free beer) and is available under MIT Lizenz at https://github.com/Bergiu/makebot."
welcome_text = "Welcome to the chatbot! Say hello to everyone! Made by {{author}}!"  # Shown for new users
stats_text = "Chat info\nYour name: {{name}}\nCurrent room: {{room}}\nTotal users: {{users}}\nVersion {{version}}"  # Statistic text
name_text = "Your new ID is {{name}}"  # Shown for users renewing their identity
room_text = "Rooms\nYou can join rooms using /join room\n{{rooms}}"  # Not implemented
update_text = "Chatbot updated to version {{version}}\nUpdate notes:\n+Testing if code works with newest python-telegram-bot"  # Text shown when bot is run
unknown_text = "Unknown command!"  # Text shown when unknown command is typed
exit_text = "Bye bye {{name}}! You can always come back by using /start"  # Text shown when /stop is used


# main
def main():
    updater = Updater(token)  # Updater, check python-telegram-bot docs
    dispatcher = updater.dispatcher  # Dispatcher, check ptb docs
    dispatcher.add_handler(CommandHandler('help', help))  # help command
    dispatcher.add_handler(CommandHandler('license', license))  # license command
    dispatcher.add_handler(CommandHandler('start', start))  # define start command
    dispatcher.add_handler(CommandHandler('renew', renew))  # same for renew
    dispatcher.add_handler(CommandHandler('info', info))  # same for info
    dispatcher.add_handler(CommandHandler('rooms', rooms))  # experimental and not implemented
    dispatcher.add_handler(MessageHandler([], message))  # message handler
    dispatcher.add_handler(CommandHandler('stop', stop))  # define stop command
    # dispatcher.addUnknownTelegramCommandHandler(unknown)  # used for unknown commands
    Thread(target=process).start()  # initialize process thread
    queue(Thread(target=send, args=(updater.bot, bot_name, send_text, 1, 0, update_text,)))  # add send update_text job to queue
    updater.start_polling()  # start polling for messages
    updater.idle()  # idle


# todo worker
def process():
    while 1:  # forever
        if len(todo) > 0:  # if there is jobs in todo list
            try:
                todo[0].start()  # try to start a job
                todo.pop(0)  # and remove it from queue
            except Exception:
                pass  # if job cannot be started this time (this will happen) try again


# queue
def queue(action):
    todo.append(action)  # and Thread object (job) to todo list


def sql(query, ret=0):  # sql query parsing helper
    try:
        lock.acquire(True)  # use lock (otherwise threading and sqlite dont work together)
        c.execute(query)  # exec query
        if ret:  # if return flag is set
            return c.fetchall()  # return stuff
    finally:
        lock.release()  # release the lock


# use this for logging
def log(message):  # log a message to log file
    log_text = str(datetime.now()) + ": " + message + "\n"
    with open("log", "a") as f:
        f.write(log_text)


# /help
def help(bot, update):
    queue(Thread(target=send, args=(bot, bot_name, send_text, 2, update.message.chat_id, help_text,)))  # send help text


# /license
def license(bot, update):
    queue(Thread(target=send, args=(bot, bot_name, send_text, 2, update.message.chat_id, license_text,)))  # send license text


# /start
def start(bot, update):
    queue(Thread(target=send, args=(bot, bot_name, send_text, 2, update.message.chat_id, welcome_text,)))  # send welcome text
    if update.message.chat_id not in ids:  # if user is not in database add it using renew function
        renew(bot, update)


# /renew - Get new public ID
def renew(bot, update):
    user_type = 0  # not implemented
    room = 0  # not implemented
    data = sql("SELECT user_type, room FROM 'users' WHERE telegram_id=" + str(update.message.chat_id), 1)  # not implemented
    remove(update.message.chat_id)  # remove old database entry if exists (renew user id)
    if len(data) > 0:
        if len(data[0]) > 0:
            user_type = data[0][0]  # not implemented
            room = data[0][1]  # not implemented
    sql("INSERT INTO 'users' ('telegram_id', 'user_type', 'room') VALUES(" + str(update.message.chat_id) + ", " + str(user_type) + ", " + str(room) + ")")  # add user to database
    queue(Thread(target=send, args=(bot, bot_name, send_text, 2, update.message.chat_id, name_text,)))  # send name_text to user


# /stats - Show some statistics
def info(bot, update):
    queue(Thread(target=send, args=(bot, bot_name, send_text, 2, update.message.chat_id, stats_text,)))  # send stats_text to user


# /rooms - Show rooms
def rooms(bot, update):
    queue(Thread(target=send, args=(bot, bot_name, send_text, 2, update.message.chat_id, room_text,)))  # not implemented (but works)


# /stop - Stop recieving messages
def stop(bot, update):
    queue(Thread(target=send, args=(bot, bot_name, send_text, 2, update.message.chat_id, exit_text,)))  # send exit_text to user
    remove(update.message.chat_id)


# any message - Send messages to other users
def message(bot, update):
    if get_name(update.message.chat_id) == 0:  # if sender not in database, add it
        renew(bot, update)
    if update.message.photo:  # if message contains something send it as something to all other users (add job to queue)
        queue(Thread(target=send, args=(bot, str(get_name(update.message.chat_id)), send_photo, 1, update.message.chat_id, update.message.caption, get_room(update.message.chat_id), update.message.photo[0].file_id,)))
    elif update.message.sticker:
        queue(Thread(target=send, args=(bot, str(get_name(update.message.chat_id)), send_sticker, 1, update.message.chat_id, "", get_room(update.message.chat_id), update.message.sticker.file_id,)))
    elif update.message.video:
        queue(Thread(target=send, args=(bot, str(get_name(update.message.chat_id)), send_video, 1, update.message.chat_id, update.message.caption, get_room(update.message.chat_id), update.message.video.file_id,)))
    elif update.message.audio:
        queue(Thread(target=send, args=(bot, str(get_name(update.message.chat_id)), send_audio, 1, update.message.chat_id, "", get_room(update.message.chat_id), update.message.audio.file_id,)))
    elif update.message.document:
        queue(Thread(target=send, args=(bot, str(get_name(update.message.chat_id)), send_document, 1, update.message.chat_id, update.message.document.file_name, get_room(update.message.chat_id), update.message.document.file_id,)))
    else:
        queue(Thread(target=send, args=(bot, str(get_name(update.message.chat_id)), send_text, 1, update.message.chat_id, update.message.text, get_room(update.message.chat_id),)))


# optimized sending
def send(bot, name, send_type, mode=0, source_id=0, text="", room=0, file=0):
    print("sent")
    # modes 0=to everyone, 1=to everyone but source_id, 2= to source_id (must exist)
    text = manipulate(text, get_name(source_id), room)  # apply filters to the message
    message_type = "message"  # was implemented for logging purposes, all messages are now just "message"
    log(name + ": (" + message_type + ")\n" + text)  # log message
    if mode != 2:  # if mode is not 2 send message to everyone or to everyone else than sender
        for target_id in sql("SELECT telegram_id FROM 'users' WHERE room=" + str(room), 1):
            print(target_id)
            if target_id[0] != source_id or mode == 0:  # send to all but the sender
                queue(Thread(target=send_type, args=(bot, target_id[0], name, file, text,)))  # add send message to queue
    else:
        send_text(bot, source_id, name, file, text)


# functions used for sending messages
# send text message
def send_text(bot, target_id, name, ignore, message):
    try:
        bot.sendMessage(chat_id=target_id, text=(bold(name) + ":\n" + message), parse_mode="HTML")
    except Exception as e:
        send_error(target_id, name, e, "t")
        pass


# send photo
def send_photo(bot, target_id, name, photo, caption):
    try:
        bot.sendPhoto(chat_id=target_id, photo=str(photo), caption=caption + " " + name)
    except Exception as e:
        send_error(target_id, name, e, "p")
        pass


# send sticker
def send_sticker(bot, target_id, name, sticker, ignore):
    try:
        bot.sendSticker(chat_id=target_id, sticker=str(sticker))
    except Exception as e:
        send_error(target_id, name, e, "s")
        pass


# send video
def send_video(bot, target_id, name, video, caption):
    try:
        bot.sendVideo(chat_id=target_id, video=str(video), caption=caption)
    except Exception as e:
        send_error(target_id, name, e, "v")
        pass


# send audio
def send_audio(bot, target_id, name, audio, ignore):
    try:
        bot.sendAudio(chat_id=target_id, audio=str(audio), performer=name)
    except Exception as e:
        send_error(target_id, name, e, "a")
        pass


# send document
def send_document(bot, target_id, name, document, filename):
    try:
        bot.sendDocument(chat_id=target_id, document=document, filename=filename)
    except Exception as e:
        send_error(target_id, name, e, "d")
        pass


# handle errors in sending, remove target if error type is Unauthorized
def send_error(target_id, name, e, t):
    log("Error: " + name + " -[" + t + "]-> " + str(get_name(target_id)) + ": " + str(e))
    if "Unauthorized" in str(e):
        remove(target_id)


# bold fuction
def bold(string):
    return "<b>" + string + "</b>"


# manipulate
def manipulate(text, name="", room_id=0):
    # replace tags with names and fix possible html characters in message
    count = sql("SELECT Count(*) FROM 'users'", 1)[0][0]
    room = sql("SELECT name FROM 'rooms' WHERE id=" + str(room_id), 1)[0][0]
    placeholders = {"&": "&amp;", "{{author}}": author, "{{name}}": name, "{{room}}": room, "{{users}}": count, "{{version}}": version, "<": "&lt;", ">": "&gt;"}
    for placeholder in placeholders:
        s1 = str(placeholder)
        s2 = str(placeholders[placeholder])
        text = text.replace(s1, s2)
    return text


# Unknown command
def unknown(bot, update):
    queue(Thread(target=send, args=(bot, bot_name, send_text, 2, update.message.chat_id, unknown_text,)))


# get name using animals script
def get_name(telegram_id):
    user_id = get_id(telegram_id)
    if user_id in custom_names:
        return custom_names[user_id].capitalize()
    return animals.get_name(user_id) + " #" + str(user_id)


# get id from database
def get_id(telegram_id):
    try:
        ids = sql("SELECT id FROM 'users' WHERE telegram_id=" + str(telegram_id), 1)
        if len(ids) > 0:
            return int(ids[0][0])
        else:
            return 0
    except Exception:
        return -1


# get room (rooms are not implemented)
def get_room(telegram_id):
    return sql("SELECT room FROM 'users' WHERE telegram_id=" + str(telegram_id), 1)[0][0]


# remove user from db
def remove(telegram_id):
    sql("DELETE FROM 'users' WHERE telegram_id=" + str(telegram_id))


if __name__ == "__main__":
    main()
