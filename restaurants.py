import requests 
from datetime import date

# All restaurants
restaurant_urls = {
    'Joensuu':['https://www.compass-group.fi/menuapi/feed/json?costNumber=0417&language=fi',
                        'https://www.compass-group.fi/menuapi/feed/json?costNumber=0413&language=fi',
                        'https://www.compass-group.fi/menuapi/feed/json?costNumber=041704&language=fi',
                        'https://www.compass-group.fi/menuapi/feed/json?costNumber=0433&language=fi',
                        'https://www.compass-group.fi/menuapi/feed/json?costNumber=041702&language=fi',
                        'https://www.compass-group.fi/menuapi/feed/json?costNumber=041703&language=fi'],
    'Helsinki': ['https://www.compass-group.fi/menuapi/feed/json?costNumber=1256&language=fi',
                        'https://www.compass-group.fi/menuapi/feed/json?costNumber=3003&language=fi',
                        'https://www.compass-group.fi/menuapi/feed/json?costNumber=3104&language=fi',
                        'https://www.compass-group.fi/menuapi/feed/json?costNumber=3406&language=fi',
                        'https://www.compass-group.fi/menuapi/feed/json?costNumber=3100&language=fi',
                        'https://www.compass-group.fi/menuapi/feed/json?costNumber=3067&language=fi',
                        'https://www.compass-group.fi/menuapi/feed/json?costNumber=1251&language=fi',
                        'https://www.compass-group.fi/menuapi/feed/json?costNumber=0083&language=fi',
                        'https://www.compass-group.fi/menuapi/feed/json?costNumber=3704&language=fi'],
    'Kuopio': ['https://www.compass-group.fi/menuapi/feed/json?costNumber=0442&language=fi',
                      'https://www.compass-group.fi/menuapi/feed/json?costNumber=0436&language=fi',
                      'https://www.compass-group.fi/menuapi/feed/json?costNumber=0437&language=fi',
                      'https://www.compass-group.fi/menuapi/feed/json?costNumber=0439&language=fi'],
    'Tampere': ['https://www.compass-group.fi/menuapi/feed/json?costNumber=0815&language=fi',
                'https://www.compass-group.fi/menuapi/feed/json?costNumber=0812&language=fi'],
    'Vaasa':   ['https://www.compass-group.fi/menuapi/feed/json?costNumber=3567&language=fi',
                'https://www.compass-group.fi/menuapi/feed/json?costNumber=3597&language=fi'],
    'Espoo':   ['https://www.compass-group.fi/menuapi/feed/json?costNumber=3087&language=fi',
                'https://www.compass-group.fi/menuapi/feed/json?costNumber=0190&language=fi',
                'https://www.compass-group.fi/menuapi/feed/json?costNumber=3101&language=fi',
                'https://www.compass-group.fi/menuapi/feed/json?costNumber=3292&language=fi',
                'https://www.compass-group.fi/menuapi/feed/json?costNumber=3208&language=fi']
}




def get_menu(url):
    response = requests.get(url)
    data = response.json()
    menu = data['MenusForDays']
    return menu

def get_restaurant_name(url):
    response = requests.get(url)
    data = response.json()
    name = data['RestaurantName']
    return name

def get_restaurant_menu(menu):
    menu_list = {}
    for day in menu:
        if day['Date'][:10] == str(date.today()):
            for meal in day['SetMenus']:
                if meal['Name'] != None:
                    menu_list[meal['Name']] = meal['Components']
    return menu_list



def get_menu_string(menu_list):
    menustrings = []
    for menu in menu_list:
        menu_string = ''
        if menu == {}:
            menustrings.append('')
            continue
        for meal, components in menu.items():
            menu_string += f'{meal}:\n'
            for component in components:
                menu_string += f'- {component}\n'
            menu_string += '\n'
        menustrings.append(menu_string)
    return menustrings

# Menus
all_menus = [[get_menu(url) for url in urls] for urls in restaurant_urls.values()]

# Restaurant names
all_restaurantNames = [[get_restaurant_name(url) for url in urls] for urls in restaurant_urls.values()]

# Menus for each restaurant
restaurantMenus = [[get_restaurant_menu(menu) for menu in menus] for menus in all_menus]

# Menu strings for each restaurant
menuStrings = [get_menu_string(menu) for menu in restaurantMenus]

cities = [city for city in restaurant_urls]
restaurants = [restaurantNames for restaurantNames in all_restaurantNames]
menus = []
for i in range (len(menuStrings)):
    temp = []
    for menu in menuStrings[i]:
        temp.append(menu)
    menus.append(temp)

print(restaurants)
