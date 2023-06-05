if [ "$(whoami)" != "root" ]; then
  echo "This script must be executed as super-user"
  exit 0
fi

mkdir /usr/share/sysfetch &>> /dev/null
mkdir $HOME/.sysfetch &>> /dev/null

cp conf.json $HOME/.sysfetch &>> /dev/null
cp sysfetch /usr/local/bin &>> /dev/null
cp distros.py /usr/share/sysfetch &>> /dev/null

echo "Succesful execution. Remeber to install the Python package \"psutil\" if you haven't already"