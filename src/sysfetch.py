from subprocess import getoutput as terminal
import os
import yaml

import sysutil
import distros

HOME = os.getenv('HOME')
USER = os.getenv('USER')
HOST = terminal('uname -n')

def getConf():
    return yaml.load(open(os.path.join(HOME, '.sysfetch', 'conf.yaml'), 'r'), Loader=yaml.FullLoader)

UNICODES = {
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

COLORS = {
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

def grep(text='', filePath='', pattern='', onlyFirst=False, start=False):
    if not text:
        if not filePath:
            return None

        with open(filePath, 'r') as file:
            text = file.read()

    matches = []
    for line in text.split('\n'):
        if start:
            condition = line.startswith(pattern)
        else:
            condition = pattern in line

        if condition:
            if onlyFirst:
                return line
            matches.append(line)

    return matches

class Sysfetch:
    def __init__(self, color, asciiArtInfo):
        self.output = []

        self.asciiArt = asciiArtInfo[0]
        self.asciiArtWidth = asciiArtInfo[1]
        self.asciiArtHeight = asciiArtInfo[2]

        self.color = color
        self.colorUnicode = f'\x1b[1;{self.color}'
        self.colorUnicodeBold = f'\x1b[7;{self.color}'

        self.white = '\x1b[0m'
        self.indent = f'\x1b[{self.asciiArtWidth}C'

        self.up = f'\x1b[{self.asciiArtHeight-1}A\x1b[9999D'
        self.down = f'\x1b[1B\x1b[9999D'

        self.downCount = 1
        self.output.append(self.asciiArt + self.white)

    def appendFmtLines(self, title, value):
        self.output.append(
            self.indent + self.colorUnicode + title + ': ' + self.white + str(value) + self.down
        )

        self.downCount += 1
        self.down = '\n' if self.downCount >= self.asciiArtHeight else self.down


def makeNew(conf={}, ignoreConf=False):
    if 'android' in terminal('uname -a').lower():
        distroName = 'android'
        asciiArtInfo = distros.distro[distroName]
        unicodeLogo = UNICODES[distroName]
        prettyName = 'Android'

    else:
        distroId = grep(filePath='/etc/os-release', pattern='ID=', onlyFirst=True, start=True)
        distroName = distroId.replace('ID=', '')

        prettyName = grep(filePath='/etc/os-release', pattern='PRETTY_NAME=', onlyFirst=True)
        prettyName = prettyName.replace('PRETTY_NAME=', '').replace('"', '')

        unicodeLogo = UNICODES.get(distroName)
        if unicodeLogo is None:
            unicodeLogo = UNICODES['tux']

        asciiArtInfo = distros.distro.get(distroName)
        if asciiArtInfo is None:
            asciiArtInfo = distros.distro['tux']

    color = COLORS['aquagreen']

    if (asciiArtName := conf.get('ascii-art')) != 'default':
        asciiArtInfo = distros.distro[asciiArtName]

    if (confColor := conf.get('color')) != 'default':
        color = COLORS.get(confColor)

    if (confUnicodeLogo := conf.get('unicode-logo')) != 'default':
        unicodeLogo = UNICODES[confUnicodeLogo]

    sysfetch = Sysfetch(color=color, asciiArtInfo=asciiArtInfo)

    firstOutputLine = sysfetch.up + sysfetch.indent + sysfetch.colorUnicode + '' + sysfetch.white + sysfetch.colorUnicodeBold + ' ' +  USER + ' ' + unicodeLogo + ' ' + HOST + ' ' + sysfetch.white + sysfetch.colorUnicode + '' + sysfetch.white + sysfetch.down

    sysfetch.output.append(firstOutputLine)

    sysfetch.downCount += 1
    sysfetch.down = '\n' if sysfetch.downCount >= sysfetch.asciiArtHeight else sysfetch.down

    if ignoreConf or conf.get('os'):
        sysfetch.appendFmtLines('os', prettyName)

    if ignoreConf or conf.get('kernel'):
        kernelName = terminal('uname -r')
        sysfetch.appendFmtLines('kernel', kernelName)

    if ignoreConf or conf.get('shell'):
        shellVersion = terminal('$SHELL --version').split('\n')[0]
        sysfetch.appendFmtLines('shell', shellVersion)

    if ignoreConf or conf.get('cpu'):
        cpuInfo = sysutil.cpuInfo()
        sysfetch.appendFmtLines('cpu', cpuInfo.modelName)

        if ignoreConf or conf.get('cpu-arch'):
            sysfetch.appendFmtLines('    architecture', cpuInfo.architecture)

        if ignoreConf or conf.get('cpu-cores'):
            sysfetch.appendFmtLines('    cores', cpuInfo.cores)

        if ignoreConf or conf.get('cpu-threads'):
            sysfetch.appendFmtLines('    threads', cpuInfo.threads)

        if ignoreConf or conf.get('cpu-usage'):
            cpuUsage = sysutil.cpuUsage()
            sysfetch.appendFmtLines('    usage', str(round(cpuUsage.average.total, 2)) + '%')

        if ignoreConf or conf.get('cpu-temp'):
            sensors = sysutil.temperatureSensors()
            if len(sensors) > 0:
                cpuTempSensor = None

                for sensor in sensors:
                    if sensor.label in ('coretemp', 'k10temp'):
                        cpuTempSensor = sensor
                        break

                if cpuTempSensor is None:
                    cpuTempSensor = sensors[0]

                sysfetch.appendFmtLines('    temperature', str(cpuTempSensor.temperature) + ' C')

    if ignoreConf or conf.get('load'):
        load = sysutil.getLoad()
        sysfetch.appendFmtLines('load', load.oneMinute)
    
    if ignoreConf or conf.get('ram'):
        ramSize = sysutil.ramSize()
        fmtRamSize = ramSize.fmt(2)
        sysfetch.appendFmtLines('ram', fmtRamSize)

        if ignoreConf or conf.get('ram-usage'):
            ramUsagePercent = sysutil.ramUsagePercent()
            fmtRamUsageBytes = sysutil.ByteSize(ramUsagePercent * ramSize.b() / 100).fmt(2)
            fmtRamUsage = f'{round(ramUsagePercent, 2)}% ({fmtRamUsageBytes})'

            sysfetch.appendFmtLines('    usage', fmtRamUsage)

        if ignoreConf or conf.get('ram-cached'):
            ramCached = sysutil.ramCached()
            fmtRamCached = ramCached.fmt(2)

            sysfetch.appendFmtLines('    cached', fmtRamCached)

    if ignoreConf or conf.get('swap'):
        swap = sysutil.swapSize().fmt(2)
        sysfetch.appendFmtLines('swap', swap)

        if ignoreConf or conf.get('swap-usage'):
            swapUsage = sysutil.swapUsagePercent()
            sysfetch.appendFmtLines('    usage', str(round(swapUsage, 2)) + '%')

        if ignoreConf or conf.get('swap-cached'):
            cachedSwap = sysutil.swapCached()
            fmtSwapCached = cachedSwap.fmt(2)

            sysfetch.appendFmtLines('    cached', fmtSwapCached)

    if ignoreConf or conf.get('gpu'):
        gpuName = terminal("lspci | grep VGA | awk -F 'controller:' '{ print $2 }'").strip().replace('\n', ', ')
        sysfetch.appendFmtLines('gpu', gpuName)

    if ignoreConf or conf.get('motherboard'):
        mobo = sysutil.motherboardInfo()
        sysfetch.appendFmtLines('motherboard', mobo.name)

        if ignoreConf or conf.get('motherboard-vendor'):
            sysfetch.appendFmtLines('    vendor', mobo.vendor)

        if ignoreConf or conf.get('motherboard-version'):
            sysfetch.appendFmtLines('    version', mobo.version)

        if ignoreConf or conf.get('motherboard-bios'):
            sysfetch.appendFmtLines('    bios', f'{mobo.bios.vendor} {mobo.bios.release}')

    if ignoreConf or conf.get('processes'):
        processes = str(len(terminal('ps axu').split('\n')) - 1)
        sysfetch.appendFmtLines('processes', processes)

    if ignoreConf or conf.get('ipv4'):
        ipAddresses = sysutil.getIPv4()
        fmtIpAddresses = []

        for ip in ipAddresses:
            if ip.address:
                fmtIpAddresses.append(f'{ip.address}/{ip.cidr}')

        sysfetch.appendFmtLines('ipv4', ', '.join(fmtIpAddresses))

    if ignoreConf or conf.get('net-rate'):
        netRate = sysutil.networkRate()
        sysfetch.appendFmtLines('network rate', '')

        sysfetch.appendFmtLines('    upload', str(round(netRate.upload / 1024, 2)) + ' kiB/s')
        sysfetch.appendFmtLines('    download', str(round(netRate.download / 1024, 2)) + ' kiB/s')

    return sysfetch

if __name__ == '__main__':
    import sys

    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print(f'sysfetch: Command line system information tool written in python')
        print('usage: sysfetch [OPTIONS] [FLAGS]')
        print('options:')
        print('    ignore-conf    Ignore configuration file and continue execution')
        print('flags:')
        print('    --help -h      Show this message and exit')
        print('To edit sysfetch behaviour, edit the file located at ~/.sysfetch/conf.yaml')
        exit(0)

    ignoreConf = False
    if 'ignore-conf' in args:
        ignoreConf = True

    try:
        conf = getConf()

    except:
        ignoreConf = True

    sysfetch = makeNew(conf=conf, ignoreConf=ignoreConf)

    for line in sysfetch.output:
        print(line, end='')

    print()