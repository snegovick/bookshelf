#!/bin/bash

if [ -f ./app.pid ]
then
	kill $(cat ./app.pid)
	rm ./app.pid
	sleep 1
fi
gunicorn -b 127.0.0.1:40020 app:app -D --pid ./app.pid #--daemon
