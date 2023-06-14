import telebot

import requests, os, environ

env = environ.Env()

from telebot import types

token = env("TELEGRAM_TOKEN")

URL = "http://127.0.0.1:8000/api/project/"

bot = telebot.TeleBot(token)

from datetime import datetime


start_keyboard = types.ReplyKeyboardMarkup(True)

create_btn = "Создать"
get_projects = "Список проектов"
start_keyboard.add(create_btn, get_projects)

update_keyboard = types.ReplyKeyboardMarkup(True)

title = "Название"
description = "Описание"
image = "Фото проекта"

update_keyboard.add(title, description, image)

delete_data = "Удалить"
update_data = "Изменить"

datas = {}
update_datas = {}


def create_dir():
    dir = os.path.join("media")
    if not os.path.exists(dir):
        os.mkdir(dir)


@bot.message_handler(commands=["start"])
def send_mess(message):
    bot.send_message(
        message.chat.id,
        "привет",
        reply_markup=start_keyboard,
    )


def update_project(project_id, data, message):
    response = requests.patch(f"{URL}{project_id}/", data)
    sc = response.status_code
    if sc == 404:
        bot.send_message(message.chat.id, "Проекта с таким id не существует")
    else:
        bot.send_message(message.chat.id, f"Проект с id {project_id} успешно изменен")


def update_progect_image(project_id, files, message):
    response = requests.patch(f"{URL}{project_id}/", {}, files=files)
    sc = response.status_code
    if sc == 404:
        bot.send_message(message.chat.id, "Проект с таким id не существует")
    else:
        bot.send_message(message.chat.id, f"Проект с  id {project_id} Успешно изменен")


def get_name(message):
    datas["title"] = message.text
    msg = bot.send_message(message.chat.id, "Введите описание")
    bot.register_next_step_handler(msg, get_description)


def update_name(message):
    update_datas["title"] = message.text
    update_project(update_datas.pop("id"), update_datas, message)
    update_datas.clear()
    bot.send_message(message.chat.id, "Название изменено", reply_markup=start_keyboard)


def update_description(message):
    update_datas["descriptions"] = message.text
    update_project(update_datas.pop("id"), update_datas, message)
    update_datas.clear()
    bot.send_message(message.chat.id, "Описание изменено", reply_markup=start_keyboard)


def update_image(message):
    update_datas["image"] = message.text
    update_project(update_datas.pop("id"), update_datas, message)
    update_datas.clear()
    bot.send_message(message.chat.id, "Фото изменено", reply_markup=start_keyboard)


def get_description(message):
    description = message.text
    datas["descriptions"] = description
    msg = bot.send_message(message.chat.id, "Загрузите фото проекта")
    bot.register_next_step_handler(msg, get_documents)


def get_proj():
    return requests.get(URL).json()


def del_upd_keyb(id):
    delete = types.InlineKeyboardButton("Удалить", callback_data=f"Удалить {id}")
    update = types.InlineKeyboardButton("Изменить", callback_data=f"Изменить {id}")
    del_upd_keyboard = types.InlineKeyboardMarkup()
    del_upd_keyboard.add(delete, update)
    return del_upd_keyboard


@bot.message_handler(content_types=["text"])
def get_messages(message):
    if message.text == create_btn:
        msg = bot.send_message(message.chat.id, "Введите название проекта")
        bot.register_next_step_handler(msg, get_name)
    elif message.text == get_projects:
        json_proj = get_proj()
        if json_proj == []:
            bot.send_message(message.chat.id, "В базе данных нет проектов")
        else:
            for p in json_proj:
                mesg = f"{p['title']}\n\n{p['descriptions']}\n\n{p['image']}"
                bot.send_message(
                    message.chat.id, mesg, reply_markup=del_upd_keyb(p.get("id"))
                )
    elif message.text == title:
        msg = bot.send_message(
            message.chat.id, "Введите новое название для этого проекта"
        )
        bot.register_next_step_handler(msg, update_name)
    elif message.text == description:
        msg = bot.send_message(
            message.chat.id, "Введите новое описание для этого проекта"
        )
        bot.register_next_step_handler(msg, update_description)
    elif message.text == image:
        msg = bot.send_message(message.chat.id, "Вставьте новое фото")
        bot.register_next_step_handler(msg, update_photo)

        
def get_documents(message):
    file_name = message.photo[-1].file_id
    file_id_info = bot.get_file(file_name)
    downloaded_file = bot.download_file(file_id_info.file_path)

    create_dir()

    image_path = f'./media/document_{datetime.now().strftime("%Y%m%d%H%M%S")}.jpeg'
    datas["image"] = image_path
    with open(image_path, "wb") as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, "Успешно сохранено")

    files = {"image": open(datas.pop("image"), "rb")}

    response = requests.post(URL, datas, files=files)
    print(response.status_code)
    datas.clear()
    os.remove(image_path)


def update_photo(message):
    file_name = message.photo[-1].file_id
    file_id_info = bot.get_file(file_name)
    downloaded_file = bot.download_file(file_id_info.file_path)

    create_dir()

    image_path = f'./media/document_{datetime.now().strftime("%Y%m%d%H%M%S")}.jpeg'
    update_datas["image"] = image_path
    with open(image_path, "wb") as new_file:
        new_file.write(downloaded_file)

    files = {"image": open(update_datas.pop("image"), "rb")}

    update_progect_image(update_datas.pop("id"), files, message)

    update_datas.clear()
    os.remove(image_path)
    bot.send_message(message.chat.id, "Фото изменено", reply_markup=start_keyboard)


def delete_project(project_id, message):
    response = requests.delete(f"{URL}{project_id}/")
    sc = response.status_code
    if sc == 404:
        bot.send_message(message.chat.id, "Проекта с таким id не существует")
    else:
        bot.send_message(message.chat.id, f"Проест с id {project_id} успешно удален")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if delete_data in call.data:
        ids = call.data.split(" ")[1]
        delete_project(ids, call.message)
    elif update_data in call.data:
        update_datas["id"] = call.data.split(" ")[1]
        bot.send_message(
            call.message.chat.id,
            "Какое поле вы хотите изменить?",
            reply_markup=update_keyboard,
        )


if __name__ == "__main__":
    bot.polling(none_stop=True)
