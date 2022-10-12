"""

This script will show a menu on the Raspberry Pi Sense Hat to
lookup the ip addresses of all interfaces. Menu can be operated
through the joystick on the Sense Hat.
The interfaces are abbreviated to a single letter for faster
scrolling, and 'x' exits the script.

Up/down    : scroll through menu-items
Left/right : show full name of the interface/menu-item
Middle     : show ip-address for selected interface

Ip-addresses and interfaces are refreshed after eacht joystick release.

"""

from sense_hat import SenseHat
from netifaces import interfaces, ifaddresses, AF_INET

sense = SenseHat()

menu = []


# exit program
def exit_menu(dummy):
    sense.show_message('Bye')
    exit()


# show ip address
def show(ip):
    sense.show_message(ip)
    print(ip)


# refresh interfaces and update menu
def refresh_menu():
    global menu
    menu = []
    for interface in interfaces():
        # skip interface localhost
        if interface == 'lo':
            continue

        # add interface to menu, and lookup ip-address
        ip = 'None'  # default None
        if AF_INET in ifaddresses(interface):
            for link in ifaddresses(interface)[AF_INET]:
                ip = link['addr']  # TODO: check multiple ips on single interface?

        menu.append({'name': interface, 'short_name': interface[0], 'param': ip, 'function': show})

    # add exit a last option to the menu
    menu.append({'name': 'exit', 'short_name': 'x', 'param': '', 'function': exit_menu})


# init
refresh_menu()
menu_item = 0
print(menu[menu_item]['name'])
sense.show_letter(menu[menu_item]['short_name'])

# menu
while True:
    for event in sense.stick.get_events():
        direction = event.direction
        action = event.action
        if action == 'released':
            # refresh menu after each joystick release to
            # add new connected interfaces (eg. usb dongle)
            # and refresh the ip-addresses
            refresh_menu()

            # scroll through menu
            if direction == 'up':
                menu_item -= 1
            if direction == 'down':
                menu_item += 1
            menu_item = menu_item % len(menu)

            # execute menu function
            if direction == 'middle':
                menu[menu_item]['function'](menu[menu_item]['param'])
            print(menu[menu_item]['name'])
            sense.show_letter(menu[menu_item]['short_name'])

            # show full menu name
            if direction == 'right' or direction == 'left':
                sense.show_message(menu[menu_item]['name'])
                sense.show_letter(menu[menu_item]['short_name'])
