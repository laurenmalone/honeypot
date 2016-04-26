#! /bin/bash

case "$(pidof node server.js | wc -w)" in

0) echo "0"
  	authbind node server.js
	;;
1) echo "Server Already Running";;
*) echo "more then one"
	kill $(pidof node server.js | awk '{print $1}')
	;;
esac