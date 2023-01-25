import openai # не забудьте установить эту библиотеку
import telebot
import time

openai.api_key = "TOKEN OPENAI"
bot = telebot.TeleBot('TOKEN TELEGRAM')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я бот gptChat! Задай мне любой вопрос, и я отвечу.')


@bot.message_handler(content_types=['text'])
def handle_message(message):
    message.text = message.text.lower()
    if 'фото:' in message.text:
        try:
            response = openai.Image.create(
                prompt=f"{message.text}",
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']
            bot.send_photo(message.chat.id, photo=image_url)
        except:
            bot.send_message(message.chat.id,'Такого придумать даже я не могу. Попробуйте изменить запрос (некоторые темы типа экстремизма, насилия и т.д. под запретом')

    else:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message.text,
            max_tokens=1024,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        bot.send_message(message.chat.id, text='Ваш вопрос: \n' + f'{message.text}\n\n' + 'Ответ: \n' + response['choices'][0].text)

while True:
    try:
      bot.polling(none_stop=True)
    except Exception as e:
      time.sleep(10)
