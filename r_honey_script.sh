#! /bin/bash

case "$(pidof python HoneypotBase.py | wc -w)" in

0) echo "0"
  	authbind python HoneypotBase.py
	;;
1) echo "Honeypot Already Running";;
*) echo "more then one"
	kill $(pidof python HoneypotBase.py | awk '{print $1}')
	;;
esac

