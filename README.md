# Sense Hat Experiments
The sense-hat package should be installed on the Raspberry Pi: 
```sudo apt-get install sense-hat```.


## ip_menu.py
Script to show a menu to lookup ip-addresses on the Raspberry Pi.

Needs the netifaces module:
```pip install netifaces```.

To run the script on startup add it to your ```/etc/rc.local```, just above ```exit 0```.

```
# show ip addresses on the raspberry pi sense hat
sudo python /full/path/to/the/script/ip_menu.py &

exit 0
```

Because the script will be run as superuser, you also need to install netifaces for it ```sudo pip install netifaces```.
