sudo mkdir /usr/share/sysfetch 2>&1 /dev/null
sudo cp sysfetch /usr/local/bin 2>&1 /dev/null
sudo cp distros.py /usr/share/sysfetch 2>&1 /dev/null

mkdir $HOME/.sysfetch 2>&1 /dev/null
cp conf.json $HOME/.sysfetch 2>&1 /dev/null

echo "Succesful execution. Remeber to install the Python package \"psutil\" if you haven't already"
