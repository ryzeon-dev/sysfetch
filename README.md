# Sysfetch
Command-line system information tool written in Python.\
Features hardware and operative system centered information.

Inspired by Neofetch and PowerLevel10k

Currently still in beta-testing phase. Feel free to test the software and report any bad behaviour 

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

### Example:
![example.png](example.png)