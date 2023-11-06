import aiogram, asyncio
from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
import os
import dropbox
from dropbox import Dropbox
import random
from aiogram.types.message import ContentType
import requests
import time
import json
import threading

# Инициализация бота и хранилища
bot = Bot(token="6091691945:AAFZ2-y5o1_uHbMj-TcIfBOZxV_V3hiZg34")
storage = MemoryStorage()


dp = Dispatcher(bot, storage=storage)
DROPBOX_ACCESS_TOKEN = None
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN,
            app_key='97q13wadtzrwbcz',
            app_secret='hoyjli1oftu3ag5',
            oauth2_refresh_token = 'ZaAkF2HwWbsAAAAAAAAAASJj2CWAmPvV6tN9HU8r-hm5OXzGJkzqQ2HCKU_nwotx'
                    )

client_id = "97q13wadtzrwbcz"
client_secret = "hoyjli1oftu3ag5"
refresh_token = "ZaAkF2HwWbsAAAAAAAAAASJj2CWAmPvV6tN9HU8r-hm5OXzGJkzqQ2HCKU_nwotx"

def refresh_access_token_periodically():
    while True:
        def refresh_access_token(client_id, client_secret, refresh_token):
            url = "https://api.dropbox.com/oauth2/token"
            data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret
            }
            response = requests.post(url, data=data)

            if response.status_code == 200:
                response_data = response.json()
                new_access_token = response_data.get("access_token")
                return new_access_token
            else:
                return None

        while True:
            new_access_token = refresh_access_token(client_id, client_secret, refresh_token)
            if new_access_token:
                DROPBOX_ACCESS_TOKEN = new_access_token
                print(f"Refreshed Access Token: {DROPBOX_ACCESS_TOKEN}")
            else:
                print("Failed to refresh Access Token")
            time.sleep(1800)

refresh_thread = threading.Thread(target=refresh_access_token_periodically)

# Запустите поток в фоновом режиме
refresh_thread.daemon = True
refresh_thread.start()


location_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
location_keyboard.add(types.KeyboardButton("На улице"), types.KeyboardButton("В ресторане"))

gender_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
gender_kb.add(types.KeyboardButton("Парень"), types.KeyboardButton("Девушка"),types.KeyboardButton("Сменить локацию") )

choice_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
choice_kb.add(types.KeyboardButton("Правда"), types.KeyboardButton("Действие"), types.KeyboardButton("Сменить локацию"))

kb_out_of_task = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_out_of_task.add(
    types.KeyboardButton("Продолжить"),
    types.KeyboardButton("Сменить локацию"))

kb_change_or_finish = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_change_or_finish.add(types.KeyboardButton("Сменить локацию"))

kb_demo = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_demo.add(types.KeyboardButton("Демо"), types.KeyboardButton("Полная версия"))

kb_pay = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_pay.add(types.KeyboardButton("Оплатить"))

out_of_task_g = ''
sent_images_for_user = []
list_images = []
available_images =[]

def get_list_name_as_string(list_name, value):
    # Получить имя переменной как строку
    for key, val in list_name.items():
        if val is value:
            return key
    return None
def change_list_name_gender(out_of_task_list):
    global out_of_task_g, available_images
    parts = out_of_task_g.split('_')
    location = parts[0]
    T_or_D = parts[2]
    if parts[1] == 'Men':
        gender = 'Women'
    else:
        gender = 'Men'
    new_list_name = f'{location}_{gender}_{T_or_D}'
    Reversed_list = Lists[f'{new_list_name}']
    available_images = [image for image in Reversed_list if image not in sent_images_for_user]
    return available_images
async def send_images_to_user(user_id, list_name, data = None):
    global out_of_task_g, list_images, sent_images_for_user

    sent_images_for_user = sent_images.get(user_id, set())
    available_images = [image for image in list_name if image not in sent_images_for_user]
    if available_images:
        chosen_image = random.choice(available_images)

        if 'secret' in chosen_image:

            sent_images.setdefault(user_id, [])
            sent_images[user_id].append(chosen_image)
            # Скачиваем файл из Dropbox
            metadata, response = dbx.files_download(chosen_image)
            await bot.send_photo(user_id, response.content, has_spoiler=True)

        else:

            sent_images.setdefault(user_id, [])
            sent_images[user_id].append(chosen_image)
            # Скачиваем файл из Dropbox
            metadata, response = dbx.files_download(chosen_image)
            await bot.send_photo(user_id, response.content)

        out_of_task_list_name = get_list_name_as_string(Lists, list_name)
        out_of_task_g = out_of_task_list_name
        list_images = list_name
        sent_images_for_user = sent_images.get(user_id, set())
        return list_name, out_of_task_g

class User_Choices(StatesGroup):
    Location = State()
    Gender = State()
    Task = State()
    Task_out_of_image = State()
    Demo = State()
    Pay = State()

Lists = {
            # На улице
            'Street_Men_T': ['/BLYaT_PRAZDNIKI_secret.jpg',
             '/NYuDSY_V_RESTIKE (1).jpg',
                             '/new.jpg',
                             '/ZNAChIMYE_MOMENTY_BLYaT.jpg',
                             '/рандомное место.jpg',
                             '/доставка.jpg'
            ],
            'Street_Men_D' : ['/BLYaT_VOPROS_V_PESKAKh.jpg',
               '/TANETs.jpg',
               '/гляделки.jpg',
                '/выдуманный язык.jpg',
                '/MEChTYYYYCh.jpg'
            ],

            'Street_Women_T': ['/TANETs.jpg',
               '/гляделки.jpg',
            ],
            'Street_Women_D' : ['/BLYaT_VOPROS_V_PESKAKh.jpg',
               '/TANETs.jpg',
               '/гляделки.jpg'],

          #   в рестике
            'Rest_Men_T': ['/BLYaT_PRAZDNIKI.jpg',
                             '/NYuDSY_V_RESTIKE (1).jpg',
                             ],
            'Rest_Men_D': ['/BLYaT_VOPROS_V_PESKAKh.jpg',
                             '/TANETs.jpg',
                             '/гляделки.jpg'],

            'Rest_Women_T': ['/TANETs.jpg',
                             '/гляделки.jpg',
                               ],
            'Rest_Women_D': ['/BLYaT_VOPROS_V_PESKAKh.jpg',
                               '/TANETs.jpg',
                               '/гляделки.jpg'],

          #   дома
            'Home_Men_T': ['/BLYaT_PRAZDNIKI.jpg',
                           '/NYuDSY_V_RESTIKE (1).jpg',
                           ],
            'Home_Men_D': ['/BLYaT_VOPROS_V_PESKAKh.jpg',
                           '/TANETs.jpg',
                           '/гляделки.jpg'],

            'Home_Women_T': ['/BLYaT_PRAZDNIKI.jpg',
                             '/NYuDSY_V_RESTIKE (1).jpg',
                             ],
            'Home_Women_D': ['/BLYaT_VOPROS_V_PESKAKh.jpg',
                             '/TANETs.jpg',
                             '/гляделки.jpg'],

          #   онлайн
            'Online_Men_T': ['/BLYaT_PRAZDNIKI.jpg',
                           '/NYuDSY_V_RESTIKE (1).jpg',
                           ],
            'Online_Men_D': ['/BLYaT_VOPROS_V_PESKAKh.jpg',
                           '/TANETs.jpg',
                           '/гляделки.jpg'],

            'Online_Women_T': ['/BLYaT_PRAZDNIKI.jpg',
                             '/NYuDSY_V_RESTIKE (1).jpg',
                             ],
            'Online_Women_D': ['/BLYaT_VOPROS_V_PESKAKh.jpg',
                             '/TANETs.jpg',
                             '/гляделки.jpg'],

          }

sent_images = {}

PRICE = types.LabeledPrice(label="Полная версия", amount=945*100)  # в копейках (руб)
PAYMENTS_TOKEN = '1744374395:TEST:359477acef8f4ccca2d9'
# Кнопки для выбора локации и пола
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer("Перед оплатой полной версии вы можете посмотреть демо,"
                         "что выберете?", reply_markup=kb_demo)


@dp.message_handler(lambda message: message.text == 'Демо')
async def process_demo(message: types.Message):

    await message.answer('Хорошо, вот ссылка на Демо бота\n'
                         'https://t.me/pravdaDATEdeistvie_bot')
    await message.answer('Если вам все понравилось, можем перейти к полной версии',
                         reply_markup=kb_pay)


@dp.message_handler(lambda message: message.text == 'Полная версия')
async def process_full(message: types.Message):
       await message.answer('Хорошо, тогда направляем ссылку на оплату полной версии',
                             reply_markup=kb_pay)

# @dp.message_handler(lambda message: message.text != 'Демо' or 'Полная версия')
# async def handle_other_text(message: types.Message):
#     await message.answer('Что-то не то, выбери одну из кнопок',
#                          reply_markup=kb_demo)

@dp.message_handler(lambda message:  message.text == 'Оплатить')
async def buy(message: types.Message):
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж!!!")


    await bot.send_invoice(message.chat.id,
                           title="Доступ к игре",
                           description="Получение полного доступа к игре",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message, state: FSMContext):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")


    await message.answer("Выберите локацию, в которой проходит ваше свидание", reply_markup=location_keyboard)
    await User_Choices.Location.set()




@dp.message_handler(state=User_Choices.Location)
async def process_location(message: types.Message, state: FSMContext):
    user_choice = message.text
    async with state.proxy() as data:
        data['location'] = user_choice
    if data['location'] in {'На улице', 'В ресторане', 'Дома', 'Онлайн'}:
        await message.answer('Укажите пол:', reply_markup=gender_kb)
        await User_Choices.Gender.set()
    else:
        await message.answer('Что-то не то, выбери одну из кнопок',
                             reply_markup=location_keyboard)
        await User_Choices.Location.set()

@dp.message_handler(state=User_Choices.Gender)
async def process_gender(message: types.Message, state: FSMContext):
    user_choice_g = message.text
    async with state.proxy() as data:
        data['gender'] = user_choice_g
    if data['gender'] in {'Парень', 'Девушка'}:
        await message.answer('Выбери задание:', reply_markup=choice_kb)
        await User_Choices.Task.set()
    elif data['gender'] == 'Сменить локацию':
        await message.answer('Выберите локацию',
                               reply_markup=location_keyboard)
        await User_Choices.Location.set()
    else:
        await message.answer('Что-то не то, выбери одну из кнопок',
                             reply_markup=gender_kb)
        await User_Choices.Gender.set()


@dp.message_handler(state=User_Choices.Task)
async def process_task(message: types.Message, state: FSMContext):
    user_choice_t = message.text
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['task'] = user_choice_t
        if data['task'] in {'Правда', 'Действие'}:
            pass
        elif data['task'] == 'Сменить локацию':
            await message.answer('Выберите локацию',
                                   reply_markup=location_keyboard)
            await User_Choices.Location.set()
        else:
            await message.answer('Что-то не то, выбери одну из кнопок',
                                 reply_markup=choice_kb)
            await User_Choices.Task.set()


    # В ресторане Парень Правда
    if data['location'] == 'В ресторане' and data['gender'] == 'Парень' and data['task'] == 'Правда' :

        await send_images_to_user(user_id, Lists['Rest_Men_T'], None)
        if all(image in sent_images_for_user for image in list_images):
            if 'Men' in out_of_task_g:

                await bot.send_message(user_id,'Карточки для парня закончились,' \
                              '\nхотите доиграть с оставшимися или сменить локацию?',
                                       reply_markup=kb_out_of_task)
                await User_Choices.Task_out_of_image.set()

                @dp.message_handler(state=User_Choices.Task_out_of_image)
                async def process_out_of_tasks(message: types.Message, state: FSMContext):
                    user_choice = message.text
                    async with state.proxy() as data:
                        data['task_out_of_image'] = user_choice

                    if data['task_out_of_image'] == 'Продолжить':
                        change_list_name_gender(out_of_task_g)

                        if available_images:
                            chosen_image = random.choice(available_images)

                            sent_images.setdefault(user_id, [])
                            sent_images[user_id].append(chosen_image)

                            metadata, response = dbx.files_download(chosen_image)
                            await bot.send_photo(user_id, response.content)
                            await bot.send_message(user_id, sent_images)

                            await bot.send_message(user_id, 'Что дальше?', reply_markup=kb_out_of_task)
                            await User_Choices.Task_out_of_image.set()
                        else:
                            await bot.send_message(user_id, 'Задания в этой локации кончились,'
                                                            'предалагаем сыграть в другой', reply_markup=location_keyboard)
                            await User_Choices.Location.set()

                    elif data['task_out_of_image'] == 'Сменить локацию':
                        await bot.send_message(user_id, 'Выбери локацию', reply_markup=location_keyboard)
                        await User_Choices.Location.set()
        else:
            async with state.proxy() as data:
                data['gender'] = None
                data['task'] = None
            await message.answer('Укажите пол:', reply_markup=gender_kb)
            await User_Choices.Gender.set()

    # В ресторане Парень Действие
    elif data['location'] == 'В ресторане' and data['gender'] == 'Парень' and data['task'] == 'Действие':
        await send_images_to_user(user_id, Lists['Rest_Men_D'], None)
        if all(image in sent_images_for_user for image in list_images):
            if 'Men' in out_of_task_g:

                await bot.send_message(user_id, 'Карточки для парня закончились,' \
                                                '\nхотите доиграть с оставшимися или сменить локацию?',
                                       reply_markup=kb_out_of_task)
                await User_Choices.Task_out_of_image.set()

                @dp.message_handler(state=User_Choices.Task_out_of_image)
                async def process_out_of_tasks(message: types.Message, state: FSMContext):
                    user_choice = message.text
                    async with state.proxy() as data:
                        data['task_out_of_image'] = user_choice

                    if data['task_out_of_image'] == 'Продолжить':
                        change_list_name_gender(out_of_task_g)

                        if available_images:
                            chosen_image = random.choice(available_images)

                            sent_images.setdefault(user_id, [])
                            sent_images[user_id].append(chosen_image)

                            metadata, response = dbx.files_download(chosen_image)
                            await bot.send_photo(user_id, response.content)
                            await bot.send_message(user_id, sent_images)

                            await bot.send_message(user_id, 'Что дальше?', reply_markup=kb_out_of_task)
                            await User_Choices.Task_out_of_image.set()
                        else:
                            await bot.send_message(user_id, 'Задания в этой локации кончились,'
                                                            'предалагаем сыграть в другой',
                                                   reply_markup=location_keyboard)
                            await User_Choices.Location.set()

                    elif data['task_out_of_image'] == 'Сменить локацию':
                        await bot.send_message(user_id, 'Выбери локацию', reply_markup=location_keyboard)
                        await User_Choices.Location.set()
        else:
            async with state.proxy() as data:
                data['gender'] = None
                data['task'] = None
            await message.answer('Укажите пол:', reply_markup=gender_kb)
            await User_Choices.Gender.set()


    # В ресторане Девушка
    elif data['location'] == 'В ресторане'and data['gender'] == 'Девушка' and data['task'] == 'Правда':
        await send_images_to_user(user_id, Lists['Rest_Women_T'], None)
        if all(image in sent_images_for_user for image in list_images):
            if 'Men' in out_of_task_g:

                await bot.send_message(user_id, 'Карточки для девушки закончились,' \
                                                '\nхотите доиграть с оставшимися или сменить локацию?',
                                       reply_markup=kb_out_of_task)
                await User_Choices.Task_out_of_image.set()

                @dp.message_handler(state=User_Choices.Task_out_of_image)
                async def process_out_of_tasks(message: types.Message, state: FSMContext):
                    user_choice = message.text
                    async with state.proxy() as data:
                        data['task_out_of_image'] = user_choice

                    if data['task_out_of_image'] == 'Продолжить':
                        change_list_name_gender(out_of_task_g)

                        if available_images:
                            chosen_image = random.choice(available_images)

                            sent_images.setdefault(user_id, [])
                            sent_images[user_id].append(chosen_image)

                            metadata, response = dbx.files_download(chosen_image)
                            await bot.send_photo(user_id, response.content)
                            await bot.send_message(user_id, sent_images)

                            await bot.send_message(user_id, 'Что дальше?', reply_markup=kb_out_of_task)
                            await User_Choices.Task_out_of_image.set()
                        else:
                            await bot.send_message(user_id, 'Задания в этой локации кончились,'
                                                            'предалагаем сыграть в другой',
                                                   reply_markup=location_keyboard)
                            await User_Choices.Location.set()

                    elif data['task_out_of_image'] == 'Сменить локацию':
                        await bot.send_message(user_id, 'Выбери локацию', reply_markup=location_keyboard)
                        await User_Choices.Location.set()
        else:
            async with state.proxy() as data:
                data['gender'] = None
                data['task'] = None
            await message.answer('Укажите пол:', reply_markup=gender_kb)
            await User_Choices.Gender.set()


    elif data['location'] == 'В ресторане' and data['gender'] == 'Девушка' and data['task'] == 'Действие':
        await send_images_to_user(user_id, Lists['Rest_Women_D'], None)
        if all(image in sent_images_for_user for image in list_images):
            if 'Men' in out_of_task_g:

                await bot.send_message(user_id, 'Вы просмотрели все доступные изображения для парня,' \
                                                '\nхотите доиграть с женскими вопросами или сменить локацию?',
                                       reply_markup=kb_out_of_task)
                await User_Choices.Task_out_of_image.set()

                @dp.message_handler(state=User_Choices.Task_out_of_image)
                async def process_out_of_tasks(message: types.Message, state: FSMContext):
                    user_choice = message.text
                    async with state.proxy() as data:
                        data['task_out_of_image'] = user_choice

                    if data['task_out_of_image'] == 'Продолжить':
                        change_list_name_gender(out_of_task_g)

                        if available_images:
                            chosen_image = random.choice(available_images)

                            sent_images.setdefault(user_id, [])
                            sent_images[user_id].append(chosen_image)

                            metadata, response = dbx.files_download(chosen_image)
                            await bot.send_photo(user_id, response.content)
                            await bot.send_message(user_id, sent_images)

                            await bot.send_message(user_id, 'Что дальше?', reply_markup=kb_out_of_task)
                            await User_Choices.Task_out_of_image.set()
                        else:
                            await bot.send_message(user_id, 'Задания в этой локации кончились,'
                                                            'предалагаем сыграть в другой',
                                                   reply_markup=location_keyboard)
                            await User_Choices.Location.set()

                    elif data['task_out_of_image'] == 'Сменить локацию':
                        await bot.send_message(user_id, 'Выбери локацию', reply_markup=location_keyboard)
                        await User_Choices.Location.set()
        else:
            async with state.proxy() as data:
                data['gender'] = None
                data['task'] = None
            await message.answer('Укажите пол:', reply_markup=gender_kb)
            await User_Choices.Gender.set()



    # На улице Парень
    elif data['location'] == 'На улице'and data['gender'] == 'Парень' and data['task'] == 'Правда':


        await send_images_to_user(user_id, Lists['Street_Men_T'], None)
        if all(image in sent_images_for_user for image in list_images):
            if 'Men' in out_of_task_g:

                await bot.send_message(user_id, 'Вы просмотрели все доступные изображения для парня,' \
                                                '\nхотите доиграть с женскими вопросами или сменить локацию?',
                                       reply_markup=kb_out_of_task)
                await User_Choices.Task_out_of_image.set()

                @dp.message_handler(state=User_Choices.Task_out_of_image)
                async def process_out_of_tasks(message: types.Message, state: FSMContext):
                    user_choice = message.text
                    async with state.proxy() as data:
                        data['task_out_of_image'] = user_choice

                    if data['task_out_of_image'] == 'Продолжить':
                        change_list_name_gender(out_of_task_g)

                        if available_images:
                            chosen_image = random.choice(available_images)

                            sent_images.setdefault(user_id, [])
                            sent_images[user_id].append(chosen_image)

                            metadata, response = dbx.files_download(chosen_image)
                            await bot.send_photo(user_id, response.content)
                            await bot.send_message(user_id, sent_images)

                            await bot.send_message(user_id, 'Что дальше?', reply_markup=kb_out_of_task)
                            await User_Choices.Task_out_of_image.set()
                        else:
                            await bot.send_message(user_id, 'Задания в этой локации кончились,'
                                                            'предалагаем сыграть в другой',
                                                   reply_markup=location_keyboard)
                            await User_Choices.Location.set()

                    elif data['task_out_of_image'] == 'Сменить локацию':
                        await bot.send_message(user_id, 'Выбери локацию', reply_markup=location_keyboard)
                        await User_Choices.Location.set()
        else:
            async with state.proxy() as data:
                data['gender'] = None
                data['task'] = None
            await message.answer('Укажите пол:', reply_markup=gender_kb)
            await User_Choices.Gender.set()


    elif data['location'] == 'На улице' and data['gender'] == 'Парень' and data['task'] == 'Действие':
        await send_images_to_user(user_id, Lists['Street_Men_D'], None)
        if all(image in sent_images_for_user for image in list_images):
            if 'Men' in out_of_task_g:

                await bot.send_message(user_id, 'Вы просмотрели все доступные изображения для парня,' \
                                                '\nхотите доиграть с женскими вопросами или сменить локацию?',
                                       reply_markup=kb_out_of_task)
                await User_Choices.Task_out_of_image.set()

                @dp.message_handler(state=User_Choices.Task_out_of_image)
                async def process_out_of_tasks(message: types.Message, state: FSMContext):
                    user_choice = message.text
                    async with state.proxy() as data:
                        data['task_out_of_image'] = user_choice

                    if data['task_out_of_image'] == 'Продолжить':
                        change_list_name_gender(out_of_task_g)

                        if available_images:
                            chosen_image = random.choice(available_images)

                            sent_images.setdefault(user_id, [])
                            sent_images[user_id].append(chosen_image)

                            metadata, response = dbx.files_download(chosen_image)
                            await bot.send_photo(user_id, response.content)
                            await bot.send_message(user_id, sent_images)

                            await bot.send_message(user_id, 'Что дальше?', reply_markup=kb_out_of_task)
                            await User_Choices.Task_out_of_image.set()
                        else:
                            await bot.send_message(user_id, 'Задания в этой локации кончились,'
                                                            'предалагаем сыграть в другой',
                                                   reply_markup=location_keyboard)
                            await User_Choices.Location.set()

                    elif data['task_out_of_image'] == 'Сменить локацию':
                        await bot.send_message(user_id, 'Выбери локацию', reply_markup=location_keyboard)
                        await User_Choices.Location.set()
        else:
            async with state.proxy() as data:
                data['gender'] = None
                data['task'] = None
            await message.answer('Укажите пол:', reply_markup=gender_kb)
            await User_Choices.Gender.set()


    # На улице Девушка
    elif data['location'] == 'На улице' and data['gender'] == 'Девушка' and data['task'] == 'Правда':
        await send_images_to_user(user_id, Lists['Street_Women_T'], None)
        if all(image in sent_images_for_user for image in list_images):
            if 'Men' in out_of_task_g:

                await bot.send_message(user_id, 'Вы просмотрели все доступные изображения для парня,' \
                                                '\nхотите доиграть с женскими вопросами или сменить локацию?',
                                       reply_markup=kb_out_of_task)
                await User_Choices.Task_out_of_image.set()

                @dp.message_handler(state=User_Choices.Task_out_of_image)
                async def process_out_of_tasks(message: types.Message, state: FSMContext):
                    user_choice = message.text
                    async with state.proxy() as data:
                        data['task_out_of_image'] = user_choice

                    if data['task_out_of_image'] == 'Продолжить':
                        change_list_name_gender(out_of_task_g)

                        if available_images:
                            chosen_image = random.choice(available_images)

                            sent_images.setdefault(user_id, [])
                            sent_images[user_id].append(chosen_image)

                            metadata, response = dbx.files_download(chosen_image)
                            await bot.send_photo(user_id, response.content)
                            await bot.send_message(user_id, sent_images)

                            await bot.send_message(user_id, 'Что дальше?', reply_markup=kb_out_of_task)
                            await User_Choices.Task_out_of_image.set()
                        else:
                            await bot.send_message(user_id, 'Задания в этой локации кончились,'
                                                            'предалагаем сыграть в другой',
                                                   reply_markup=location_keyboard)
                            await User_Choices.Location.set()

                    elif data['task_out_of_image'] == 'Сменить локацию':
                        await bot.send_message(user_id, 'Выбери локацию', reply_markup=location_keyboard)
                        await User_Choices.Location.set()
        else:
            async with state.proxy() as data:
                data['gender'] = None
                data['task'] = None
            await message.answer('Укажите пол:', reply_markup=gender_kb)
            await User_Choices.Gender.set()


    elif data['location'] == 'На улице' and data['gender'] == 'Девушка' and data['task'] == 'Действие':
        await message.answer('улица девушка правда')
    # Дома Парень
    elif data['location'] == 'Дома' and data['gender'] == 'Парень' and data['task'] == 'Правда':
        await message.answer('улица парень правда')
    elif data['location'] == 'Дома' and data['gender'] == 'Парень' and data['task'] == 'Действие':
        await message.answer('улица парень правда')
    # Дома Девушка
    elif data['location'] == 'Дома' and data['gender'] == 'Девушка' and data['task'] == 'Правда':
        await message.answer('улица девушка правда')
    elif data['location'] == 'Дома' and data['gender'] == 'Девушка' and data['task'] == 'Действие':
        await message.answer('улица девушка правда')
        # Онлайн Парень
    elif data['location'] == 'Онлайн' and data['gender'] == 'Парень' and data['task'] == 'Правда':
        await message.answer('улица парень правда')
    elif data['location'] == 'Онлайн' and data['gender'] == 'Парень' and data['task'] == 'Действие':
        await message.answer('улица парень правда')
    # Онлайн Девушка
    elif data['location'] == 'Онлайн' and data['gender'] == 'Девушка' and data['task'] == 'Правда':
        await message.answer('улица девушка правда')
    elif data['location'] == 'Онлайн' and data['gender'] == 'Девушка' and data['task'] == 'Действие':
        await message.answer('улица девушка правда')
    elif data['gender'] or data['task'] == 'Сменить локацию':
        pass
    else:
        await message.answer('Что-то не то, выбери одну из кнопок',
                             reply_markup=choice_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
