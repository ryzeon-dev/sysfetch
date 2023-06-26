#!/bin/bash

if [ -z "$1" ]; then
	echo -e "Sysfetch installation script\n"
	echo -e "./install.sh OPTION\n"
	echo -e "Options:"
	echo -e "	full			Full installation: creates /$HOME/.sysfetch directory and copies in it standard version of \"conf.json\"," 
	echo -e "    				it also copies the \"sysfetch\" script in /usr/local/bin\n"
	echo -e "	update 			Only copies \"sysfetch\" script in /usr/local/bin"
	exit 0

elif [ "$1" == "full" ]; then
	sudo mkdir /usr/share/sysfetch &>> /dev/null
	sudo cp sysfetch /usr/local/bin &>> /dev/null
	sudo cp distros.py /usr/share/sysfetch &>> /dev/null	

	mkdir $HOME/.sysfetch &>> /dev/null
	cp conf.json $HOME/.sysfetch &>> /dev/null

	echo "Succesful full installation. Remeber to install the Python package \"psutil\" if you haven't already"

elif [ "$1" == "update" ]; then
	sudo cp sysfetch /usr/local/bin &>> /dev/null
	echo "Succesful update"
fi
