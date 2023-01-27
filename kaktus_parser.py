import csv
import json
import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag



import telebot
from telebot import types


URL = 'https://kaktus.media/'


def get_link_to_all_news(url: str):
    html_of_main_page = requests.get(url=url).text
    soup = BeautifulSoup(html_of_main_page, 'lxml')
    html_link = soup.find('a', class_='Main--all_news-link').get('href')
    return html_link


def get_html(html_link: str):
    html = requests.get(url= html_link)
    return html.text


def get_news_from_html(html: str) -> ResultSet:
    soup = BeautifulSoup(html, 'lxml')
    news_total = soup.find_all('div', class_='Tag--article')
    return news_total

def parse_news(news_total: ResultSet):
    result = []
    for news in news_total:
        title = news.find('div', class_='ArticleItem--data ArticleItem--data--withImage').find('a', class_='ArticleItem--name').text.strip()
        description = news.find('Tag--articles', class_='articleItem')
        image_link = news.find('a', class_= 'ArticleItem--image').find('img').get('src')
        news_link = news.find('a', class_='ArticleItem--name').get('href')

        def description_of_one_news(news_link):
            one_news_page = get_html(news_link)
            soup_of_one = BeautifulSoup(one_news_page, 'lxml')
            descript = soup_of_one.find('div', class_= 'BbCode').find('p').text
            return descript
        description = description_of_one_news(news_link)
          
                      
        
        obj = {
            'title': title,
            'description': description,
            'image_link': image_link,
            'news_link': news_link
        }
        result.append(obj)
    return result



# def write_to_json(result: list) -> str:
#     with open('get_news_from_html.json', 'w') as file1:
#         res = json.dump(result, file1, ensure_ascii=False, indent=4)




def main():
    html_link = get_link_to_all_news(URL)
    html = get_html(html_link)
    all_news = get_news_from_html(html)
    result = parse_news(all_news)
    # write_to_json(result)
    return result



if __name__ == '__main__':
    data = main()


token = '5725887388:AAHg80VMbSnbIQFkuClCYI4xv8bPzHWV_7U' #telegram_bot

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def hello_func(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Получить Новости от КактусМедиа')
    keyboard.add(button)
    news_number = 0
    call_back_nums = 1
    for news in data:
        if news_number < 15:
            description = news['description']
            image = news['image_link']
            inline_keyboard = types.InlineKeyboardMarkup()
            inline_button1 = types.InlineKeyboardButton('Подробнее', url=news['news_link'])
            inline_keyboard.add(inline_button1)
            # bot.send_message(message.chat.id,  news['title'], reply_markup=inline_keyboard)
            bot.send_message(message.chat.id, f'<b>{news["title"]}</b>\n\n{description}\n{image}', reply_markup=inline_keyboard, parse_mode='html')
            news_number += 1
            call_back_nums += 1
            print(news_number, 'для Выхода напишите "Выйти"')



inline_keyboard = types.InlineKeyboardMarkup()
inline_button = types.InlineKeyboardButton('Пока', callback_data='mydata')
inline_keyboard.add(inline_button)

@bot.message_handler()
def get_inline_keyboard(message: types.Message):
    bot.send_message(message.chat.id, 'Нажми на кнопку, чтобы попрощаться', reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data == 'mydata')
def goodbye(callback: types.CallbackQuery):
    bot.send_message(callback.message.chat.id, 'До свидания!')
    bot.send_sticker(callback.message.chat.id, 'CAACAgIAAxkBAAEHbvFj0TXihpx2j-f6oXmYMsKECO6B7wACER0AAiToYUmShecu8SgERS0E')




            






bot.polling()
  


# bot.polling() # запуск бота


