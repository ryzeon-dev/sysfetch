#!/bin/bash

if [ "$1" == "--force" ]; then
  command="$2"
else
  command="$1"
fi

if [ "$(id -u)" == "0" ]; then
  if [ "$1" != "--force" ]; then
    echo "Please do not run this script as root"
    exit 1
  else
    echo "It is not suggested to run this script as root. Executing anyways"
  fi
fi

compile() {
  echo "Creating python virtual environment for compilation"

  python3 -m venv venv
  if [ "$?" != "0" ]; then
    echo "Python virtual environment creation failed: exiting"
    exit 1
  fi

  source ./venv/bin/activate

  echo "Installing dependencies via pip"
  pip install pyinstaller pyyaml &>> /dev/null
  if [ "$?" != "0" ]; then
    echo "Dependencies installation via pip failed: exiting"
    exit 1
  fi

  echo "Compiling..."
  pyinstaller --onefile ./src/sysfetch.py --name sysfetch &>> /dev/null
  if [ "$?" != "0" ]; then
    echo "Compilation failed: exiting"
    deactivate
    exit 1
  fi

  echo "Compilation terminated successfully"
	deactivate
}

clean() {
  echo "Removing installation files"
	rm -rf ./dist ./build ./sysfetch.spec ./venv &>> /dev/null
}

if [ -z "$command" ]; then
	echo -e "Sysfetch installation script"
	echo -e "./install.sh [--force] [OPTIONS]\n"
	echo -e "If \`--force\` flag is added, this script will allow running as \`root\`\n"
	echo -e "Options:"
	echo -e " full      Full installation: creates $HOME/.sysfetch directory and copies in it standard version of \`conf.yaml\`,"
	echo -e "           it also compiles and copies \`sysfetch\` in /usr/local/bin\n"
	echo -e " update    Only compiles and copies \`sysfetch\` in /usr/local/bin"
	exit 0

elif [ "$command" == "full" ]; then
  compile

  echo "Installing sysfetch binary"
  sudo cp ./dist/sysfetch /usr/local/bin
  if [ "$?" != "0" ]; then
    echo "Install failed: exiting"
    deactivate
    exit 1
  fi
  clean

	mkdir $HOME/.sysfetch &>> /dev/null
	cp conf.yaml $HOME/.sysfetch &>> /dev/null
	if [ "$?" != "0" ]; then
    echo "Standard configuration copying failed: exiting"
    deactivate
    exit 1
  fi

	echo "Succesful full installation"

elif [ "$command" == "update" ]; then
	compile

	echo "Installing sysfetch binary"
	sudo cp ./dist/sysfetch /usr/local/bin &>> /dev/null
	if [ "$?" != "0" ]; then
    echo "Install failed: exiting"
    deactivate
    exit 1
  fi
	clean

	echo "Succesful update"
fi
