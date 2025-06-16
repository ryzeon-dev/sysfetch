#!/usr/bin/python3

import sys
from subprocess import getoutput as terminal

if not 'android' in terminal('uname -a').lower():
    import psutil

import os
import json
import time

HOME = os.getenv('HOME')

import distros

def getConf():
    try:
        conf = json.load(open(f'{HOME}/.sysfetch/conf.json', 'r'))
        show = conf['show']

    except:
        print('Can\'t read conf.json, please execute "install.sh" script to install or update the software')
        sys.exit(0)

    else:
        return conf, show

unicodes = {
    'alpine': '\uF300',
    'macos': '\uF302',
    'arch': '\uF303',
    'debian': '\uF306',
    'kali': '\uF327',
    'parrot': '\uF329',
    'endeavour': '\uF322',
    'raspbian': '\uF315',
    'fedora' : '\uF30A',
    'manjaro': '\uF312',
    'centos': '\uF304',
    'opensuse': '\uF314',
    'redhat': '\uF316',
    'sabayon': '\uF317',
    'slackware': '\uF318',
    'mandriva': '\uF311',
    'mageia': '\uF310',
    'devuan': '\uF307',
    'tux' : '\uF31A',
    'android' : '\uF17B'
}

colors = {
    'grey': '90m',
    'red': '31m',
    'yellow': '93m',
    'purple': '95m',
    'green': '32m',
    'lightblue': '94m',
    'blue': '34m',
    'orange': '33m',
    'aquagreen': '96m'
}

def makeNew(ignoreConf=False):
    output = []
    cache = []

    asciiArt = 'tux'

    if 'android' in terminal('uname -a').lower():
        asciiArt = 'android'
        osname = 'android'

    else:
        osname = terminal('cat /etc/os-release | grep -w ID | awk -F \'=\' \'{ print $2 }\'').strip().lower()
        osSpecific = terminal('cat /etc/issue').strip().split(' ')[0].lower()

        if osSpecific in distros.distro.keys():
            asciiArt = osSpecific

        else:
            if osname in distros.distro.keys():
                asciiArt = osname

    if not ignoreConf and conf['ascii-art']:
        asciiArt = conf['ascii-art']

    asciiLogo = distros.distro[asciiArt][0]
    width = distros.distro[asciiArt][1]
    height = distros.distro[asciiArt][2]

    if not ignoreConf and conf['separator-unicode']:
        unicodeLogo = unicodes[conf['separator-unicode']]

    else:
        unicodeLogo = '\uF31A'
        if osname.lower() in unicodes.keys():
            unicodeLogo = unicodes[osname.lower()]

        else:
            try:
                osLike = terminal('cat /etc/os-release | grep -w ID_LIKE | awk -F \'=\' \'{ print $2 }\'')

            except:
                pass

            else:
                for key in unicodes:

                    if key.lower() in osLike.lower():
                        unicodeLogo = unicodes[key]

    try:
        sent = psutil.net_io_counters().bytes_sent
        recv = psutil.net_io_counters().bytes_recv
        written = psutil.disk_io_counters().write_bytes
        red = psutil.disk_io_counters().read_bytes
        before = time.time()
    except: pass

    colorUnicode = f'\x1b[1;{color}'
    colorUnicodeBold = f'\x1b[7;{color}'

    white = '\x1b[0m'
    indent = f'\x1b[{width}C'

    if not ('no-ascii-art' not in sys.argv and (ignoreConf or (not ignoreConf and not conf['no-ascii-art']))):
        indent = ''
        height = 0

    down = '\x1b[1B\x1b[9999D'
    downCount = 0

    output.append('{up}' + indent + '\x1b[1D' + colorUnicode + '' + white + f'{colorUnicodeBold} ' + terminal(
        'whoami') + f' {unicodeLogo} ' + terminal('uname -n') + ' ' + white + colorUnicode + '' + white + down)
    cache.append(
        '{up}' + indent + '\x1b[1D' + '{color_unicode}' + '' + white + '{color_unicode_bold} ' + '{username} ' +
        unicodeLogo + ' {hostname} ' + white + '{color_unicode}' + '' + white + down)

    downCount += 1
    down = '\n' if downCount >= height else down

    if ignoreConf or show['os']:
        if asciiArt == 'android':
            distro = 'Android'

        else:
            distro = terminal('cat /etc/issue')
            distro = distro[0:distro.index('\\')]
            distro = distro.split('\n')[0]

            if not distro.strip():
                distro = terminal('cat /etc/os-release | grep PRETTY_NAME | awk -F \'"\' \'{ print $2 }\'')

        output.append(indent + colorUnicode + 'os: ' + white + distro + down)
        cache.append(indent + '{color_unicode}' + 'os: ' + white + distro + down)

        downCount += 1
        down = '\n' if downCount >= height else down

    if ignoreConf or show['kernel']:
        kernel = terminal('uname -r')
        output.append(indent + colorUnicode + 'kernel: ' + white + kernel + down)
        cache.append(indent + '{color_unicode}' + 'kernel: ' + white + '{kernel}' + down)
        downCount += 1
        down = '\n' if downCount >= height else down

    if ignoreConf or show['shell']:
        shell = terminal('$SHELL --version').split('\n')[0]
        if 'not found' not in shell:
            output.append(indent + colorUnicode + 'shell: ' + white + shell + down)
            cache.append(indent + '{color_unicode}' + 'shell: ' + white + '{shell}' + down)
            downCount += 1
            down = '\n' if downCount >= height else down

    if ignoreConf or show['cpu']:
        cpu = terminal('cat /proc/cpuinfo | grep -m 1 "model name" | awk -F \':\' \'{ print $2 }\'').strip()
        if not cpu:
            cpu = terminal('lscpu | grep "Model name" -w | awk -F \':\' \'{ print $2 }\'').strip()
        output.append(indent + colorUnicode + 'cpu: ' + white + cpu + down)
        cache.append(indent + '{color_unicode}' + 'cpu: ' + white + cpu + down)
        downCount += 1
        down = '\n' if downCount >= height else down

        if ignoreConf or show['cpu-arch']:
            cpuarch = terminal('arch').strip()
            output.append(indent + colorUnicode + '    architecture: ' + white + cpuarch + down)
            cache.append(indent + '{color_unicode}' + '    architecture: ' + white + cpuarch + down)
            downCount += 1
            down = '\n' if downCount >= height else down

        if ignoreConf or show['cpu-cores']:
            cpuCores = terminal('cat /proc/cpuinfo | grep -m 1 cores | awk -F \':\' \'{ print $2 }\'').strip()

            output.append(indent + colorUnicode + '    cores: ' + white + cpuCores + down)
            cache.append(indent + '{color_unicode}' + '    cores: ' + white + cpuCores + down)
            downCount += 1
            down = '\n' if downCount >= height else down

        if ignoreConf or show['cpu-threads']:
            cpuThreads = terminal('cat /proc/cpuinfo | grep -c processor').strip()
            if 'not found' not in cpuThreads:   
                output.append(indent + colorUnicode + '    threads: ' + white + cpuThreads + down)
                cache.append(indent + '{color_unicode}' + '    threads: ' + white + cpuThreads + down)
                downCount += 1
                down = '\n' if downCount >= height else down

        if ignoreConf or show['cpu-usage']:
            try:
                cpuUsage = str(psutil.cpu_percent()) + '%'
                output.append(indent + colorUnicode + '    usage: ' + white + cpuUsage + down)
                cache.append(indent + '{color_unicode}' + '    usage: ' + white + '{cpu_usage}' + down)
                downCount += 1
                down = '\n' if downCount >= height else down

            except:
                pass

        if ignoreConf or show['cpu-temp']:
            try:
                temps = psutil.sensors_temperatures()
                keys = list(temps.keys())

                key = keys[0]
                if 'coretemp' in keys:
                    key = 'coretemp'

                elif 'k10temp' in keys:
                    key = 'k10temp'

                cpuTemp = str(temps[key][0].current) + ' C'
                output.append(indent + colorUnicode + '    temperature: ' + white + cpuTemp + down)
                cache.append(indent + '{color_unicode}' + '    temperature: ' + white + '{cpu_temperature}' + down)
                downCount += 1
                down = '\n' if downCount >= height else down

            except:
                pass

    if ignoreConf or show['load']:
        load = terminal('uptime | awk -F \'load average: \' \'{ print $2 }\' | awk -F \', \' \'{ print $1 }\'').strip()
        if not 'not found' in load:
            output.append(indent + colorUnicode + 'system load: ' + white + load + down)
            cache.append(indent + '{color_unicode}' + 'system load: ' + white + '{load}' + down)
            downCount += 1
            down = '\n' if downCount >= height else down

    if ignoreConf or show['ram']:
        ram = terminal('cat /proc/meminfo | grep MemTotal | awk \'{ printf "%.2f", $2 / 1024 / 1024 }\'')+ ' GB'
        output.append(indent + colorUnicode + 'ram: ' + white + ram + down)
        cache.append(indent + '{color_unicode}' + 'ram: ' + white + ram + down)
        downCount += 1
        down = '\n' if downCount >= height else down

        if ignoreConf or show['ram-usage']:
            ramUsage = terminal('echo $(cat /proc/meminfo | grep MemTotal | awk \'{ print $2 }\' && cat /proc/meminfo |'
                                ' grep MemAvailable | awk \'{ print $2 }\') | awk \'{ printf \"%d %s (%.2f GB)\", ($1 - $2) *'
                                ' 100 / $1, "%", ($1 -$2) / 1024 / 1024 }\'')
            output.append(indent + colorUnicode + '    usage: ' + white + ramUsage + down)
            cache.append(indent + '{color_unicode}' + '    usage: ' + white + '{ram_usage}' + down)
            downCount += 1
            down = '\n' if downCount >= height else down

        if ignoreConf or show['ram-cached']:
            ramCached = terminal('cat /proc/meminfo | grep -m 1 "Cached" | awk  \'{ printf "%.2f MB", $2 / 1024}\'').strip()
            output.append(indent + colorUnicode + '    cached: ' + white + ramCached + down)
            cache.append(indent + '{color_unicode}' + '    cached: ' + white + '{ram_cached}' + down)
            downCount += 1
            down = '\n' if downCount >= height else down

    if ignoreConf or show['swap']:
        swap = terminal('cat /proc/meminfo | grep "SwapTotal" | awk \'{ printf "%.2f", $2 / 1024 / 1024 }\'') + ' GB'
        output.append(indent + colorUnicode + 'swap: ' + white + swap + down)
        cache.append(indent + '{color_unicode}' + 'swap: ' + white + swap + down)
        downCount += 1
        down = '\n' if downCount >= height else down

        if ignoreConf or show['swap-usage']:
            swapUsage = terminal('echo $(cat /proc/meminfo | grep SwapTotal | awk \'{ print $2 }\' && cat /proc/meminfo | '
                                 'grep SwapFree | awk \'{ print $2 }\') | awk \'{ printf "%d%s (%.2f GB)", $1 ? ($1 - $2) * 100'
                                 ' / $1 : 0, "%", ($1 -$2) / 1024 / 1024 }\'')
            output.append(indent + colorUnicode + '    usage: ' + white + swapUsage + down)
            cache.append(indent + '{color_unicode}' + '    usage: ' + white + '{swap_usage}' + down)
            downCount += 1
            down = '\n' if downCount >= height else down

        if ignoreConf or show['swap-cached']:
            swapCached = terminal('cat /proc/meminfo | grep SwapCached | awk \'{ printf "%2.f", $2 / 1024 }\'').strip() + ' MB'
            output.append(indent + colorUnicode + '    cached: ' + white + swapCached + down)
            cache.append(indent + '{color_unicode}' + '    cached: ' + white + '{swap_cached}' + down)
            downCount += 1
            down = '\n' if downCount >= height else down

    if ignoreConf or show['storage']:
        try:
            totalStorage = terminal('df -lh /home | grep /home -w | awk \'{ print $2 }\'')
            if not totalStorage:
                totalStorage = terminal('df -lh / | grep / -w | awk \'{ print $2 }\'')

            output.append(indent + colorUnicode + 'storage: ' + white + totalStorage + down)
            cache.append(indent + '{color_unicode}' + 'storage: ' + white + totalStorage + down)

            downCount += 1
            down = '\n' if downCount >= height else down

        except: pass

        if ignoreConf or show['storage-usage']:
            try:
                usedStorage = terminal('df -lh /home | grep /home -w | awk \'{ printf "%s (%s)", $5, $3 }\'')
                if not usedStorage:
                    usedStorage = terminal('df -lh / | grep / -w | awk \'{ printf "%s (%s)", $5, $3 }\'')

                if not 'not found' in usedStorage:
                    output.append(indent + colorUnicode + '    usage: ' + white + usedStorage + down)
                    cache.append(indent + '{color_unicode}' + '    usage: ' + white + '{used_storage}' + down)
                    downCount += 1
                    down = '\n' if downCount >= height else down

            except: pass

    if ignoreConf or show['gpu']:
        gpu = terminal("lspci | grep VGA | awk -F 'controller:' '{ print $2 }'").strip()
        if not 'not found' in gpu and not 'pcilib' in gpu and gpu:
            output.append(indent + colorUnicode + 'gpu: ' + white + gpu + down)
            cache.append(indent + '{color_unicode}' + 'gpu: ' + white + gpu + down)
            downCount += 1
            down = '\n' if downCount >= height else down

    if ignoreConf or show['processes']:
        processes = str(len(terminal('ps axu').split('\n')) - 1)
        output.append(indent + colorUnicode + 'processes: ' + white + processes + down)
        cache.append(indent + '{color_unicode}' + 'processes: ' + white + '{processes}' + down)
        downCount += 1
        down = '\n' if downCount >= height else down

    if ignoreConf or show['ipv4']:
        ipv4 = terminal('echo $(ip a | grep inet -w | awk \'{ print $2 }\')')

        if not 'invalid' in ipv4 and not 'not found' in ipv4:
            output.append(indent + colorUnicode + 'ipv4: ' + white + ipv4 + down)
            cache.append(indent + '{color_unicode}' + 'ipv4: ' + white + '{ipv4}' + down)
            downCount += 1
            down = '\n' if downCount >= height else down

    try:
        now = time.time()
        sentNow = psutil.net_io_counters().bytes_sent
        recvNow = psutil.net_io_counters().bytes_recv
        writtenNow = psutil.disk_io_counters().write_bytes
        redNow = psutil.disk_io_counters().read_bytes

    except:
        pass

    else:
        if ignoreConf or show['network-speed']:
            output.append(indent + colorUnicode + 'network speed: ' + white + down)
            cache.append(indent + colorUnicode + 'network speed: ' + white + down)
            downCount += 1
            down = '\n' if downCount >= height else down

            if ignoreConf or show['upload-speed']:
                output.append(
                    indent + colorUnicode + '    upload: ' + white + str(round((sentNow-sent) / (now - before) / 1024, 2)) +
                    ' kBps' + down)
                cache.append(
                    indent + colorUnicode + '    upload: ' + white + '{upload}' + ' kBps' + down)
                downCount += 1
                down = '\n' if downCount >= height else down

            if ignoreConf or show['download-speed']:
                output.append(
                    indent + colorUnicode + '    download: ' + white + str(round((recvNow - recv) / (now - before) / 1024, 2))
                    + ' kBps' + down)
                cache.append(
                    indent + colorUnicode + '    download: ' + white + '{download}' + ' kBps' + down)
                downCount += 1
                down = '\n' if downCount >= height else down

        if ignoreConf or show['disk-speed']:
            output.append(indent + colorUnicode + 'disk speed: ' + white + down)
            cache.append(indent + colorUnicode + 'disk speed: ' + white + down)
            downCount += 1
            down = '\n' if downCount >= height else down

            if ignoreConf or show['writing-speed']:
                output.append(
                    indent + colorUnicode + '    writing: ' + white + str(round((writtenNow - written) /
                    (now - before) / 1024, 2)) + ' kBps' + down)
                cache.append(
                    indent + colorUnicode + '    writing: ' + white + '{writing}' + ' kBps' + down)
                downCount += 1
                down = '\n' if downCount >= height else down

            if ignoreConf or show['reading-speed']:
                output.append(
                    indent + colorUnicode + '    reading: ' + white + str(round((redNow - red) / (now - before) / 1024, 2)) +
                    ' kBps' + down)
                cache.append(
                    indent + colorUnicode + '    reading: ' + white + '{reading}' + ' kBps' + down)
                downCount += 1
                down = '\n' if downCount >= height else down

    output.append('{end}')
    cache.append('{end}')

    lines = len(output)

    up = f'\x1b[{height-1}A\x1b[999D'
    if height - lines < 0:
        end = ''
    else:
        end = f'\x1b[9999D\x1b[{height - lines}B'

    showAsciiArt = 'no-ascii-art' not in sys.argv and (ignoreConf or (not ignoreConf and not conf['no-ascii-art']))

    if not showAsciiArt:
        up = ''
        end = ''

    output[0] = output[0].replace('{up}', up)
    cache[0] = cache[0].replace('{up}', up)

    if showAsciiArt:
        output.insert(0, colorUnicode + asciiLogo.replace('\x1b[?7l', '').replace('\x1b[?25l', '') + white)
        cache.insert(0, colorUnicode + asciiLogo.replace('\x1b[?7l', '').replace('\x1b[?25l', '') + white)

    output[-1] = output[-1].replace('{end}', end)
    cache[-1] = cache[-1].replace('{end}', end)

    if showAsciiArt:
        print('')

    print(''.join(output))

    with open(HOME + '/.sysfetch/sysfetch.cache', 'w') as file:
        file.write(''.join(cache))


def printCached(color):
    with open(HOME + '/.sysfetch/sysfetch.cache', 'r') as cache:

        try:
            sent = psutil.net_io_counters().bytes_sent
            recv = psutil.net_io_counters().bytes_recv

            written = psutil.disk_io_counters().write_bytes
            red = psutil.disk_io_counters().read_bytes
            before = time.time()
        except:
            pass

        content = cache.read()

        if conf['default-color']:
            color = colors[conf['default-color']]

        colorUnicode = f'\x1b[1;{color}'
        colorUnicodeBold = f'\x1b[7;{color}'

        content = content.replace('{username}', terminal('whoami'))
        content = content.replace('{hostname}', terminal('uname -n'))
        content = content.replace('{color_unicode}', colorUnicode)
        content = content.replace('{color_unicode_bold}', colorUnicodeBold)

        if show['kernel']:
            content = content.replace('{kernel}', terminal('uname -r'))

        if ignoreConf or  show['shell']:
            content = content.replace('{shell}', terminal('$SHELL --version').split('\n')[0])

        if  show['cpu'] and show['cpu-usage']:
            try:
                content = content.replace('{cpu_usage}', str(psutil.cpu_percent()) + '%')
            except: pass

        if show['cpu'] and show['cpu-temp']:
            try:
                temps = psutil.sensors_temperatures()
                keys = list(temps.keys())

                key = keys[0]
                if 'coretemp' in keys:
                    key = 'coretemp'

                elif 'k10temp' in keys:
                    key = 'k10temp'

                cpuTemp = str(temps[key][0].current) + ' C'
                content = content.replace('{cpu_temperature}', cpuTemp)
            except: pass

        if show['load']:
            try: content = content.replace('{load}', terminal('uptime | awk -F \'load average: \' \'{ print $2 }\' | '
                                                              'awk -F \', \' \'{ print $1 }\'').strip())
            except: pass

        if show['ram'] and show['ram-usage']:
            try:
                content = content.replace('{ram_usage}', terminal('echo $(cat /proc/meminfo | grep MemTotal |'
                                          ' awk \'{ print $2 }\' && cat /proc/meminfo | grep MemAvailable | '
                                          'awk \'{ print $2 }\') | awk \'{ printf \"%d%s (%.2f GB)\", ($1 - $2) * 100 '
                                          '/ $1, "%", ($1 -$2) / 1024 / 1024 }\''))
            except: pass

        if show['ram'] and show['ram-cached']:
            try:
                content = content.replace('{ram_cached}', terminal(
                    'cat /proc/meminfo | grep -m 1 "Cached" | awk  \'{ printf "%.2f MB", $2 / 1024}\'').strip())
            except: pass

        if show['swap'] and show['swap-usage']:
            try:
                content = content.replace('{swap_usage}', terminal('echo $(cat /proc/meminfo | grep SwapTotal | '
                                          'awk \'{ print $2 }\' && cat /proc/meminfo | grep SwapFree | awk \'{ print $2 }\')'
                                          ' | awk \'{ printf "%d%s (%.2f GB)", $1 ? ($1 - $2) * 100 / $1 : 0, "%", ($1 -$2) '
                                          '/ 1024 / 1024 }\''))
            except: pass

        if show['swap'] and show['swap-cached']:
            try:
                content = content.replace('{swap_cached}', terminal(
                   'cat /proc/meminfo | grep SwapCached | awk \'{ printf "%.2f", $2 / 1024 }\'').strip() + ' MB')
            except: pass

        if show['storage'] and show['storage-usage']:
            usedStorage = terminal('df -lh /home | grep /home -w | awk \'{ printf "%s (%s)", $5, $3 }\'')
            if not usedStorage:
                usedStorage = terminal('df -lh / | grep / -w | awk \'{ printf "%s (%s)", $5, $3 }\'')

            try:
                content = content.replace('{used_storage}', usedStorage)
            except: pass

        if show['processes']:
            content = content.replace('{processes}', str(len(terminal('ps axu').split('\n')) - 1))

        if show['ipv4']:
            content = content.replace('{ipv4}', terminal('echo $(ip a | grep inet -w | awk \'{ print $2 }\' | awk -F \'/\' \'{ print $1 }\') | awk -F \'127.0.0.1 \' \'{ print $2 }\''))

        try:
            now = time.time()
            sentNow = psutil.net_io_counters().bytes_sent
            recvNow = psutil.net_io_counters().bytes_recv
            writtenNow = psutil.disk_io_counters().write_bytes
            redNow = psutil.disk_io_counters().read_bytes

        except:
            pass

        else:
            if show['network-speed'] and show['upload-speed']:
                content = content.replace('{upload}', str(round((sentNow - sent) / (now - before) / 1024, 2)))

            if show['network-speed'] and show['upload-speed']:
                content = content.replace('{download}', str(round((recvNow - recv) / (now - before) / 1024, 2)))

            if show['disk-speed'] and show['writing-speed']:
                content = content.replace('{writing}', str(round((writtenNow - written) / (now - before) / 1024, 2)))

            if show['disk-speed'] and show['reading-speed']:
                content = content.replace('{reading}', str(round((redNow - red) / (now - before) / 1024, 2)))

        print('')
        sys.stdout.write(content)
        print('')


if __name__ == '__main__':
    color = colors['aquagreen']

    if not 'ignore-conf' in sys.argv:
        ignoreConf = False
        conf, show = getConf()
        if conf['default-color']:
            color = colors[conf['default-color']]
    else:
        ignoreConf = True

    if not '.sysfetch' in os.listdir(HOME):
        terminal(f'mkdir  {HOME}/.sysfetch')

    if len(sys.argv) == 1:
        if 'sysfetch.cache' in os.listdir(HOME + '/.sysfetch') and (ignoreConf or not conf['always-recache']):
            printCached(color)

        else:
            makeNew(ignoreConf)

    else:
        if '--help' in sys.argv or '-h' in sys.argv:
            print('''sysfetch [options] [arguments]

Command line system information tool written in Python

Options:
    recache             makes new cache file updating all static data 
    color               allows to set the color of the text output
    no-ascii-art        output information only, no distro ascii art (requires recache)
    ignore-conf         ignores conf.json file and follows standard behaviour (requires recache)
    --help, -h          show this message and exit

Colors:
    red, yellow, grey, purple, green, lightblue, blue, orange, aquagreen (default)
   
To set a standard behaviuor, edit the file "conf.json" located in $HOME/.sysfetch/conf.json
For an example configutation, check at https://github.com/cpy-dev/sysfetch
            ''')
            sys.exit(0)
        
        if 'color' in sys.argv:
            try:
                colorIndex = sys.argv.index('color') + 1

            except:
                print('Error: A color must be given after "color" paramter')
                sys.exit(0)

            else:
                choosenColor = sys.argv[colorIndex]
                if choosenColor in colors.keys():
                    color = colors[sys.argv[colorIndex]]

                else:
                    print(f'Error: "{choosenColor}" is not in the color list')
                    sys.exit(0)


        if 'recache' in sys.argv or 'no-ascii-art' in sys.argv or ignoreConf or conf['always-recache']:
            makeNew(ignoreConf)
            
        else:
            printCached(color)