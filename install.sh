sudo mkdir /usr/share/sysfetch &>> /dev/null
sudo cp sysfetch /usr/local/bin &>> /dev/null
sudo cp distros.py /usr/share/sysfetch &>> /dev/null

mkdir $HOME/.sysfetch &>> /dev/null
cp conf.json $HOME/.sysfetch &>> /dev/null

echo "Succesful execution. Remeber to install the Python package \"psutil\" if you haven't already"