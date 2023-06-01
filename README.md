# Sysfetch
Command-line system information tool written in Python.\
Features hardware and operative system centered information.

![sample.png](sample.png)

Inspired by Neofetch and PowerLevel10k

Currently still in beta-testing phase. Feel free to test the software and report any bad behaviour 

### Install 
To install sysfetch in your system, you need to execute "install.sh" file with root privilegies:

```commandline
$ ./install.sh
```

The script will create a folder called "sysfetch" in "/usr/share", and will copy "distros.py" into it. \
The "sysfetch" main script will be copied into "/usr/local/bin".

It is also required to have installed the package "psutil", 
which can be installed both by your distro's package manager or
by pip

```commandline
$ pip install psutil
```

### Usage

```commandline
$ sysfetch
```
To decrease execution time, Sysfetch implements a cacheing method, 
which locally stores all "static" data featured.

If you want data to be recached, in case you changed something in 
your device which concerns "static" data, simply use:

```commandline
$ sysfetch recache
```
It is a good practice to recache at least once a week.

If you desire to use a color different from default one (purple), 
you can change it by:

```commandline
$ sysfetch color aquagreen
```

Available colors:
- grey
- red
- yellow
- purple
- green
- lightblue
- blue
- orange
- aquagreen

To get help about usage, it is available the "--help" option:

```commandline
$ sysfetch --help
```


If you wish to set a personalised default behaviour, you can edit the configurartion file
located in "$HOME/.sysfetch/conf.json". Example configuration:

```json
{
  "ascii-art" : "Debian",
  "separator-unicode" : "debian",
  "default-color" : "aquagreen",
  "always-recache" : false
}
```

Leave blank if you want to keep the standard behaviour.

Once done with conf.json, to load your changes it is required to recache.

Available always-recache values:
- true
- false

Available separator unicode:
- alpine
- macos
- arch
- debian
- kali
- parrot
- endeavour
- raspbian
- manjaro
- centos
- opensuse
- redhat
- sabayon
- slackware
- mandriva
- mangeia
- devuan

Available colors:
- grey
- red
- yellow
- purple
- green
- lightblue
- blue
- orange
- aquagreen

Available ascii-art:
- AIX
- Alpine
- AlterLinux
- Anarchy
- Android
- Antergos
- antiX
- "AOSC OS"
- "AOSC OS/Retro"
- Apricity
- ArcoLinux
- ArchBox
- ARCHlabs
- ArchStrike
- XFerience
- ArchMerge
- Arch
- Artix
- Arya
- Bedrock
- Bitrig
- BlackArch
- BLAG
- BlankOn
- BlueLight
- bonsai
- BSD,BunsenLabs
- Calculate
- Carbs
- CentOS
- Chakra
- ChaletOS
- Chapeau
- Chrom
- Cleanjaro
- ClearOS
- Clear_Linux
- Clover
- Condres
- Container_Linux
- CRUX
- Cucumber
- Debian
- Deepin
- DesaOS
- Devuan
- DracOS
- DarkOs
- DragonFly
- Drauger
- Elementary
- EndeavourOS
- Endless
- EuroLinux
- Exherbo
- Fedora
- Feren
- FreeBSD
- FreeMiNT
- Frugalware
- Funtoo
- GalliumOS
- Garuda
- Gentoo
- Pentoo
- gNewSense
- GNOME
- GNU
- GoboLinux
- Grombyang
- Guix
- Haiku
- Huayra
- Hyperbola
- janus
- Kali
- KaOS
- KDE_neon
- Kibojoe
- Kogaion
- Korora
- KSLinux
- Kubuntu
- LEDE
- LFS
- Linux_Lite
- LMDE
- Lubuntu
- Lunar
- macos
- Mageia
- MagpieOS
- Mandriva
- Manjaro
- Maui
- Mer
- Minix
- LinuxMint
- MX_Linux
- Namib
- Neptune
- NetBSD
- Netrunner
- Nitrux
- NixOS
- Nurunner
- NuTyX
- OBRevenge
- OpenBSD
- openEuler
- OpenIndiana
- openmamba
- OpenMandriva
- OpenStage
- OpenWrt
- osmc
- Oracle
- OS Elbrus
- PacBSD
- Parabola
- Pardus
- Parrot
- Parsix
- TrueOS
- PCLinuxOS
- Peppermint
- popos
- Porteus
- PostMarketOS
- Proxmox
- Puppy
- PureOS
- Qubes
- Radix
- Raspbian
- Reborn_OS
- Redstar
- Redcore
- Redhat
- Refracted_Devuan
- Regata
- Rosa
- sabotage
- Sabayon
- Sailfish
- SalentOS
- Scientific
- Septor
- SereneLinux
- SharkLinux
- Siduction
- Slackware
- SliTaz
- SmartOS
- Solus
- Source_Mage
- Sparky
- Star
- SteamOS
- SunOS
- openSUSE_Leap
- openSUSE_Tumbleweed
- openSUSE
- SwagArch
- Tails
- Trisquel
- Ubuntu-Budgie
- Ubuntu-GNOME
- Ubuntu-MATE
- Ubuntu-Studio
- Ubuntu
- Venom
- Void
- Obarun
- windows10
- Windows7
- Xubuntu
- Zorin
- IRIX
    