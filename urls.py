URL_MAIN = 'https://www.olx.uz/'

CATEGORIES = {
    'Детская одежда': 'detskaya-odezhda/',
    'Детская обувь': 'detskaya-obuv/',
    'Детские коляски': 'detskie-kolyaski/',
    'Детские автокресла': 'detskie-avtokresla/',
    'Детская мебель': 'detskaya-mebel/',
    'Игрушки': 'igrushki/',
    'Детский транспорт': 'detskiy-transport/',
    'Кормление': 'kormlenie/',
    'Товары для школьников': 'tovary-dlya-shkolnikov/',
    'Прочие детские товары': 'prochie-detskie-tovary/',
    'Посуточная аренда': 'posutochno_pochasovo/',
    'Квартиры': 'kvartiry/',
    'Дома': 'doma/',
    'Земля': 'zemlja/',
    'Гаражи / стоянки': 'garazhi-stoyanki/',
    'Коммерческие помещения': 'kommercheskie-pomeshcheniya/',
    'Легковые автомобили': 'legkovye-avtomobili/',
    'Автозапчасти и аксессуары': 'avtozapchasti-i-aksessuary/',
    'Шины, диски и колёса': 'shiny-diski-i-kolesa/',
    'Мото': 'moto/',
    'Мотозапчасти и аксессуары': 'motozapchasti-i-aksessuary/',
    'Другой транспорт': 'drugoy-transport/',
    'Автобусы': 'avtobusy/',
    'Грузовые автомобили': 'gruzovye-avtomobili/',
    'Прицепы': 'pritsepy/',
    'Спецтехника': 'spetstehnika/',
    'Сельхозтехника': 'selhoztehnika/',
    'Запчасти для спец / с.х. техники': 'zapchasti-dlya-spets-sh-tehniki/',
    'Водный транспорт': 'vodnyy-transport/',
    'Прочие запчасти': 'prochie-zapchasti/',
    'Розничная торговля / Продажи': 'roznichnaya-torgovlya-prodazhi/',
    'Транспорт / логистика': 'transport-logistika/',
    'Строительство': 'stroitelstvo/',
    'Бары / рестораны': 'bary-restorany-razvlecheniya/',
    'Юриспруденция и бухгалтерия': 'yurisprudentsiya-i-buhgalteriya/',
    'Охрана / безопасность': 'ohrana-bezopasnost/',
    'Домашний персонал': 'domashniy-personal/',
    'Красота / фитнес / спорт': 'krasota-fitnes-sport/',
    'Туризм / отдых / развлечения': 'turizm-otdyh-razvlecheniya/',
    'Образование': 'obrazovanie/',
    'Культура / искусство': 'kultura-iskusstvo/',
    'Медицина / фармация': 'meditsina-farmatsiya/',
    'ИТ / телеком / компьютеры': 'it-telekom-kompyutery/',
    'Недвижимость': 'nedvizhimost/',
    'Маркетинг / реклама / дизайн': 'marketing-reklama-dizayn/',
    'Производство / энергетика': 'proizvodstvo-energetika/',
    'Cекретариат / АХО': 'cekretariat-aho/',
    'Начало карьеры / Студенты': 'nachalo-karery-studenty/',
    'Сервис и быт': 'servis-i-byt/',
    'Другие сферы занятий': 'drugie-sfery-zanyatiy/',
    'Частичная занятость': 'chastichnaya-zanyatost/',
    'Собаки': 'sobaki/',
    'Кошки': 'koshki/',
    'Аквариумистика': 'akvariumnye-rybki/',
    'Птицы': 'ptitsy/',
    'Грызуны': 'gryzuny/',
    'Сельхоз животные': 'selskohozyaystvennye-zhivotnye/',
    'Зоотовары': 'tovary-dlya-zhivotnyh/',
    'Вязка': 'vyazka/',
    'Бюро находок': 'byuro-nahodok/',
    'Другие животные': 'drugie-zhivotnye/',
    'Животные даром': 'zhivotnye-darom/',
    'Мебель': 'mebel/',
    'Сад / огород': 'sad-ogorod/',
    'Предметы интерьера': 'predmety-interera/',
    'Товары для строительства/ремонта': 'tovari-dlya-stroitelstva-remonta/',
    'Инструменты': 'instrumenty/',
    'Комнатные растения': 'komnatnye-rasteniya/',
    'Посуда / кухонная утварь': 'posuda-kuhonnaya-utvar/',
    'Садовый инвентарь': 'sadovyy-inventar/',
    'Хозяйственный инвентарь / бытовая химия': 'hozyaystvennyy-inventar/',
    'Канцтовары / расходные материалы': 'kantstovary-rashodnye-materialy/',
    'Продукты питания / Напитки': 'produkty-pitaniya-napitki/',
    'Прочие товары для дома': 'prochie-tovary-dlya-doma/',
    'Телефоны': 'telefony/',
    'Компьютеры': 'kompyutery/',
    'Фото / видео': 'foto-video/',
    'Тв / видеотехника': 'tv-videotehnika/',
    'Аудиотехника': 'audiotehnika/',
    'Игры и игровые приставки': 'igry-i-igrovye-pristavki/',
    'Техника для дома': 'tehnika-dlya-doma/',
    'Техника для кухни': 'tehnika-dlya-kuhni/',
    'Климатическое оборудование': 'klimaticheskoe-oborudovanie/',
    'Индивидуальный уход': 'individualnyy-uhod/',
    'Аксессуары и комплектующие': 'aksessuary-i-komplektuyuschie/',
    'Прочая электроника': 'prochaja-electronika/',
    'Строительство / ремонт / уборка': 'stroitelstvo-otdelka-remont/',
    'Финансовые услуги / партнерство': 'finansovye-uslugi/',
    'Перевозки / аренда транспорта': 'perevozki-arenda-transporta/',
    'Реклама / полиграфия / маркетинг / интернет': 'reklama-marketing-pr/',
    'Няни / сиделки': 'nyani-sidelki/', 'Сырьё / материалы': 'syre-materialy/',
    'Красота / здоровье': 'krasota-zdorove/', 'Оборудование': 'oborudovanie/',
    'Образование / Спорт': 'obrazovanie/', 'Услуги для животных': 'uslugi-dlya-zhivotnyh/',
    'Продажа бизнеса': 'prodazha-biznesa/',
    'Развлечения / Искусство / Фото / Видео': 'razvlechenie-foto-video/',
    'Туризм': 'turizm/',
    'Услуги переводчиков / набор текста': 'uslugi-perevodchikov-nabor-teksta/',
    'Авто / мото услуги': 'avto-moto-uslugi/',
    'Обслуживание, ремонт техники': 'obsluzhivanie-remont-tehniki/',
    'Юридические услуги': 'yuridicheskie-uslugi/', 'Прокат товаров': 'prokat-tovarov/',
    'Прочие услуги': 'prochie-usligi/', 'Одежда/обувь': 'odezhda/',
    'Для свадьбы': 'dlya-svadby/', 'Мода разное': 'moda-raznoe/',
    'Наручные часы': 'naruchnye-chasy/', 'Аксессуары': 'aksessuary/',
    'Подарки': 'podarki/',
    'Антиквариат / коллекции': 'hobbi-otdyh-i-sport/antikvariat-kollektsii/',
    'Музыкальные инструменты': 'hobbi-otdyh-i-sport/muzykalnye-instrumenty/',
    'Другое': 'hobbi-otdyh-i-sport/drugoe/', 'Спорт / отдых': 'hobbi-otdyh-i-sport/sport-otdyh/',
    'Книги / журналы': 'hobbi-otdyh-i-sport/knigi-zhurnaly/',
    'CD / DVD / пластинки / кассеты': 'hobbi-otdyh-i-sport/cd-dvd-plastinki/',
    'Билеты': 'hobbi-otdyh-i-sport/bilety/'
}

SUBCATEGORIES = {
    'Аренда долгосрочная': 'arenda-dolgosrochnaya/',
    'Продажа': 'prodazha/',
    'Обмен': 'obmen/',
    'Хостелы': 'hostel/',
    'Отели': 'oteli/',
    'Квартиры': 'kvartira/',
    'Дома': 'dachi/',
    'Санатории': 'sanatorii/'
}

AREAS = {
    'Андижанская область ': {'Акалтын': 'oqoltin/', 'Алтынкуль': 'oltinkol/', 'Андижан': 'andizhan/', 'Асака': 'asaka/',
                             'Ахунбабаев': 'ahunbabaev/', 'Балыкчи': 'baliqchi/', 'Боз': 'boz/',
                             'Булакбаши': 'buloqboshi/', 'Карасу': 'qorasuv/', 'Куйганъяр': 'kuyganyor/',
                             'Кургантепа': 'kurgantepa/', 'Мархамат': 'marhamat/', 'Пайтуг': 'pajtug/',
                             'Пахтаабад': 'pahtaabad/', 'Шахрихан': 'shahrihan/', 'Ханабад': 'hanabad/',
                             'Ходжаабад': 'hodzhaabad/', 'Андижанская область ': 'andizhanskaya-oblast/'},
    'Бухарская область': {'Алат': 'alat/', 'Бухара': 'buhara/', 'Галаасия': 'galaasiya/', 'Газли': 'gazli/',
                          'Гиждуван': 'gizhduvan/', 'Каган': 'kagan/', 'Каракуль': 'karakul/',
                          'Караулбазар': 'qorovulbozor/', 'Ромитан': 'romitan/', 'Шафиркан': 'shafirkan/',
                          'Вабкент': 'vabkent/', 'Жондор': 'jondor/', 'Бухарская область': 'buharskaya-oblast/', },
    'Джизакская область': {'Айдаркуль': 'aydar_koli/', 'Баландчакир': 'balandchaqir/', 'Даштобод': 'dashtobod/',
                           'Дустлик': 'dustlik/', 'Джизак': 'dzhizak/', 'Гагарин': 'gagarin/',
                           'Галлаарал': 'gallyaaral/', 'Голиблар': 'goliblar/', 'Марджанбулак': 'mardzhanbulak/',
                           'Пахтакор': 'pahtakor/', 'Учтепа': 'uchtepa/', 'Усмат': 'osmat/',
                           'Янгикишлак': 'yangiqishloq/', 'Заамин': 'zomin/', 'Зафарабад': 'zafarobod/',
                           'Зарбдар': 'zarbdor/', 'Джизакская область': 'dzhizakskaya-oblast/'},
    'Каракалпакстан': {'Акмангит': 'oqmangit/', 'Беруни': 'beruni/', 'Бустан': 'bustan/', 'Чимбай': 'chimbaj/',
                       'Канлыкуль': 'qanlikol/', 'Караузяк': 'qoraozak/', 'Кегейли': 'kegeyli/', 'Кунград': 'kungrad/',
                       'Мангит': 'mangit/', 'Муйнак': 'mujnak/', 'Нукус': 'nukus/', 'Шуманай': 'shumanaj/',
                       'Тахиаташ': 'tahiatash/', 'Тахтакупыр': 'taxtakopir/', 'Турткуль': 'turtkul/',
                       'Ходжейли': 'hodzhejli/', 'Каракалпакстан': 'karakalpakstan/'},
    'Кашкадарьинская область': {'Бешкент': 'beshkent/', 'Чиракчи': 'chirakchi/', 'Дехканабад': 'dehkanabad/',
                                'Гузар': 'guzar/', 'Камаши': 'kamashi/', 'Карашина': 'karashina/', 'Карши': 'karshi/',
                                'Касан': 'kasan/', 'Касби': 'kasbi/', 'Китаб': 'kitab/', 'Мубарек': 'mubarek/',
                                'Муглан': 'muglon/', 'Шахрисабз': 'shahrisabz/', 'Талимарджан\t': 'talimardzhan/',
                                'Яккабаг': 'yakkabag/', 'Янги Миришкор': 'mirishkor/', 'Янги-Нишан': 'nishan/',
                                'Кашкадарьинская область': 'kashkadarinskaya-oblast/'},
    'Навоийская область': {'Бешрабат': 'beshrobot/', 'Канимех': 'konimex/', 'Кармана': 'karmana/',
                           'Кызылтепа': 'kyzyltepa/', 'Навои': 'navoi/', 'Нурата': 'nurata/',
                           'Тамдыбулак': 'tomdibuloq/', 'Учкудук': 'uchkuduk/', 'Янгирабат': 'yangirabat/',
                           'Зарафшан': 'zarafshan/', 'Навоийская область': 'navoijskaya-oblast/'},
    'Наманганская область': {'Чартак': 'chartak/', 'Челак': 'chust/', 'Чуст': 'chust/', 'Джумашуй': 'jomashoy/',
                             'Касансай': 'kasansaj/', 'Наманган': 'namangan/', 'Пап': 'pap/', 'Ташбулак': 'toshbuloq/',
                             'Туракурган': 'turakurgan/', 'Учкурган': 'uchkurgan/', 'Хаккулабад': 'hakulabad/',
                             'Наманганская область': 'namanganskaya-oblast/'},
    'Самаркандская область': {'Акташ': 'aktash/', 'Булунгур': 'bulungur/', 'Чилек': 'chilek/', 'Дарбанд': 'darband/',
                              'Джамбай': 'dzhambaj/', 'Джума': 'dzhuma/', 'Гузалкент': 'gozalkent/',
                              'Гюлабад': 'gulobod/', 'Иштыхан': 'ishtyhan/', 'Каттакурган': 'kattakurgan/',
                              'Кушрабад': 'qoshrobod/', 'Лаиш': 'loish/', 'Нурабад': 'nurabad/', 'Пайарык': 'payariq/',
                              'Пайшанба': 'payshanba/', 'Самарканд': 'samarkand/', 'Тайлак': 'tayloq/',
                              'Ургут': 'urgut/', 'Зиадин': 'ziadin/',
                              'Самаркандская область': 'samarkandskaya-oblast/'},
    'Сурхандарьинская область': {'Ангор': 'angor/', 'Байсун': 'bajsun/', 'Бандихон': 'bandixon/', 'Денау': 'denau/',
                                 'Джаркурган': 'dzharkurgan/', 'Карлук': 'qorlik/', 'Кизирик': 'kizirik/',
                                 'Кумкурган': 'kumkurgan/', 'Музрабад': 'muzrabad/', 'Сариасия': 'sariosiyo/',
                                 'Сарык': 'sariq/', 'Шаргунь': 'shargun/', 'Шерабад': 'sherabad/', 'Шурчи': 'shurchi/',
                                 'Термез': 'termez/', 'Учкызыл': 'uchqizil/', 'Узун': 'uzun/', 'Халкабад': 'xalqobod/',
                                 'Сурхандарьинская область': 'surhandarinskaya-oblast/'},
    'Сырдарьинская область': {'Бахт': 'baht/', 'Баяут': 'boyovut/', 'Cырдарья': 'sirdaryo/', 'Гулистан': 'gulistan/',
                              'Навруз': 'navroz/', 'Сайхун': 'sayxun/', 'Сардоба': 'sardoba/', 'Ширин': 'shirin/',
                              'Сырдарья': 'syrdarya/', 'Теренозек': 'terenozek/', 'Хаваст': 'xovos/',
                              'Янгиер': 'yangier/', 'Янгиёр': 'yangiyer/',
                              'Сырдарьинская область': 'syrdarinskaya-oblast/'},
    'Ташкентская область': {'Аккурган': 'akkurgan/', 'Алмалык': 'almalyk/', 'Ангрен': 'angren/',
                            'Ахангаран': 'ahangaran/', 'Бекабад': 'bekabad/', 'Большой Чимган': 'katta_chimyon/',
                            'Бука': 'buka/', 'Чарвак': 'chorvoq/', 'Чиназ': 'chinaz/', 'Чирчик': 'chirchik/',
                            'Cукок': 'so_qoq/', 'Дурмень': 'durmen/', 'Дустабад': 'dustabad/',
                            'Эшангузар': 'eshanguzar/', 'Газалкент': 'gazalkent/', 'Гульбахор': 'gulbahor/',
                            'Искандар': 'iskandar/', 'Карасу': 'qorasuv/', 'Келес': 'keles/', 'Кибрай': 'kibraj/',
                            'Коксарай': 'koksaroy/', 'Красногорск': 'krasnogórsk/', 'Мирабад': 'mirobod/',
                            'Назарбек': 'nazarbek/', 'Нурафшан (Тойтепа)': 'tojtepa/', 'Паркент': 'parkent/',
                            'Пскент': 'pskent/', 'Салар': 'salar/', 'Ташкент': 'tashkent/', 'Ташморе': 'tashmore/',
                            'Туркестан': 'turkiston/', 'Уртааул': 'ortaovul/', 'Ходжикент': 'xojakent/',
                            'Янгиабад': 'yangiobod/', 'Янгибазар': 'yangibazar/', 'Янгиюль': 'yangiyul/',
                            'Зафар': 'zafar/', 'Зангиата': 'zangiota/', 'Ташкентская область': 'toshkent-oblast/'},
    'Ферганская область': {'Алтыарык': 'oltiariq/', 'Багдад': 'bogdod/', 'Бешарык': 'besharyk/', 'Дангара': 'dangara/',
                           'Фергана': 'fergana/', 'Коканд': 'kokand/', 'Кува': 'kuva/', 'Кувасай': 'kuvasaj/',
                           'Лангар': 'langar/', 'Маргилан': 'margilan/', 'Навбахор': 'navbahor/', 'Раван': 'ravon/',
                           'Риштан': 'rishtan/', 'Шахимардан': 'shohimardon/', 'Ташлак': 'toshloq/',
                           'Учкуприк': 'uchkopriq/', 'Вуадиль': 'vodil/', 'Хамза': 'hamza/', 'Яйпан': 'yaypan/',
                           'Янги Маргилан': 'yangi_margilon/', 'Янгикурган': 'yangiqorgon/', 'Язъяван': 'yozyovon/',
                           'Ферганская область': 'ferganskaya-oblast/'},
    'Хорезмская область': {'Багат': 'bagat/', 'Чалыш': 'cholish/', 'Гурлен': 'gurlen/', 'Караул': 'qorovul/',
                           'Кошкупыр': 'qoshkopir/', 'Питнак': 'pitnak/', 'Шават': 'shovot/', 'Ургенч': 'urgench/',
                           'Ханка': 'hanka/', 'Хазарасп': 'xozarasp/', 'Хива': 'hiva/', 'Янгиарык': 'yangiariq/',
                           'Хорезмская область': 'horezmskaya-oblast/'}
}

TASHKENT_DISTRICTS = {
    'Алмазарский район': '?search%5Bdistrict_id%5D=20',
    'Бектемирский район': '?search%5Bdistrict_id%5D=18',
    'Мирзо-улугбекский район': '?search%5Bdistrict_id%5D=12',
    'Мирабадский район': '?search%5Bdistrict_id%5D=13',
    'Сергелийский район': '?search%5Bdistrict_id%5D=19',
    'Учтепинский район': '?search%5Bdistrict_id%5D=21',
    'Яшнабадский район': '?search%5Bdistrict_id%5D=22',
    'Чиланзарский район': '?search%5Bdistrict_id%5D=23',
    'Шайхантахурский район': '?search%5Bdistrict_id%5D=24',
    'Юнусабадский район': '?search%5Bdistrict_id%5D=25',
    'Яккасарайский район': '?search%5Bdistrict_id%5D=26'
}

CURRENCY = {'sum': '?currency=UZS', 'dollar': '?currency=UYE'}

CONDITION = {
    'used': '&search%5Bfilter_enum_state%5D%5B0%5D=used',
    'new': '&search%5Bfilter_enum_state%5D%5B0%5D=new'
}

price_from = None
price_to = None

PRICE = {
    'from': f'&search%5Bfilter_float_price:from%5D={price_from}',
    'to': f'&search%5Bfilter_float_price:to%5D={price_to}'
}

rooms_from = None
rooms_to = None
ROOMS = {
    'from': f'&search%5Bfilter_float_number_of_rooms:from%5D={rooms_from}',
    'to': f'&search%5Bfilter_float_number_of_rooms:to%5D={rooms_to}'
}

#todo: add sizes for clothes

total_area_from = None
total_area_to = None

TOTAL_AREA = {
    'from': f'&search%5Bfilter_float_total_area:from%5D={total_area_from}',
    'to': f'&search%5Bfilter_float_total_area:to%5D={total_area_to}'
}

FURNISHED = {
    'yes': '&search%5Bfilter_enum_furnished%5D%5B0%5D=yes',
    'no': '&search%5Bfilter_enum_furnished%5D%5B0%5D=no'
}

floor_from = None
floor_to = None

FLOOR = {
    'from': f'&search%5Bfilter_float_floor:from%5D={floor_from}',
    'to': f'&search%5Bfilter_float_floor:to%5D={floor_to}'
}

all_floors_from = None
all_floors_to = None

ALL_FLOORS = {
    'from': f'&search%5Bfilter_float_total_floors:from%5D={all_floors_from}',
    'to': f'&search%5Bfilter_float_total_floors:to%5D={all_floors_to}'
}

SORTING = {
    'cheapest': '&search%5Border%5D=filter_float_price:asc',
    'most_expensive': '&search%5Border%5D=filter_float_price:desc',
    'newest': '&search%5Border%5D=created_at:desc'
}

#todo: add params for daily

JOB_STATUS = {
    'offer': '&search%5Boffer_seek%5D=offer',
    'seek': '&search%5Boffer_seek%5D=seek'
}

LENGHT_OF_EMPLOYMENT = {
    'permanent': '&search%5Bfilter_enum_job_type%5D%5B0%5D=perm',
    'temporary': '&search%5Bfilter_enum_job_type%5D%5B0%5D=temp'
}

FORM_OF_EMPLOYMENT = {
    'full-time': '&search%5Bfilter_enum_job_timing%5D%5B0%5D=full',
    'temporary': '&search%5Bfilter_enum_job_timing%5D%5B0%5D=part'
}

salary_from = None
salary_to = None

SALARY = {
    'from': f'&search%5Bfilter_float_salary:from%5D={salary_from}',
    'to': f'&search%5Bfilter_float_salary:to%5D={salary_to}'
}

TELECOMMUTING = '&search%5Bfilter_enum_remote_work%5D%5B0%5D=1'



