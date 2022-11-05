# -*- coding: cp1251 -*-
import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

open_weather_token='6962f94e1af5f280519138c8f94623a9'
tg_bot_token='5447587625:AAGDRTk_TtwihLhepN5qpzz-EjnhxzQXkUk'
bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("������! ������ ��� �������� ������ � � ������ ������ ������!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "���� \U00002600",
        "Clouds": "������� \U00002601",
        "Rain": "����� \U00002614",
        "Drizzle": "����� \U00002614",
        "Thunderstorm": "����� \U000026A1",
        "Snow": "���� \U0001F328",
        "Mist": "����� \U0001F32B"
    }

    try:
        g= requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={message.text}&appid={open_weather_token}")
        dg=g.json()
        lat=dg[0]["lat"]
        lon=dg[0]["lon"]
        name = dg[0]["local_names"]["en"]
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={open_weather_token}"
        )
        data = r.json()

        city = name
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "�������� � ����, �� ����� ��� ��� �� ������!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"������ � ������: {city}\n�����������: {cur_weather}C� {wd}\n"
              f"���������: {humidity}%\n��������: {pressure} ��.��.��\n�����: {wind} �/�\n"
              f"������ ������: {sunrise_timestamp}\n����� ������: {sunset_timestamp}\n����������������� ���: {length_of_the_day}\n"
              f"^_^Have a nice day bro!6_6"
              )

    except:
        await message.reply("\U00002620 ��������� �������� ������ \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)
