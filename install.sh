#!/bin/bash

if [ "$(id -u)" == "0" ]; then
  echo "Please do not run this script as root"
fi

compile() {
  python3 -m venv venv
  source ./venv/bin/activate

  pip install pyinstaller psutil
  pyinstaller --onefile ./src/sysfetch.py --name sysfetch

	deactivate
}

clean() {
	rm -rf ./dist ./build ./sysfetch.spec
}

if [ -z "$1" ]; then
	echo -e "Sysfetch installation script\n"
	echo -e "./install.sh OPTION\n"
	echo -e "Options:"
	echo -e "	full			Full installation: creates /$HOME/.sysfetch directory and copies in it standard version of \"conf.json\"," 
	echo -e "    				it also compiles and copies \"sysfetch\" in /usr/local/bin\n"
	echo -e "	update 		Only compiles and copies \"sysfetch\" in /usr/local/bin"
	exit 0

elif [ "$1" == "full" ]; then
  compile
  sudo cp ./dist/sysfetch /usr/local/bin
  clean

	mkdir $HOME/.sysfetch &>> /dev/null
	cp conf.json $HOME/.sysfetch &>> /dev/null

	echo "Succesful full installation"

elif [ "$1" == "update" ]; then
	compile
	sudo cp ./dist/sysfetch /usr/local/bin
	clean

	echo "Succesful update"
fi
