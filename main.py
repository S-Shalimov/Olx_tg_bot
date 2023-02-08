from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import executor
import os
from typing import Final
from dotenv import load_dotenv
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from urls import *
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from olx_parser import main_get_advertisements
import asyncio


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class TgKeys:
    TOKEN: Final = os.environ.get('TOKEN')

bot = Bot(token=TgKeys.TOKEN)
dp = Dispatcher(bot)



def new_url():
    global search_url
    global search_params
    search_url = [URL_MAIN, 'd/']
    search_params = dict()

@dp.message_handler(commands=['main'], commands_prefix='@')
async def send_welcome(message: types.Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Начать поиск', callback_data='categories'))
    markup.add(InlineKeyboardButton('Отмена', callback_data='cancel'))
    await bot.send_message(chat_id=message.chat.id, text='Бот агрегирует OLX-объявления.\n', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'city')
async def select_area(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Ташкент', callback_data=('Ташкент')))
    markup.add(InlineKeyboardButton('Самарканд', callback_data=('Самарканд')))
    markup.add(InlineKeyboardButton('Андижанская область', callback_data=('Андижанская область')))
    markup.add(InlineKeyboardButton('Бухарская область', callback_data=('Бухарская область')))
    markup.add(InlineKeyboardButton('Джизакская область', callback_data=('Джизакская область')))
    markup.add(InlineKeyboardButton('Каракалпакстан', callback_data=('Каракалпакстан')))
    markup.add(InlineKeyboardButton('Кашкадарьинская область', callback_data=('Кашкадарьинская область')))
    markup.add(InlineKeyboardButton('Навоийская область', callback_data=('Навоийская область')))
    markup.add(InlineKeyboardButton('Наманганская область', callback_data=('Наманганская область')))
    markup.add(InlineKeyboardButton('Самаркандская область', callback_data=('Самаркандская область')))
    markup.add(InlineKeyboardButton('Сурхандарьинская область', callback_data=('Сурхандарьинская область')))
    markup.add(InlineKeyboardButton('Сырдарьинская область', callback_data=('Сырдарьинская область')))
    markup.add(InlineKeyboardButton('Ташкентская область', callback_data=('Ташкентская область')))
    markup.add(InlineKeyboardButton('Ферганская область', callback_data=('Ферганская область')))
    markup.add(InlineKeyboardButton('Хорезмская область', callback_data=('Хорезмская область')))
    markup.add(InlineKeyboardButton('Весь Узбекистан', callback_data=('get_params')))
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='В каком регионе будем искать объявления?', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data in ['Ташкент', 'Самарканд', 'Андижанская область', 'Бухарская область',
                           'Джизакская область', 'Каракалпакстан', 'Кашкадарьинская область', 'Навоийская область',
                           'Наманганская область', 'Самаркандская область', 'Сурхандарьинская область', 'Ташкентская область',
                           'Ферганская область', 'Хорезмская область', 'Сырдарьинская область'])
async def select_city_or_not(callback_query: types.CallbackQuery):
    if callback_query.data == 'Ташкент':
        search_url.append(AREAS['Ташкентская область']['Ташкент'])
        await get_params(callback_query)
    if callback_query.data == 'Самарканд':
        search_url.append(AREAS['Самаркандская область']['Самарканд'])
        await get_params(callback_query)
    search_params['Город/Область'] = callback_query.data
    search_url.append(search_params['Город/Область'])
    await get_params(callback_query)
    await bot.answer_callback_query(callback_query.id, show_alert=False)

@dp.callback_query_handler(lambda c: c.data == 'categories')
async def big_categories(callback_query: types.CallbackQuery):
    new_url()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Детский мир', callback_data='childrens_world'))
    markup.add(InlineKeyboardButton('Недвижимость', callback_data='real_estate'))
    markup.add(InlineKeyboardButton('Транспорт', callback_data='transport'))
    markup.add(InlineKeyboardButton('Работа', callback_data='job'))
    markup.add(InlineKeyboardButton('Животные', callback_data='animals'))
    markup.add(InlineKeyboardButton('Дом и сад', callback_data='home_garden'))
    markup.add(InlineKeyboardButton('Электроника', callback_data='electronics'))
    markup.add(InlineKeyboardButton('Бизнес и услуги', callback_data='business'))
    markup.add(InlineKeyboardButton('Мода и стиль', callback_data='fashion'))
    markup.add(InlineKeyboardButton('Хобби, спорт и отдых', callback_data='sport'))
    markup.add(InlineKeyboardButton('Отдам даром', callback_data='free'))
    markup.add(InlineKeyboardButton('Обмен', callback_data='exchange'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите категорию', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'childrens_world')
async def childrens_world(callback_query: types.CallbackQuery):
    search_url.append('detskiy-mir/')
    search_params['Категория'] = 'Детский мир'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Детская одежда', callback_data='detskaya-odezhda'))
    markup.add(InlineKeyboardButton('Детская обувь', callback_data='detskaya-obuv'))
    markup.add(InlineKeyboardButton('Детские коляски', callback_data='detskie-kolyaski'))
    markup.add(InlineKeyboardButton('Детские автокресла', callback_data='detskie-avtokresla'))
    markup.add(InlineKeyboardButton('Детская мебель', callback_data='detskaya-mebel'))
    markup.add(InlineKeyboardButton('Игрушки', callback_data='igrushki'))
    markup.add(InlineKeyboardButton('Детский транспорт', callback_data='detskiy-transport'))
    markup.add(InlineKeyboardButton('Кормление', callback_data='kormlenie'))
    markup.add(InlineKeyboardButton('Товары для школьников', callback_data='tovary-dlya-shkolnikov'))
    markup.add(InlineKeyboardButton('Прочие детские товары', callback_data='prochie-detskie-tovary'))
    markup.add(InlineKeyboardButton('Весь детский мир', callback_data='detskiy-mir'))
    markup.add(InlineKeyboardButton('Отдам даром', callback_data='free'))
    markup.add(InlineKeyboardButton('Обмен', callback_data='exchange'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите подкатегорию', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'real_estate')
async def real_estate(callback_query: types.CallbackQuery):
    search_url.append('nedvizhimost/')
    search_params['Категория'] = 'Недвижимость'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Посуточная аренда', callback_data='posutochno_pochasovo'))
    markup.add(InlineKeyboardButton('Квартиры', callback_data='kvartiry'))
    markup.add(InlineKeyboardButton('Дома', callback_data='doma'))
    markup.add(InlineKeyboardButton('Земля', callback_data='zemlja'))
    markup.add(InlineKeyboardButton('Гаражи / стоянки', callback_data='garazhi'))
    markup.add(InlineKeyboardButton('Коммерческие помещения', callback_data='kommercheskie'))
    markup.add(InlineKeyboardButton('Вся недвижимость', callback_data='all_real_estate'))
    markup.add(InlineKeyboardButton('Отдам даром', callback_data='free'))
    markup.add(InlineKeyboardButton('Обмен', callback_data='exchange'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите подкатегорию', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'transport')
async def transport(callback_query: types.CallbackQuery):
    search_params['Категория'] = 'Транспорт'
    search_url.append('transport/')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Мото', callback_data='moto'))
    markup.add(InlineKeyboardButton('Мотозапчасти и аксессуары', callback_data='motozapchasti'))
    markup.add(InlineKeyboardButton('Другой транспорт', callback_data='drugoytransport'))
    markup.add(InlineKeyboardButton('Автобусы', callback_data='avtobusy'))
    markup.add(InlineKeyboardButton('Грузовые автомобили', callback_data='gruzovyeavtomobili'))
    markup.add(InlineKeyboardButton('Прицепы', callback_data='pritsepy'))
    markup.add(InlineKeyboardButton('Спецтехника', callback_data='spetstehnika'))
    markup.add(InlineKeyboardButton('Сельхозтехника', callback_data='selhoztehnika'))
    markup.add(InlineKeyboardButton('Запчасти для спец / с.х. техники', callback_data='zapchastidlyaspetshtehniki'))
    markup.add(InlineKeyboardButton('Водный транспорт', callback_data='vodnyytransport'))
    markup.add(InlineKeyboardButton('Прочие запчасти', callback_data='prochiezapchasti'))
    markup.add(InlineKeyboardButton('Весь транспорт', callback_data='all_transport'))
    markup.add(InlineKeyboardButton('Отдам даром', callback_data='free'))
    markup.add(InlineKeyboardButton('Обмен', callback_data='exchange'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите подкатегорию', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'job')
async def job(callback_query: types.CallbackQuery):
    search_url.append('rabota/')
    search_params['Категория'] = 'Работа'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Розничная торговля / Продажи', callback_data='roznichnayatorgovlyaprodazhi'))
    markup.add(InlineKeyboardButton('Транспорт / логистика', callback_data='transportlogistika'))
    markup.add(InlineKeyboardButton('Строительство', callback_data='stroitelstvo'))
    markup.add(InlineKeyboardButton('Бары / рестораны', callback_data='baryrestoranyrazvlecheniya'))
    markup.add(InlineKeyboardButton('Юриспруденция и бухгалтерия', callback_data='yurisprudentsiyabuhgalteriya'))
    markup.add(InlineKeyboardButton('Охрана / безопасность', callback_data='ohranabezopasnost'))
    markup.add(InlineKeyboardButton('Домашний персонал', callback_data='domashniypersonal'))
    markup.add(InlineKeyboardButton('Красота / фитнес / спорт', callback_data='krasota_fitnes_sport'))
    markup.add(InlineKeyboardButton('Туризм / отдых / развлечения', callback_data='turizm_otdyh_razvlecheniya'))
    markup.add(InlineKeyboardButton('Образование', callback_data='obrazovanie'))
    markup.add(InlineKeyboardButton('Культура / искусство', callback_data='kultura_iskusstvo'))
    markup.add(InlineKeyboardButton('Медицина / фармация', callback_data='meditsina_farmatsiya'))
    markup.add(InlineKeyboardButton('ИТ / телеком / компьютеры', callback_data='it_telekom_kompyutery'))
    markup.add(InlineKeyboardButton('Недвижимость', callback_data='nedvizhimost'))
    markup.add(InlineKeyboardButton('Маркетинг / реклама / дизайн', callback_data='marketing_reklama_dizayn'))
    markup.add(InlineKeyboardButton('Производство / энергетика', callback_data='proizvodstvo_energetika'))
    markup.add(InlineKeyboardButton('Cекретариат / АХО', callback_data='cekretariat_aho'))
    markup.add(InlineKeyboardButton('Начало карьеры / Студенты', callback_data='nachalo_karery_studenty'))
    markup.add(InlineKeyboardButton('Сервис и быт', callback_data='servis_i_byt'))
    markup.add(InlineKeyboardButton('Другие сферы занятий', callback_data='drugie_sfery_zanyatiy'))
    markup.add(InlineKeyboardButton('Частичная занятость', callback_data='chastichnaya_zanyatost'))
    markup.add(InlineKeyboardButton('Вся работа', callback_data='all_jobs'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите подкатегорию', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'animals')
async def animals(callback_query: types.CallbackQuery):
    search_url.append('zhivotnye/')
    search_params['Категория'] = 'Животные'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Собаки', callback_data='sobaki'))
    markup.add(InlineKeyboardButton('Кошки', callback_data='koshki'))
    markup.add(InlineKeyboardButton('Аквариумистика', callback_data='akvariumnye-rybki'))
    markup.add(InlineKeyboardButton('Птицы', callback_data='ptitsy'))
    markup.add(InlineKeyboardButton('Грызуны', callback_data='gryzuny'))
    markup.add(InlineKeyboardButton('Сельхоз животные', callback_data='selskohozyaystvennye-zhivotnye'))
    markup.add(InlineKeyboardButton('Зоотовары', callback_data='tovary-dlya-zhivotnyh'))
    markup.add(InlineKeyboardButton('Вязка', callback_data='vyazka'))
    markup.add(InlineKeyboardButton('Бюро находок', callback_data='byuro-nahodok'))
    markup.add(InlineKeyboardButton('Другие животные', callback_data='drugie-zhivotnye'))
    markup.add(InlineKeyboardButton('Животные даром', callback_data='zhivotnye-darom'))
    markup.add(InlineKeyboardButton('Все животные и зоотовары', callback_data='all_animals'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите подкатегорию', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'home_garden')
async def home_garden(callback_query: types.CallbackQuery):
    search_url.append('dom-i-sad/')
    search_params['Категория'] = 'Дом и сад'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Мебель', callback_data='mebel'))
    markup.add(InlineKeyboardButton('Сад / огород', callback_data='sad-ogorod'))
    markup.add(InlineKeyboardButton('Предметы интерьера', callback_data='predmety-interera'))
    markup.add(InlineKeyboardButton('Товары для строительства/ремонта', callback_data='tovari-dlya-stroitelstva-remonta'))
    markup.add(InlineKeyboardButton('Инструменты', callback_data='instrumenty'))
    markup.add(InlineKeyboardButton('Комнатные растения', callback_data='komnatnye-rasteniya'))
    markup.add(InlineKeyboardButton('Посуда / кухонная утварь', callback_data='posuda-kuhonnaya-utvar'))
    markup.add(InlineKeyboardButton('Садовый инвентарь', callback_data='sadovyy-inventar'))
    markup.add(InlineKeyboardButton('Хозяйственный инвентарь / бытовая химия', callback_data='hozyaystvennyy-inventar'))
    markup.add(InlineKeyboardButton('Дом и сад', callback_data='all_home_garden'))
    markup.add(InlineKeyboardButton('Отдам даром', callback_data='free'))
    markup.add(InlineKeyboardButton('Обмен', callback_data='exchange'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите подкатегорию', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'electronics')
async def electronics(callback_query: types.CallbackQuery):
    search_url.append('elektronika/')
    search_params['Категория'] = 'Электроника'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Канцтовары / расходные материалы', callback_data='kantstovary'))
    markup.add(InlineKeyboardButton('Продукты питания / Напитки', callback_data='produkty_pitaniya'))
    markup.add(InlineKeyboardButton('Прочие товары для дома', callback_data='prochie_tovary_dlya_doma'))
    markup.add(InlineKeyboardButton('Телефоны', callback_data='telefony'))
    markup.add(InlineKeyboardButton('Компьютеры', callback_data='kompyutery'))
    markup.add(InlineKeyboardButton('Фото / видео', callback_data='foto_video'))
    markup.add(InlineKeyboardButton('Тв / видеотехника', callback_data='tv_videotehnika'))
    markup.add(InlineKeyboardButton('Аудиотехника', callback_data='audiotehnika'))
    markup.add(InlineKeyboardButton('Игры и игровые приставки', callback_data='igry_i_igrovye_pristavki'))
    markup.add(InlineKeyboardButton('Техника для дома', callback_data='tehnika_dlya_doma'))
    markup.add(InlineKeyboardButton('Техника для кухни', callback_data='tehnika_dlya_kuhni'))
    markup.add(InlineKeyboardButton('Климатическое оборудование', callback_data='klimaticheskoe_oborudovanie'))
    markup.add(InlineKeyboardButton('Индивидуальный уход', callback_data='individualnyy_uhod'))
    markup.add(InlineKeyboardButton('Аксессуары и комплектующие', callback_data='aksessuary_i_komplektuyuschie'))
    markup.add(InlineKeyboardButton('Прочая электроника', callback_data='prochaja_electronika'))
    markup.add(InlineKeyboardButton('Вся электроника', callback_data='all_electronics'))
    markup.add(InlineKeyboardButton('Отдам даром', callback_data='free'))
    markup.add(InlineKeyboardButton('Обмен', callback_data='exchange'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите подкатегорию', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'business')
async def business(callback_query: types.CallbackQuery):
    search_url.append('uslugi/')
    search_params['Категория'] = 'Бизнес и услуги'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Строительство / ремонт / уборка', callback_data='stroitelstvo_remont'))
    markup.add(InlineKeyboardButton('Финансовые услуги / партнерство', callback_data='finansovye_uslugi'))
    markup.add(InlineKeyboardButton('Перевозки / аренда транспорта', callback_data='perevozki_arenda'))
    markup.add(InlineKeyboardButton('Реклама / полиграфия / маркетинг / интернет', callback_data='reklama_marketing'))
    markup.add(InlineKeyboardButton('Няни / сиделки', callback_data='nyani_sidelki'))
    markup.add(InlineKeyboardButton('Сырьё / материалы', callback_data='syre_materialy'))
    markup.add(InlineKeyboardButton('Красота / здоровье', callback_data='krasota_zdorove'))
    markup.add(InlineKeyboardButton('Оборудование', callback_data='oborudovanie'))
    markup.add(InlineKeyboardButton('Образование / Спорт', callback_data='obrazovanie'))
    markup.add(InlineKeyboardButton('Услуги для животных', callback_data='uslugi_zhivotnyh'))
    markup.add(InlineKeyboardButton('Продажа бизнеса', callback_data='prodazha_biznesa'))
    markup.add(InlineKeyboardButton('Развлечения / Искусство / Фото / Видео', callback_data='razvlechenie_foto_video'))
    markup.add(InlineKeyboardButton('Туризм', callback_data='turizm'))
    markup.add(InlineKeyboardButton('Услуги переводчиков / набор текста', callback_data='perevodchiki_nabor_teksta'))
    markup.add(InlineKeyboardButton('Авто / мото услуги', callback_data='avtomoto'))
    markup.add(InlineKeyboardButton('Обслуживание, ремонт техники', callback_data='obsluzhivanie'))
    markup.add(InlineKeyboardButton('Юридические услуги', callback_data='yuridicheskie'))
    markup.add(InlineKeyboardButton('Прокат товаров', callback_data='prokat'))
    markup.add(InlineKeyboardButton('Прочие услуги', callback_data='prochie'))
    markup.add(InlineKeyboardButton('Бизнес и услуги', callback_data='all_business'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите подкатегорию', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'fashion')
async def fashion(callback_query: types.CallbackQuery):
    search_url.append('moda-i-stil/')
    search_params['Категория'] = 'Мода и стиль'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Одежда/обувь', callback_data='odezhda'))
    markup.add(InlineKeyboardButton('Для свадьбы', callback_data='svadby'))
    markup.add(InlineKeyboardButton('Мода разное', callback_data='modaraznoe'))
    markup.add(InlineKeyboardButton('Наручные часы', callback_data='naruchnye'))
    markup.add(InlineKeyboardButton('Аксессуары', callback_data='aksessuary'))
    markup.add(InlineKeyboardButton('Подарки', callback_data='podarki'))
    markup.add(InlineKeyboardButton('Мода и стиль', callback_data='all_fashion'))
    markup.add(InlineKeyboardButton('Отдам даром', callback_data='free'))
    markup.add(InlineKeyboardButton('Обмен', callback_data='exchange'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите подкатегорию', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'sport')
async def sport(callback_query: types.CallbackQuery):
    search_url.append('hobbi-otdyh-i-sport/')
    search_params['Категория'] = 'Хобби, спорт и отдых'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Антиквариат / коллекции', callback_data='antikvariat'))
    markup.add(InlineKeyboardButton('Музыкальные инструменты', callback_data='muzykalnye'))
    markup.add(InlineKeyboardButton('Другое', callback_data='drugoe'))
    markup.add(InlineKeyboardButton('Спорт / отдых', callback_data='sportotdyh'))
    markup.add(InlineKeyboardButton('Книги / журналы', callback_data='knigi'))
    markup.add(InlineKeyboardButton('CD / DVD / пластинки / кассеты', callback_data='cddvd'))
    markup.add(InlineKeyboardButton('Билеты', callback_data='bilety'))
    markup.add(InlineKeyboardButton('Хобби, спорт и отдых', callback_data='all_sport'))
    markup.add(InlineKeyboardButton('Отдам даром', callback_data='free'))
    markup.add(InlineKeyboardButton('Обмен', callback_data='exchange'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите подкатегорию', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'detskaya-odezhda')
async def detskaya_odezhda(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Детская одежда'])
    search_params['Подкатегория'] = 'Детская одежда'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Детская одежда', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'detskaya-obuv')
async def detskaya_obuv(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Детская обувь'])
    search_params['Подкатегория'] = 'Детская обувь'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Детская обувь', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'detskie-kolyaski')
async def detskie_kolyaski(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Детские коляски'])
    search_params['Подкатегория'] = 'Детские коляски'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Детские коляски', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'detskie-avtokresla')
async def detskie_avtokresla(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Детские автокресла'])
    search_params['Подкатегория'] = 'Детские автокресла'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Детские автокресла', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'detskaya-mebel')
async def detskaya_mebel(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Детская мебель'])
    search_params['Подкатегория'] = 'Детская мебель'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Детская мебель', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'igrushki')
async def igrushki(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Игрушки'])
    search_params['Подкатегория'] = 'Игрушки'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Игрушки', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'detskiy-transport')
async def detskiy_transport(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Детский транспорт'])
    search_params['Подкатегория'] = 'Детский транспорт'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Детский транспорт', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'kormlenie')
async def kormlenie(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Кормление'])
    search_params['Подкатегория'] = 'Кормление'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Кормление', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'tovary-dlya-shkolnikov')
async def tovary_dlya_shkolnikov(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Товары для школьников'])
    search_params['Подкатегория'] = 'Товары для школьников'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Товары для школьников', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'prochie-detskie-tovary')
async def prochie_detskie_tovary(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Прочие детские товары'])
    search_params['Подкатегория'] = 'Прочие детские товары'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Прочие детские товары', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'detskiy-mir')
async def detskiy_mir(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Детский мир', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'posutochno_pochasovo')
async def prochie_detskie_tovary(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Посуточная аренда'])
    search_params['Подкатегория'] = 'Посуточная аренда'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Посуточная аренда', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'kvartiry')
async def kvartiry(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Квартиры'])
    search_params['Подкатегория'] = 'Квартиры'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Квартиры', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'doma')
async def doma(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Дома'])
    search_params['Подкатегория'] = 'Дома'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Дома', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'zemlja')
async def zemlja(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Земля'])
    search_params['Подкатегория'] = 'Земля'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Земля', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'garazhi')
async def garazhi(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Гаражи / стоянки'])
    search_params['Подкатегория'] = 'Гаражи / стоянки'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Гаражи / стоянки', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'kommercheskie')
async def kommercheskie(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Коммерческие помещения'])
    search_params['Подкатегория'] = 'Коммерческие помещения'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Коммерческие помещения', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'all_real_estate')
async def all_real_estate(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Недвижимость', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'moto')
async def moto(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Мото'])
    search_params['Подкатегория'] = 'Мото'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Мото', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'motozapchasti')
async def motozapchasti(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Мотозапчасти и аксессуары'])
    search_params['Подкатегория'] = 'Мотозапчасти и аксессуары'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Мотозапчасти и аксессуары', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'drugoytransport')
async def drugoytransport(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Другой транспорт'])
    search_params['Подкатегория'] = 'Другой транспорт'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Другой транспорт', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'avtobusy')
async def avtobusy(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Автобусы'])
    search_params['Подкатегория'] = 'Автобусы'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Автобусы', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'gruzovyeavtomobili')
async def gruzovyeavtomobili(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Грузовые автомобили'])
    search_params['Подкатегория'] = 'Грузовые автомобили'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Грузовые автомобили', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'pritsepy')
async def pritsepy(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Прицепы'])
    search_params['Подкатегория'] = 'Прицепы'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Прицепы', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'spetstehnika')
async def spetstehnika(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Спецтехника'])
    search_params['Подкатегория'] = 'Спецтехника'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Спецтехника', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'selhoztehnika')
async def selhoztehnika(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Сельхозтехника'])
    search_params['Подкатегория'] = 'Сельхозтехника'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Сельхозтехника', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'zapchastidlyaspetshtehniki')
async def zapchastidlyaspetshtehniki(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Запчасти для спец / с.х. техники'])
    search_params['Подкатегория'] = 'Запчасти для спец / с.х. техники'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Запчасти для спец / с.х. техники', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'vodnyytransport')
async def vodnyytransport(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Водный транспорт'])
    search_params['Подкатегория'] = 'Водный транспорт'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Водный транспорт', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'prochiezapchasti')
async def prochiezapchasti(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Прочие запчасти'])
    search_params['Подкатегория'] = 'Прочие запчасти'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Прочие запчасти', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'all_transport')
async def all_transport(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Транспорт', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'roznichnayatorgovlyaprodazhi')
async def roznichnayatorgovlyaprodazhi(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Розничная торговля / Продажи'])
    search_params['Подкатегория'] = 'Розничная торговля / Продажи'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Розничная торговля / Продажи', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'transportlogistika')
async def transportlogistika(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Транспорт / логистика'])
    search_params['Подкатегория'] = 'Транспорт / логистика'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Транспорт / логистика', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'stroitelstvo')
async def stroitelstvo(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Строительство'])
    search_params['Подкатегория'] = 'Строительство'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Строительство', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'baryrestoranyrazvlecheniya')
async def baryrestoranyrazvlecheniya(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Бары / рестораны'])
    search_params['Подкатегория'] = 'Бары / рестораны'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Бары / рестораны', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'yurisprudentsiyabuhgalteriya')
async def yurisprudentsiyabuhgalteriya(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Юриспруденция и бухгалтерия'])
    search_params['Подкатегория'] = 'Юриспруденция и бухгалтерия'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Юриспруденция и бухгалтерия', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'ohranabezopasnost')
async def ohranabezopasnost(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Охрана / безопасность'])
    search_params['Подкатегория'] = 'Охрана / безопасность'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Охрана / безопасность', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'domashniypersonal')
async def domashniypersonal(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Домашний персонал'])
    search_params['Подкатегория'] = 'Домашний персонал'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Домашний персонал', reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'turizm_otdyh_razvlecheniya')
async def turizm_otdyh_razvlecheniya(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Туризм / отдых / развлечения'])
    search_params['Подкатегория'] = 'Туризм / отдых / развлечения'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Туризм / отдых / развлечения', reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'obrazovanie')
async def obrazovanie(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Образование'])
    search_params['Подкатегория'] = 'Образование'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Образование', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'kultura_iskusstvo')
async def kultura_iskusstvo(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Культура / искусство'])
    search_params['Подкатегория'] = 'Культура / искусство'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Культура / искусство', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'meditsina_farmatsiya')
async def meditsina_farmatsiya(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Медицина / фармация'])
    search_params['Подкатегория'] = 'Медицина / фармация'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Медицина / фармация', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'it_telekom_kompyutery')
async def it_telekom_kompyutery(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['ИТ / телеком / компьютеры'])
    search_params['Подкатегория'] = 'ИТ / телеком / компьютеры'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='ИТ / телеком / компьютеры', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'nedvizhimost')
async def nedvizhimost(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Недвижимость'])
    search_params['Подкатегория'] = 'Недвижимость'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Недвижимость', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'marketing_reklama_dizayn')
async def marketing_reklama_dizayn(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Маркетинг / реклама / дизайн'])
    search_params['Подкатегория'] = 'Маркетинг / реклама / дизайн'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Маркетинг / реклама / дизайн', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'proizvodstvo_energetika')
async def proizvodstvo_energetika(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Производство / энергетика'])
    search_params['Подкатегория'] = 'Производство / энергетика'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Производство / энергетика', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'cekretariat_aho')
async def cekretariat_aho(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Cекретариат / АХО'])
    search_params['Подкатегория'] = 'Cекретариат / АХО'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Cекретариат / АХО', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'nachalo_karery_studenty')
async def nachalo_karery_studenty(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Начало карьеры / Студенты'])
    search_params['Подкатегория'] = 'Начало карьеры / Студенты'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Начало карьеры / Студенты', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'servis_i_byt')
async def servis_i_byt(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Сервис и быт'])
    search_params['Подкатегория'] = 'Сервис и быт'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Сервис и быт', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'drugie_sfery_zanyatiy')
async def drugie_sfery_zanyatiy(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Другие сферы занятий'])
    search_params['Подкатегория'] = 'Другие сферы занятий'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Другие сферы занятий', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'chastichnaya_zanyatost')
async def chastichnaya_zanyatost(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Частичная занятость'])
    search_params['Подкатегория'] = 'Частичная занятость'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Частичная занятость', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'all_jobs')
async def all_jobs(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Работа', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'sobaki')
async def sobaki(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Собаки'])
    search_params['Подкатегория'] = 'Собаки'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Собаки', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'koshki')
async def koshki(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Кошки'])
    search_params['Подкатегория'] = 'Кошки'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Кошки', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'akvariumnye-rybki')
async def akvariumnye_rybki(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Аквариумистика'])
    search_params['Подкатегория'] = 'Аквариумистика'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Аквариумистика', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'ptitsy')
async def ptitsy(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Птицы'])
    search_params['Подкатегория'] = 'Птицы'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Птицы', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'gryzuny')
async def gryzuny(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Грызуны'])
    search_params['Подкатегория'] = 'Грызуны'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Грызуны', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'selskohozyaystvennye-zhivotnye')
async def selskohozyaystvennye_zhivotnye(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Сельхоз животные'])
    search_params['Подкатегория'] = 'Сельхоз животные'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Сельхоз животные', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'tovary-dlya-zhivotnyh')
async def tovary_dlya_zhivotnyh(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Зоотовары'])
    search_params['Подкатегория'] = 'Зоотовары'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Зоотовары', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'vyazka')
async def vyazka(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Вязка'])
    search_params['Подкатегория'] = 'Вязка'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Вязка', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'byuro-nahodok')
async def byuro_nahodok(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Бюро находок'])
    search_params['Подкатегория'] = 'Бюро находок'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Бюро находок', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'drugie-zhivotnye')
async def drugie_zhivotnye(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Другие животные'])
    search_params['Подкатегория'] = 'Другие животные'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Другие животные', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'all_animals')
async def all_animals(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Все животные и зоотовары', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'mebel')
async def mebel(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Мебель'])
    search_params['Подкатегория'] = 'Мебель'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Мебель', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'sad-ogorod')
async def sad_ogorod(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Сад / огород'])
    search_params['Подкатегория'] = 'Сад / огород'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Задать параметры поиска', callback_data='city'))
    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Сад / огород', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'predmety-interera')
async def predmety_interera(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Предметы интерьера'])
    search_params['Подкатегория'] = 'Предметы интерьера'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Предметы интерьера', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'tovari-dlya-stroitelstva-remonta')
async def stroitelstva_remonta(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Товары для строительства/ремонта'])
    search_params['Подкатегория'] = 'Товары для строительства/ремонта'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Товары для строительства/ремонта', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'instrumenty')
async def instrumenty(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Инструменты'])
    search_params['Подкатегория'] = 'Инструменты'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Инструменты', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'komnatnye-rasteniya')
async def komnatnye_rasteniya(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Комнатные растения'])
    search_params['Подкатегория'] = 'Комнатные растения'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Комнатные растения', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'posuda-kuhonnaya-utvar')
async def kuhonnaya_utvar(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Посуда / кухонная утварь'])
    search_params['Подкатегория'] = 'Посуда / кухонная утварь'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Посуда / кухонная утварь', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'sadovyy-inventar')
async def sadovyy_inventar(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Садовый инвентарь'])
    search_params['Подкатегория'] = 'Садовый инвентарь'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Садовый инвентарь', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'hozyaystvennyy-inventar')
async def inventar(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Хозяйственный инвентарь / бытовая химия'])
    search_params['Подкатегория'] = 'Хозяйственный инвентарь / бытовая химия'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Хозяйственный инвентарь / бытовая химия', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'all_home_garden')
async def all_home_garden(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Дом и сад', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'kantstovary')
async def kantstovary(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Канцтовары / расходные материалы'])
    search_params['Подкатегория'] = 'Канцтовары / расходные материалы'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Канцтовары / расходные материалы', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'produkty_pitaniya')
async def produkty_pitaniya(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Продукты питания / Напитки'])
    search_params['Подкатегория'] = 'Продукты питания / Напитки'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Продукты питания / Напитки', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'prochie_tovary_dlya_doma')
async def prochie_tovary_dlya_doma(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Прочие товары для дома'])
    search_params['Подкатегория'] = 'Прочие товары для дома'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Прочие товары для дома', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'telefony')
async def telefony(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Телефоны'])
    search_params['Подкатегория'] = 'Телефоны'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Телефоны', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'kompyutery')
async def kompyutery(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Компьютеры'])
    search_params['Подкатегория'] = 'Компьютеры'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Компьютеры', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'tv_videotehnika')
async def tv_videotehnika(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Тв / видеотехника'])
    search_params['Подкатегория'] = 'Тв / видеотехника'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Тв / видеотехника', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'audiotehnika')
async def audiotehnika(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Аудиотехника'])
    search_params['Подкатегория'] = 'Аудиотехника'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Аудиотехника', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'igry_i_igrovye_pristavki')
async def igry_i_igrovye_pristavki(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Игры и игровые приставки'])
    search_params['Подкатегория'] = 'Игры и игровые приставки'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Игры и игровые приставки', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'tehnika_dlya_doma')
async def tehnika_dlya_doma(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Техника для дома'])
    search_params['Подкатегория'] = 'Техника для дома'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Техника для дома', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'tehnika_dlya_kuhni')
async def tehnika_dlya_kuhni(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Техника для кухни'])
    search_params['Подкатегория'] = 'Техника для кухни'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Техника для кухни', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'klimaticheskoe_oborudovanie')
async def klimaticheskoe_oborudovanie(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Климатическое оборудование'])
    search_params['Подкатегория'] = 'Климатическое оборудование'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Климатическое оборудование', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'individualnyy_uhod')
async def individualnyy_uhod(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Индивидуальный уход'])
    search_params['Подкатегория'] = 'Индивидуальный уход'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Индивидуальный уход', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'aksessuary_i_komplektuyuschie')
async def aksessuary_i_komplektuyuschie(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Аксессуары и комплектующие'])
    search_params['Подкатегория'] = 'Аксессуары и комплектующие'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Аксессуары и комплектующие', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'prochaja_electronika')
async def prochaja_electronika(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Прочая электроника'])
    search_params['Подкатегория'] = 'Прочая электроника'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Прочая электроника', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'all_electronics')
async def all_electronics(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Прочая электроника', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'all_electronics')
async def all_electronics(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Прочая электроника', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'stroitelstvo_remont')
async def stroitelstvo_remont(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Строительство / ремонт / уборка'])
    search_params['Подкатегория'] = 'Строительство / ремонт / уборка'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Строительство / ремонт / уборка', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'finansovye_uslugi')
async def finansovye_uslugi(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Финансовые услуги / партнерство'])
    search_params['Подкатегория'] = 'Финансовые услуги / партнерство'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Финансовые услуги / партнерство', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'perevozki_arenda')
async def perevozki_arenda(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Перевозки / аренда транспорта'])
    search_params['Подкатегория'] = 'Перевозки / аренда транспорта'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Перевозки / аренда транспорта', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'reklama_marketing')
async def reklama_marketing(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Реклама / полиграфия / маркетинг / интернет'])
    search_params['Подкатегория'] = 'Реклама / полиграфия / маркетинг / интернет'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Реклама / полиграфия / маркетинг / интернет', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'nyani_sidelki')
async def nyani_sidelki(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Няни / сиделки'])
    search_params['Подкатегория'] = 'Няни / сиделки'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Реклама / полиграфия / маркетинг / интернет', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'syre_materialy')
async def syre_materialy(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Сырьё / материалы'])
    search_params['Подкатегория'] = 'Сырьё / материалы'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Сырьё / материалы', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'krasota_zdorove')
async def krasota_zdorove(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Красота / здоровье'])
    search_params['Подкатегория'] = 'Красота / здоровье'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Красота / здоровье', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'oborudovanie')
async def oborudovanie(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Оборудование'])
    search_params['Подкатегория'] = 'Оборудование'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Оборудование', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'obrazovanie')
async def obrazovanie(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Образование / Спорт'])
    search_params['Подкатегория'] = 'Образование / Спорт'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Образование / Спорт', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'uslugi_zhivotnyh')
async def uslugi_zhivotnyh(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Услуги для животных'])
    search_params['Подкатегория'] = 'Услуги для животных'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Услуги для животных', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'prodazha_biznesa')
async def prodazha_biznesa(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Продажа бизнеса'])
    search_params['Подкатегория'] = 'Продажа бизнеса'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Продажа бизнеса', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'razvlechenie_foto_video')
async def razvlechenie_foto_video(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Развлечения / Искусство / Фото / Видео'])
    search_params['Подкатегория'] = 'Развлечения / Искусство / Фото / Видео'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Развлечения / Искусство / Фото / Видео', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'turizm')
async def turizm(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Туризм'])
    search_params['Подкатегория'] = 'Туризм'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Туризм', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'perevodchiki_nabor_teksta')
async def perevodchiki_nabor_teksta(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Услуги переводчиков / набор текста'])
    search_params['Подкатегория'] = 'Услуги переводчиков / набор текста'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Услуги переводчиков / набор текста', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'avtomoto')
async def avtomoto(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Авто / мото услуги'])
    search_params['Подкатегория'] = 'Авто / мото услуги'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Авто / мото услуги', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'obsluzhivanie')
async def obsluzhivanie(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Обслуживание, ремонт техники'])
    search_params['Подкатегория'] = 'Обслуживание, ремонт техники'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Обслуживание, ремонт техники', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'yuridicheskie')
async def yuridicheskie(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Юридические услуги'])
    search_params['Подкатегория'] = 'Юридические услуги'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Юридические услуги', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'prokat')
async def prokat(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Прокат товаров'])
    search_params['Подкатегория'] = 'Прокат товаров'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Прокат товаров', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'prochie')
async def prochie(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Прочие услуги'])
    search_params['Подкатегория'] = 'Прочие услуги'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Прочие услуги', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'all_business')
async def all_business(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Бизнес и услуги', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'odezhda')
async def odezhda(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Одежда/обувь'])
    search_params['Подкатегория'] = 'Одежда/обувь'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Одежда/обувь', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'svadby')
async def svadby(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Для свадьбы'])
    search_params['Подкатегория'] = 'Для свадьбы'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Для свадьбы', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'modaraznoe')
async def modaraznoe(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Мода разное'])
    search_params['Подкатегория'] = 'Мода разное'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Мода разное', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'naruchnye')
async def naruchnye(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Наручные часы'])
    search_params['Подкатегория'] = 'Наручные часы'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Наручные часы', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'aksessuary')
async def aksessuary(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Аксессуары'])
    search_params['Подкатегория'] = 'Аксессуары'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Аксессуары', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'podarki')
async def podarki(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Подарки'])
    search_params['Подкатегория'] = 'Подарки'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Подарки', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'all_fashion')
async def all_fashion(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Мода и стиль', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'antikvariat')
async def antikvariat(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Антиквариат / коллекции'])
    search_params['Подкатегория'] = 'Антиквариат / коллекции'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Антиквариат / коллекции', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'muzykalnye')
async def muzykalnye(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Музыкальные инструменты'])
    search_params['Подкатегория'] = 'Музыкальные инструменты'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Музыкальные инструменты', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'drugoe')
async def drugoe(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Другое'])
    search_params['Подкатегория'] = 'Другое'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Другое', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'sportotdyh')
async def sportotdyh(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Спорт / отдых'])
    search_params['Подкатегория'] = 'Спорт / отдых'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Спорт / отдых', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'knigi')
async def knigi(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Книги / журналы'])
    search_params['Подкатегория'] = 'Книги / журналы'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Книги / журналы', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'cddvd')
async def cddvd(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['CD / DVD / пластинки / кассеты'])
    search_params['Подкатегория'] = 'CD / DVD / пластинки / кассеты'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='CD / DVD / пластинки / кассеты', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'bilety')
async def bilety(callback_query: types.CallbackQuery):
    search_url.append(CATEGORIES['Билеты'])
    search_params['Подкатегория'] = 'Билеты'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Билеты', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'all_sport')
async def all_sport(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Хобби, спорт и отдых', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'free')
async def free(callback_query: types.CallbackQuery):
    search_url.append('/list/?search%5Bfilter_enum_price%5D%5B0%5D=free')
    search_params['Подкатегория'] = 'Отдам даром'
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Поиск объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Отдам даром', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'exchange')
async def exchange(callback_query: types.CallbackQuery):
    search_url.append('/list/?search%5Bfilter_enum_price%5D%5B0%5D=exchange')
    search_params['Подкатегория'] = 'Обмен'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Искать 10 объявлений', callback_data='search'))
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Отдам даром', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'to_main')
async def to_main(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await send_welcome(message=callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'get_params')
async def get_params(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Далее', callback_data='search'))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Нажмите "далее"', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'search')
async def get_advs(callback_query: types.CallbackQuery):
    url = ''.join(search_url)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('На главную', callback_data='to_main'))
    advs = await main_get_advertisements(url=url, amount=10)
    await bot.answer_callback_query(callback_query.id, show_alert=False)
    for adv in advs:
        text = adv['title'] + '\n' + adv['desc'] + '\n' + adv['price'] + '\n' + URL_MAIN + adv['href']
        for image in adv['img']:
            await bot.send_photo(chat_id=callback_query.message.chat.id, photo=image)
        await bot.send_message(chat_id=callback_query.message.chat.id, text=text,)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="На главную", reply_markup=markup)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



