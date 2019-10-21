from bs4 import BeautifulSoup
import urllib3
import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def write_msg(user_id, message):
    r = random.randint(0, 999999999999)
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': r})

# API-ключ созданный ранее
token = ""

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
    
        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
        
            # Сообщение от пользователя
            request = event.text
            
            # Каменная логика ответа
            if request == "гороскоп":
                
                def pars(url):
                    http = urllib3.PoolManager()
                    response = http.request('GET', url)
                    soup = BeautifulSoup(response.data)

                    res = soup('p')[2].string[4:]
                    return res

                urls = ['http://astroscope.ru/horoskop/ejednevniy_goroskop/aquarius.html',
                        'http://astroscope.ru/horoskop/ejednevniy_goroskop/aries.html',
                        'http://astroscope.ru/horoskop/ejednevniy_goroskop/capricorn.html',
                        'http://astroscope.ru/horoskop/ejednevniy_goroskop/taurus.html',
                        'http://astroscope.ru/horoskop/ejednevniy_goroskop/virgo.html',
                        'http://astroscope.ru/horoskop/ejednevniy_goroskop/gemini.html',
                        'http://astroscope.ru/horoskop/ejednevniy_goroskop/leo.html',
                        'http://astroscope.ru/horoskop/ejednevniy_goroskop/sagittarius.html']

                names = ['Водолей',
                'Овен',
                'Козерог',
                'Телец',
                'Дева',
                'Близнецы',
                'Лев',
                'Стрелец']

                res = ''
                for u in range(len(urls)):
                    res += (names[u]+': \n')
                    res += (pars(urls[u])+'\n')

                    write_msg(event.user_id, res)
                    res = ''
                write_msg(event.user_id, '-----------------------------------------------------------------------------------------------------------')
                write_msg(event.user_id, 'Удачного тебе дня =)')
            else:
                write_msg(event.user_id, 'не понял')
