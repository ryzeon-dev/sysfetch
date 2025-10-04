'''
THIS FILE COMES FROM `sysutil-lib` package written by ryzeon-dev (me)
This is a slightly modified version
'''

import dataclasses
import os
import sys
import time


class BatteryStatus:
    Charging = 'charging'
    Discharging = 'discharging'
    Full = 'full'


@dataclasses.dataclass
class Battery:
    capacity: int
    status: str


@dataclasses.dataclass
class ProcessorUsage:
    total: float
    user: float
    nice: float
    system: float
    idle: float
    iowait: float
    interrupt: float
    soft_interrupt: float


@dataclasses.dataclass
class CpuUsage:
    average: ProcessorUsage
    processors: [ProcessorUsage]


@dataclasses.dataclass
class NetworkRate:
    download: float
    upload: float


@dataclasses.dataclass
class TemperatureSensor:
    label: str
    temperature: float


@dataclasses.dataclass
class CpuInfo:
    modelName: str
    cores: int
    threads: int
    dies: int
    governors: [str]
    maxFrequencyMHz: float
    clockBoost: bool
    architecture: str
    byteOrder: str


@dataclasses.dataclass
class SchedulerPolicy:
    name: str
    scalingGovernor: str
    scalingDriver: str
    minimumScalingMHz: float
    maximumScalingMHz: float


@dataclasses.dataclass
class Frequency:
    _khz: float

    def khz(self):
        return self._khz

    def mhz(self):
        return self._khz / 1000

    def ghz(self):
        return self._khz / 1000_000


@dataclasses.dataclass
class ProcessorFrequency:
    processorID: str
    frequency: Frequency


@dataclasses.dataclass
class CPU:
    info: CpuInfo
    averageUsage: ProcessorUsage
    perProcessorUsage: [ProcessorUsage]
    schedulerPolicies: [SchedulerPolicy]
    averageFrequency: Frequency
    perProcessorFrequency: [ProcessorFrequency]

    def __init__(self):
        self.info = cpuInfo()

        usage = cpuUsage()
        self.averageUsage = usage.average
        self.perProcessorUsage = usage.processors

        self.schedulerPolicies = schedulerInfo()

        frequency = cpuFrequency()
        self.averageFrequency = frequency.average
        self.perProcessorFrequency = cpuFrequency().processors

    def update(self):
        usage = cpuUsage()
        self.averageUsage = usage.average
        self.perProcessorUsage = usage.processors
        self.schedulerPolicies = schedulerInfo()


@dataclasses.dataclass
class RamSize:
    gb: float
    gib: float


@dataclasses.dataclass
class VramSize:
    gb: float
    gib: float


class RouteType:
    TCP = 'tcp'
    TCP6 = 'tcp6'
    UDP = 'udp'
    UDP6 = 'udp6'


class RouteStatus:
    ESTABLISHED = 'established'
    SYN_SENT = 'syn sent'
    SYN_RECEIVED = 'syn received'
    FIN_WAIT1 = 'fin wait 1'
    FIN_WAIT2 = 'fin wait 2'
    TIME_WAIT = 'time wait'
    CLOSED = 'closed'
    CLOSE_WAIT = 'close wait'
    LAST_ACKNOWLEDGEMENT = 'last acknowledgement'
    LISTENING = 'listening'
    CLOSING = 'closing'
    NEW_SYN_RECEIVED = 'new syn received'

    @staticmethod
    def fromTcpCode(code):
        if code == '01':
            return RouteStatus.ESTABLISHED

        elif code == '02':
            return RouteStatus.SYN_SENT

        elif code == '03':
            return RouteStatus.SYN_RECEIVED

        elif code == '04':
            return RouteStatus.FIN_WAIT1

        elif code == '05':
            return RouteStatus.FIN_WAIT2

        elif code == '06':
            return RouteStatus.TIME_WAIT

        elif code == '07':
            return RouteStatus.CLOSED

        elif code == '08':
            return RouteStatus.CLOSE_WAIT

        elif code == '09':
            return RouteStatus.LAST_ACKNOWLEDGEMENT

        elif code == '0A':
            return RouteStatus.LISTENING

        elif code == '0B':
            return RouteStatus.CLOSING

        elif code == '0C':
            return RouteStatus.NEW_SYN_RECEIVED


@dataclasses.dataclass
class NetworkRoute:
    routeType: str
    localAddress: str
    localPort: int
    remoteAddress: str
    remotePort: int
    routeStatus: str


@dataclasses.dataclass
class ClockSource:
    current: str
    available: [str]


@dataclasses.dataclass
class Bios:
    vendor: str
    release: str
    version: str
    date: str


@dataclasses.dataclass
class Motherboard:
    name: str
    vendor: str
    version: str
    bios: Bios


@dataclasses.dataclass
class GpuMetrics:
    temperatureEdge: int
    temperatureHotspot: int
    temperatureMem: int
    temperatureVrgfx: int
    temperatureVrsoc: int
    temperatureVrmem: int
    averageSocketPower: int
    averageGfxclkFrequency: int
    averageSockclkFrequency: int
    averageUclkFrequency: int
    currentGfxclk: int
    currentSockclk: int
    throttleStatus: int
    currentFanSpeed: int
    pcieLinkWidth: int
    pcieLinkSpeed: int


@dataclasses.dataclass
class ByteSize:
    __bytes: int

    def b(self):
        return self.__bytes

    def kb(self):
        return self.__bytes / 1000

    def mb(self):
        return self.__bytes / (1000 ** 2)

    def gb(self):
        return self.__bytes / (1000 ** 3)

    def tb(self):
        return self.__bytes / (1000 ** 4)

    def kib(self):
        return self.__bytes / 1024

    def mib(self):
        return self.__bytes / (1024 ** 2)

    def gib(self):
        return self.__bytes / (1024 ** 3)

    def tib(self):
        return self.__bytes / (1024 ** 4)

    def fmt(self, rounded=-1):
        bytes = self.__bytes
        unit = 'B'

        while bytes >= 1024:
            bytes /= 1024

            if unit == 'B':
                unit = 'kiB'

            elif unit == 'kiB':
                unit = 'MiB'

            elif unit == 'MiB':
                unit = 'GiB'

            elif unit == 'GiB':
                unit = 'TiB'
                break

        return f'{bytes if rounded == -1 else round(bytes, rounded)} {unit}'

@dataclasses.dataclass
class StoragePartition:
    device: str
    mountPoint: str
    filesystem: str
    size: ByteSize
    startPoint: str


@dataclasses.dataclass
class NvmeDevice:
    device: str
    pcieAddress: str
    model: str
    linkSpeedGTs: float
    pcieLanes: int
    size: ByteSize
    partitions: [StoragePartition]


@dataclasses.dataclass
class StorageDevice:
    model: str
    device: str
    size: ByteSize
    partitions: [StoragePartition]


@dataclasses.dataclass
class CpuFrequency:
    average: Frequency
    processors: [ProcessorFrequency]


@dataclasses.dataclass
class Backlight:
    brightness: int
    maxBrightness: int


@dataclasses.dataclass
class Load:
    oneMinute: int
    fiveMinutes: int
    fifteenMinutes: int


@dataclasses.dataclass
class IPv4:
    address: str
    interface: str
    broadcast: str
    cidr: int
    netmask: str


@dataclasses.dataclass
class BusInput:
    bus: int
    vendor: int
    product: int
    version: int
    name: str
    physicalPath: str
    sysfsPath: str
    uniqueIdentifier: str
    handles: [str]
    properties: int
    events: int
    keys: [str]
    miscellaneousEvents: int
    led: int


class InterfaceType:
    PHYSICAL = 'physical'
    VIRTUAL = 'virtual'


@dataclasses.dataclass
class NetowrkInterface:
    name: str
    macAddress: str
    interfaceType: str


def __linuxCheck():
    if not os.path.exists('/sys') or not os.path.exists('/proc'):
        raise Exception('Detected non-Linux system')


def __readFile(filePath):
    try:
        with open(filePath, 'r') as file:
            return file.read()

    except:
        return ''


def __batteryPath():
    DRIVER_DIR = '/sys/class/power_supply'
    batteries = []

    for dir in os.listdir(DRIVER_DIR):
        path = f'{DRIVER_DIR}/{dir}'

        if 'type' not in os.listdir(path):
            continue

        with open(f'{path}/type', 'r') as type:
            if type != 'Battery':
                continue

        if os.path.exists(f'{path}/status') and os.path.exists(f'{path}/capacity'):
            batteries.append(path)

    try:
        battery = batteries[0]

    except:
        return None

    return battery


def batteryInfo():
    __linuxCheck()

    batteryPath = __batteryPath()

    if batteryPath is None:
        return None

    try:
        with open(f'{batteryPath}/capacity', 'r') as file:
            capacity = file.read().strip()

    except:
        return None

    else:
        if not capacity:
            return None

    try:
        capacity = int(capacity)
    except:
        capacity = None

    try:
        with open(f'{batteryPath}/status', 'r') as file:
            status = file.read().strip()

    except:
        return None

    else:
        if not status:
            return None

    if status == 'Charging':
        status = BatteryStatus.Charging

    elif status == 'Discharging':
        status = BatteryStatus.Discharging

    elif status == 'Full':
        status = BatteryStatus.Full

    else:
        status = None

    return Battery(
        capacity=capacity,
        status=status
    )


def gpuUsage():
    __linuxCheck()

    try:
        with open('/sys/class/drm/card0/device/gpu_busy_percent', 'r') as file:
            return float(file.read().strip())

    except:
        return None


def __getStats():
    with open('/proc/stat', 'r') as file:
        statFile = file.read()

    lines = statFile.split('\n')
    intLines = []

    for line in lines:
        if 'cpu' not in line:
            continue

        splittedLine = line.split(' ')
        intLine = []

        for chunk in splittedLine:
            if chunk and 'cpu' not in chunk:
                intLine.append(int(chunk))
        intLines.append(intLine)

    return intLines


def cpuUsage():
    __linuxCheck()

    before = __getStats()
    time.sleep(0.25)
    after = __getStats()

    processors = []

    for i in range(len(before)):
        beforeLine = before[i]
        afterLine = after[i]

        beforeSum = sum(beforeLine)
        afterSum = sum(afterLine)

        delta = afterSum - beforeSum
        processors.append(
            ProcessorUsage(
                total=100 - (afterLine[3] - beforeLine[3]) * 100 / delta,
                user=(afterLine[0] - beforeLine[0]) * 100 / delta,
                nice=(afterLine[1] - beforeLine[1]) * 100 / delta,
                system=(afterLine[2] - beforeLine[2]) * 100 / delta,
                idle=(afterLine[3] - beforeLine[3]) * 100 / delta,
                iowait=(afterLine[4] - beforeLine[4]) * 100 / delta,
                interrupt=(afterLine[5] - beforeLine[5]) * 100 / delta,
                soft_interrupt=(afterLine[6] - beforeLine[6]) * 100 / delta,
            )
        )

    return CpuUsage(
        average=processors[0],
        processors=processors[1:]
    )


def ramUsagePercent():
    __linuxCheck()

    with open('/proc/meminfo', 'r') as file:
        fileContent = file.read()

    memTotal = 0
    memAvailable = 0

    for element in fileContent.split('\n'):
        if 'MemTotal' in element:
            memTotal = int(element.split(' ')[-2])

        elif 'MemAvailable' in element:
            memAvailable = int(element.split(' ')[-2])

    return 100 - memAvailable * 100 / memTotal

def ramCached():
    __linuxCheck()

    with open('/proc/meminfo', 'r') as file:
        fileContent = file.read()

    memCached = 0
    for line in fileContent.split('\n'):
        if line.startswith('Cached:'):
            memCached = int(line.replace('Cached:', '').strip().split(' ')[0]) * 1024
            break

    return ByteSize(memCached)

def swapSize():
    __linuxCheck()

    with open('/proc/meminfo', 'r') as file:
        fileContent = file.read()

    swapSize = 0
    for line in fileContent.split('\n'):
        if line.startswith('SwapTotal:'):
            swapSize = int(line.replace('SwapTotal:', '').strip().split(' ')[0]) * 1024
            break

    return ByteSize(swapSize)

def swapUsagePercent():
    __linuxCheck()
    swapSizeBytes = swapSize().b()

    with open('/proc/meminfo', 'r') as file:
        fileContent = file.read()

    swapFree = 0
    for line in fileContent.split('\n'):
        if line.startswith('SwapFree:'):
            swapFree = int(line.replace('SwapFree:', '').strip().split(' ')[0]) * 1024
            break

    # swapFree : total = x : 100
    if swapSizeBytes == 0:
        return 0

    swapUsage = swapFree * 100 / swapSizeBytes
    return 100 - swapUsage

def swapCached():
    __linuxCheck()

    with open('/proc/meminfo', 'r') as file:
        fileContent = file.read()

    swapCached = 0
    for line in fileContent.split('\n'):
        if line.startswith('SwapCached:'):
            swapCached = int(line.replace('SwapCached:', '').strip().split(' ')[0]) * 1024
            break

    return ByteSize(swapCached)

def __getRate():
    with open('/proc/net/dev', 'r') as file:
        stats = file.read()

    downloadRate = 0
    uploadRate = 0

    for line in stats.split('\n'):
        if ':' in line:

            data = []
            for chunk in line.split(' '):
                if chunk and ':' not in chunk:
                    data.append(chunk)

            downloadRate += int(data[0])
            uploadRate += int(data[8])

    return downloadRate, uploadRate


def networkRate():
    __linuxCheck()

    downBefore, upBefore = __getRate()
    time.sleep(0.5)
    downAfter, upAfter = __getRate()

    return NetworkRate(
        download=(downAfter - downBefore) / 0.5,
        upload=(upAfter - upBefore) / 0.5
    )


def temperatureSensors():
    __linuxCheck()

    DRIVER_DIR = '/sys/class/hwmon'
    sensorsDirectories = os.listdir(DRIVER_DIR)

    sensors = []
    for directory in sensorsDirectories:
        try:
            with open(f'{DRIVER_DIR}/{directory}/name', 'r') as labelFile:
                label = labelFile.read().strip()
        except:
            label = None

        try:
            with open(f'{DRIVER_DIR}/{directory}/temp1_input', 'r') as temperatureFile:
                temperature = float(temperatureFile.read()) / 1000

        except:
            temperature = None

        if label is None:
            continue

        sensors.append(
            TemperatureSensor(
                label=label,
                temperature=temperature
            )
        )

    return sensors


def cpuInfo():
    __linuxCheck()

    with open('/proc/cpuinfo', 'r') as file:
        infoFile = file.read()

    modelName = ''
    for line in infoFile.split('\n'):
        if 'model name' in line:
            modelName = line.split(':')[1].strip()
            break

    DRIVER_DIR = '/sys/devices/system/cpu'
    coreCount = 0
    dieCount = 0

    for processor in os.listdir(DRIVER_DIR):
        if 'cpu' not in processor:
            continue

        try:
            with open(f'{DRIVER_DIR}/{processor}/topology/core_id', 'r') as file:
                coreId = file.read()

                if int(coreId) > coreCount:
                    coreCount = int(coreId)
        except:
            pass

        try:
            with open(f'{DRIVER_DIR}/{processor}/topology/die_id', 'r') as file:
                coreId = file.read()

                if int(coreId) > coreCount:
                    coreCount = int(coreId)
        except:
            pass
    if coreCount % 2:
        coreCount += 1
    dieCount += 1

    with open('/proc/cpuinfo', 'r') as file:
        threadCount = file.read().count('processor')

    DRIVER_DIR = '/sys/devices/system/cpu/cpufreq'
    maxFrequency = 0

    governors = []
    clockBoost = None

    for policy in os.listdir(DRIVER_DIR):
        if 'boost' in policy:
            with open(f'{DRIVER_DIR}/{policy}', 'r') as boostFile:
                clockBoost = True if boostFile.read() == '1' else False

            continue

        elif 'policy' not in policy:
            continue

        with open(f'{DRIVER_DIR}/{policy}/scaling_available_governors', 'r') as file:
            localGovernors = file.read().strip().split(' ')

            for governor in localGovernors:
                if governor not in governors:
                    governors.append(governor)

        with open(f'{DRIVER_DIR}/{policy}/cpuinfo_max_freq', 'r') as file:
            if (maxFreq := int(file.read())) > maxFrequency:
                maxFrequency = maxFreq

    maxFrequency /= 1000
    arch = ''

    if sys.maxsize == 2 ** (64 - 1) - 1:
        arch = '64 bit'

    elif sys.maxsize == 2 ** (32 - 1) - 1:
        arch = '32 bit'

    byteOrder = ''
    if sys.byteorder == 'little':
        byteOrder = 'Little Endian'

    elif sys.byteorder == 'big':
        byteOrder = 'Big Endian'

    return CpuInfo(
        modelName=modelName,
        cores=coreCount,
        threads=threadCount,
        dies=dieCount,
        governors=governors,
        maxFrequencyMHz=maxFrequency,
        clockBoost=clockBoost,
        architecture=arch,
        byteOrder=byteOrder
    )


def ramSize():
    __linuxCheck()

    with open('/proc/meminfo', 'r') as file:
        memInfo = file.read().split('\n')

    memTotal = 0
    for line in memInfo:

        if 'MemTotal' in line:
            memTotal = int(line.split(' ')[-2].strip())

    memBytes = memTotal * 1024
    return ByteSize(memBytes)

def schedulerInfo():
    __linuxCheck()

    DRIVER_DIR = '/sys/devices/system/cpu/cpufreq'
    policies = []

    for dir in os.listdir(DRIVER_DIR):
        if 'policy' not in dir:
            continue

        policyName = dir

        with open(f'{DRIVER_DIR}/{dir}/scaling_governor', 'r') as file:
            scalingGovernor = file.read().strip()

        with open(f'{DRIVER_DIR}/{dir}/scaling_driver', 'r') as file:
            scalingDriver = file.read().strip()

        with open(f'{DRIVER_DIR}/{dir}/scaling_max_freq', 'r') as file:
            scalingMaxFreq = int(file.read().strip())

        with open(f'{DRIVER_DIR}/{dir}/scaling_min_freq', 'r') as file:
            scalingMinFreq = int(file.read().strip())

        policies.append(
            SchedulerPolicy(
                name=policyName,
                scalingGovernor=scalingGovernor,
                scalingDriver=scalingDriver,
                minimumScalingMHz=scalingMinFreq,
                maximumScalingMHz=scalingMaxFreq
            )
        )

    return policies


def vramSize():
    __linuxCheck()

    try:
        with open('/sys/class/drm/card0/device/mem_info_vram_total', 'r') as file:
            fileContent = file.read()

        intSize = int(fileContent.strip())

        return VramSize(
            gb=intSize / 1000 / 1000 / 1000,
            gib=intSize / 1024 / 1024 / 1024
        )
    except:
        return None


def vramUsage():
    __linuxCheck()

    try:
        with open('/sys/class/drm/card0/device/mem_info_vram_total', 'r') as file:
            fileContent = file.read()

        intSize = int(fileContent.strip())

        with open('/sys/class/drm/card0/device/mem_info_vram_used', 'r') as file:
            fileContent = file.read()

        intUsed = int(fileContent.strip())

        return intUsed * 100 / intSize

    except:
        return None


def __bytesToAddress(address, separator):
    chunks = []

    for index in range(0, len(address), 2):
        chunks.append(
            str(int(address[index:index + 2], 16))
        )

    chunks = chunks[::-1]
    return separator.join(chunks)


def __bytesToPort(port):
    LSB = port[:2]
    MSB = port[2:]

    return (int(MSB, 16) << 8) + (int(LSB, 16))


def __getRoutes(filePath, separator, routeType):
    routes = []

    try:
        with open(filePath, 'r') as file:
            fileContent = file.read()

    except:
        return []

    for line in fileContent.split('\n'):
        if ':' not in line:
            continue

        splittedLine = line.strip().split(' ')
        local = splittedLine[1].split(':')
        remote = splittedLine[2].split(':')

        localAddress = __bytesToAddress(local[0], separator)
        localPort = __bytesToPort(local[1])

        remoteAddress = __bytesToAddress(remote[0], separator)
        remotePort = __bytesToPort(remote[1])

        statusCode = splittedLine[3]
        if routeType in (RouteType.TCP, RouteType.TCP6):
            status = RouteStatus.fromTcpCode(statusCode)

        else:
            status = RouteStatus.LISTENING

        routes.append(
            NetworkRoute(
                routeType=routeType,
                localAddress=localAddress,
                localPort=localPort,
                remoteAddress=remoteAddress,
                remotePort=remotePort,
                routeStatus=status
            )
        )

    return routes


def networkRoutes():
    __linuxCheck()

    routes = []

    routes.extend(
        __getRoutes(
            '/proc/net/tcp', '.', RouteType.TCP
        )
    )

    routes.extend(
        __getRoutes(
            '/proc/net/udp', '.', RouteType.UDP
        )
    )

    routes.extend(
        __getRoutes(
            '/proc/net/tcp6', ':', RouteType.TCP6
        )
    )

    routes.extend(
        __getRoutes(
            '/proc/net/udp6', ':', RouteType.UDP6
        )
    )

    return routes


def clockSource():
    __linuxCheck()

    currentClockSource = ''
    try:
        with open('/sys/devices/system/clocksource/clocksource0/current_clocksource', 'r') as file:
            currentClockSource = file.read().strip()
    except:
        pass

    availableClockSources = []
    try:
        with open('/sys/devices/system/clocksource/clocksource0/available_clocksource', 'r') as file:
            availableClockSources = file.read().strip().split(' ')
    except:
        pass

    return ClockSource(
        current=currentClockSource,
        available=availableClockSources
    )


def biosInfo():
    __linuxCheck()

    vendor = ''
    try:
        with open('/sys/devices/virtual/dmi/id/bios_vendor', 'r') as file:
            vendor = file.read().strip()
    except:
        pass

    release = ''
    try:
        with open('/sys/devices/virtual/dmi/id/bios_release', 'r') as file:
            release = file.read().strip()
    except:
        pass

    version = ''
    try:
        with open('/sys/devices/virtual/dmi/id/bios_version', 'r') as file:
            version = file.read().strip()
    except:
        pass

    date = ''
    try:
        with open('/sys/devices/virtual/dmi/id/bios_date', 'r') as file:
            date = file.read().strip()
    except:
        pass

    return Bios(
        vendor=vendor,
        version=version,
        release=release,
        date=date
    )


def motherboardInfo():
    __linuxCheck()

    name = ''
    try:
        with open('/sys/devices/virtual/dmi/id/board_name', 'r') as file:
            name = file.read().strip()
    except:
        pass

    vendor = ''
    try:
        with open('/sys/devices/virtual/dmi/id/board_vendor', 'r') as file:
            vendor = file.read().strip()
    except:
        pass

    version = ''
    try:
        with open('/sys/devices/virtual/dmi/id/board_version', 'r') as file:
            version = file.read().strip()
    except:
        pass

    bios = biosInfo()
    return Motherboard(
        name=name,
        version=version,
        vendor=vendor,
        bios=bios
    )


def __bytesToInt(bytes):
    res = 0
    shift = 8 * len(bytes)

    if sys.byteorder == 'little':
        bytes = bytes[::-1]

    for byte in bytes:
        shift -= 8
        res += byte << shift

    return res


def gpuMetrics():
    __linuxCheck()

    try:
        with open('/sys/class/drm/card0/device/gpu_metrics', 'rb') as file:
            bytes = file.read()

    except:
        pass

    if bytes[2] != 1:
        return None

    content = bytes[3]
    bytes = bytes[4:]

    return GpuMetrics(
        temperatureEdge=__bytesToInt(bytes[0:2] if content else bytes[8:10]),
        temperatureHotspot=__bytesToInt(bytes[2:4] if content else bytes[10:12]),
        temperatureMem=__bytesToInt(bytes[4:6] if content else bytes[12:14]),
        temperatureVrgfx=__bytesToInt(bytes[6:8] if content else bytes[14:16]),
        temperatureVrsoc=__bytesToInt(bytes[8:10] if content else bytes[16:18]),
        temperatureVrmem=__bytesToInt(bytes[10:12] if content else bytes[18:20]),
        averageSocketPower=__bytesToInt(bytes[18:20] if content else bytes[26:28]),
        averageGfxclkFrequency=__bytesToInt(bytes[36:38]),
        averageSockclkFrequency=__bytesToInt(bytes[38:40]),
        averageUclkFrequency=__bytesToInt(bytes[40:42]),
        currentGfxclk=__bytesToInt(bytes[50:52]),
        currentSockclk=__bytesToInt(bytes[52:54]),
        throttleStatus=__bytesToInt(bytes[64:68]),
        currentFanSpeed=__bytesToInt(bytes[68:70]),
        pcieLinkWidth=__bytesToInt(bytes[70:72]),
        pcieLinkSpeed=__bytesToInt(bytes[72:74]),
    )


def nvmeDevices():
    __linuxCheck()

    baseDir = '/sys/class/nvme'

    try:
        dirContent = os.listdir(baseDir)
    except:
        return []

    devices = []
    partitions = __readFile('/proc/partitions').strip()
    mountPoints = __readFile('/proc/mounts').strip()

    for device in dirContent:
        address = __readFile(f'{baseDir}/{device}/address').strip()
        model = __readFile(f'{baseDir}/{device}/model').strip()

        linkSpeed = __readFile(f'{baseDir}/{device}/device/current_link_speed').strip()
        linkSpeed = float(linkSpeed.split(' ')[0])

        pcieLanes = __readFile(f'{baseDir}/{device}/device/current_link_width').strip()
        pcieLanes = int(pcieLanes)

        size = 0
        for partitionLine in partitions.strip().split('\n')[2:]:
            if device in partitionLine:
                size = int(partitionLine.split(' ')[-2])

        localPartitions = []
        for mount in mountPoints.split('\n'):

            if device in mount:
                splitted = mount.split(' ')
                device = splitted[0]
                deviceName = device.split('/')[2]

                mountPoint = splitted[1]
                filesystem = splitted[2]

                partSize = ByteSize(0)
                startPoint = 0

                for partition in partitions.split('\n'):
                    if deviceName in partition:
                        try:
                            partSize = ByteSize(
                                int(
                                    __readFile(f'/sys/class/block/{deviceName}/size').strip()
                                )
                            )
                        except:
                            pass

                        try:
                            startPoint = int(
                                __readFile(f'/sys/class/block/{deviceName}/start').strip()
                            )
                        except:
                            pass

                        break

                localPartitions.append(StoragePartition(
                    device=device,
                    mountPoint=mountPoint,
                    filesystem=filesystem,
                    size=partSize,
                    startPoint=startPoint
                ))

        devices.append(NvmeDevice(
            device=device,
            model=model,
            pcieAddress=address,
            linkSpeedGTs=linkSpeed,
            pcieLanes=pcieLanes,
            size=ByteSize(size),
            partitions=localPartitions
        ))

    return devices


def storageDevices():
    __linuxCheck()

    baseDir = '/sys/class/block'

    try:
        dirContent = os.listdir(baseDir)
    except:
        return []

    mountPoints = __readFile('/proc/mounts').split('\n')

    devices = []
    for dir in dirContent:
        if 'sd' not in dir or len(dir) != 3:
            continue

        device = f'/dev/{dir}'
        size = __readFile(f'{baseDir}/{dir}/size').strip()

        try:
            size = ByteSize(int(size))

        except:
            size = ByteSize(0)

        model = __readFile(f'{baseDir}/{dir}/device/model').strip()
        partitions = []

        for partitionDir in dirContent:
            if dir not in partitionDir:
                continue

            if len(partitionDir) <= 3:
                continue

            partitionSize = __readFile(f'{baseDir}/{partitionDir}/size').strip()
            partitionSize = ByteSize(int(partitionSize) if partitionSize else 0)

            startByte = __readFile(f'{baseDir}/{partitionDir}/start').strip()
            startByte = ByteSize(int(startByte) if startByte else 0)

            mountPoint = ''
            fileSystem = ''

            for mount in mountPoints:
                if f'/dev/{partitionDir} ' in mount:
                    splitted = mount.split(' ')

                    mountPoint = splitted[1]
                    fileSystem = splitted[2]
                    break

            partitions.append(
                StoragePartition(
                    device=f'/dev/{partitionDir}',
                    mountPoint=mountPoint,
                    filesystem=fileSystem,
                    size=partitionSize,
                    startPoint=startByte
                )
            )

        devices.append(
            StorageDevice(
                model=model,
                device=device,
                size=size,
                partitions=partitions
            )
        )

    devices.extend(nvmeDevices())
    return devices


def cpuFrequency():
    __linuxCheck()

    totalFreq = 0
    frequencies = []

    fileContent = __readFile('/proc/cpuinfo')
    for chunk in fileContent.split('\n\n'):
        if not chunk or chunk == ' ':
            continue

        id = ''
        freq = 0

        for line in chunk.split('\n'):
            if 'processor' in line:
                id = line.strip().split(':')[-1]

            elif 'cpu MHz' in line:
                freq = float(line.strip().split(':')[-1])

        if not id or freq == 0:
            continue

        totalFreq += freq * 1000
        frequencies.append(
            ProcessorFrequency(
                processorID=id,
                frequency=Frequency(
                    _khz=freq * 1000
                )
            )
        )

    return CpuFrequency(
        average=Frequency(
            _khz=totalFreq * 1000 / len(frequencies)
        ),
        processors=frequencies
    )


def getBacklight():
    baseDir = '/sys/class/backlight'
    dirs = os.listdir(baseDir)
    path = ''

    for dir in dirs:
        dirPath = os.path.join(baseDir, dir)
        if os.path.exists(os.path.join(dirPath, 'brightness')) and os.path.exists(
                os.path.join(dirPath, 'max_brightness')):
            path = dirPath
            break

    if not path:
        return None

    with open(os.path.join(path, 'brightness'), 'r') as file:
        brightness = int(file.read().strip().replace(',', '.'))

    with open(os.path.join(path, 'max_brightness'), 'r') as file:
        maxBrightness = int(file.read().strip().replace(',', '.'))

    return Backlight(brightness, maxBrightness)


def getLoad():
    with open('/proc/loadavg', 'r') as file:
        content = file.read()

    splitted = content.split(' ')
    return Load(
        oneMinute=splitted[0],
        fiveMinutes=splitted[1],
        fifteenMinutes=splitted[2]
    )


def __containsAddress(addresses, address):
    for addr, broadcast, netmask, cidr in addresses:
        if addr == address:
            return True
    return False


def __bitsToByte(bits):
    reversed = bits[::-1]
    byte = 0

    for index, bit in enumerate(reversed):
        byte += bit * (2 ** index)

    return byte


def __netmaskFromCidr(cidr):
    bits = []

    for i in range(32):
        if i < int(cidr):
            bits.append(1)

        else:
            bits.append(0)

    mask = []
    i = 0
    while i < 32:
        mask.append(__bitsToByte(bits[i:i + 8]))
        i += 8

    return f'{mask[0]}.{mask[1]}.{mask[2]}.{mask[3]}'


def getIPv4():
    ipv4Addresses = []

    interfaces = []
    addresses = []

    routes = __readFile("/proc/net/route")
    fibTrie = __readFile("/proc/net/fib_trie")

    index = 0
    lines = fibTrie.split('|--')

    while index < len(lines):
        line = lines[index]
        chunks = line.split('\n')

        address = chunks[0].strip()
        addressType = chunks[1].strip()

        if '/32 host LOCAL' in addressType and not __containsAddress(addresses, address):
            broadcast = lines[index + 1].split('\n')[0].strip()
            cidr = lines[index - 1].split('\n')[1].strip().split(' ')[0].replace('/', '').strip()

            mask = __netmaskFromCidr(cidr)
            addresses.append((address, broadcast, cidr, mask))

        index += 1

    for line in routes.split('\n'):
        if not line or 'Gateway' in line:
            continue

        splittedLine = line.split('\t')
        device = splittedLine[0].strip()

        network = __bytesToAddress(splittedLine[1], '.')
        ip = None
        brd = None

        mask = None
        cidr = None

        for address, broadcast, cidrAddr, netmask in addresses:
            addressNetwork = address.strip().split('.')

            addressNetwork[3] = '0'
            addressNetwork = '.'.join(addressNetwork)

            if network == addressNetwork:
                ip = address
                brd = broadcast
                cidr = cidrAddr
                mask = netmask

        if ip is not None:
            ipv4Addresses.append(
                IPv4(
                    address=ip.strip(),
                    interface=device,
                    broadcast=brd,
                    cidr=cidr,
                    netmask=mask
                ))

    return ipv4Addresses


def busInput():
    inputs = []

    with open('/proc/bus/input/devices', 'r') as file:
        fileContent = file.read()

    for chunk in fileContent.split('\n\n'):
        if not chunk.strip():
            continue

        bus = None
        vwndor = None
        version = None
        product = None
        name = None
        physicalPath = None
        sysfsPath = None
        uniqueIdentifier = None
        handlees = []
        properties = None
        events = None
        miscellaneousEvents = None
        led = None
        keys = []

        for line in chunk.strip().split('\n'):

            if 'I: ' in line:
                for block in line.strip().split(' '):
                    if 'Bus=' in block:
                        bus = int(block.replace('Bus=', ''), 16)

                    elif 'Vendor=' in block:
                        vendor = int(block.replace('Vendor=', ''), 16)

                    elif 'Version=' in block:
                        version = int(block.replace('Version=', ''), 16)

                    elif 'Product=' in block:
                        product = int(block.replace('Product=', ''), 16)

            elif (target := 'N: Name=') in line:
                name = line.replace(target, '').replace('"', '')

            elif (target := 'P: Phys=') in line:
                physicalPath = line.replace(target, '')

            elif (target := 'S: Sysfs=') in line:
                sysfsPath = line.replace(target, '')

            elif (target := 'U: Uniq=') in line:
                uniqueIdentifier = line.replace(target, '')

            elif (target := 'H: Handlers=') in line:
                handlersList = line.replace(target, '').split(' ')
                handles = []

                for handler in handlersList:
                    handles.append(handler)

            elif (target := 'B: PROP=') in line:
                properties = int(line.replace(target, ''), 16)

            elif (target := 'B: EV=') in line:
                events = int(line.replace(target, ''), 16)

            elif (target := 'B: MSC=') in line:
                miscellaneousEvents = int(line.replace(target, ''), 16)

            elif (target := 'B: LED=') in line:
                led = int(line.replace(target, ''), 16)

            elif (target := 'B: KEY=') in line:
                keys = []

                for key in line.replace(target, '').split(' '):
                    keys.append(key)

        inputs.append(BusInput(
            bus=bus,
            vendor=vendor,
            product=product,
            version=version,
            name=name,
            physicalPath=physicalPath,
            sysfsPath=sysfsPath,
            uniqueIdentifier=uniqueIdentifier,
            handles=handles,
            properties=properties,
            events=events,
            keys=keys,
            miscellaneousEvents=miscellaneousEvents,
            led=led
        ))

    return inputs


def networkInterfaces():
    baseDirectory = '/sys/class/net'
    interfaces = []

    for directory in os.listdir(baseDirectory):
        name = directory
        path = f'{baseDirectory}/{name}'

        with open(f'{path}/address', 'r') as file:
            mac = file.read().strip()

        interfaceType = InterfaceType.VIRTUAL
        directoryContent = os.listdir(path)

        if 'phydev' in directoryContent or 'phy80211' in directoryContent:
            interfaceType = InterfaceType.PHYSICAL

        interfaces.append(NetowrkInterface(name=name, macAddress=mac, interfaceType=interfaceType))

    return interfaces


def exportJson():
    json = {}

    def processorUsageToJson(usage):
        return {
            'total': usage.total,
            'user': usage.user,
            'nice': usage.nice,
            'system': usage.system,
            'idle': usage.idle,
            'iowait': usage.iowait,
            'interrupt': usage.interrupt,
            'soft-interrupt': usage.soft_interrupt
        }

    def schedulerPolicyToJson(sched):
        return {
            'scaling-governor': sched.scalingGovernor,
            'scaling-driver': sched.scalingDriver,
            'minimum-scaling-mhz': sched.minimumScalingMHz,
            'maximum-scaling-mhz': sched.maximumScalingMHz
        }

    def partitionToJson(partition: StoragePartition):
        return {
            'device': partition.device,
            'mount-point': partition.mountPoint,
            'filesystem': partition.filesystem,
            'size': partition.size,
            'start-point': partition.startPoint
        }

    def nvmeDeviceToJson(device: NvmeDevice):
        return {
            'device': device.device,
            'pcie-address': device.pcieAddress,
            'model': device.model,
            'link-speed-gts': device.linkSpeedGTs,
            'pcie-lanes': device.pcieLanes,
            'size': device.size,
            'partitions': [partitionToJson(partition) for partition in device.partitions]
        }

    def storageDeviceToJson(device: StorageDevice):
        return {
            'device': device.device,
            'model': device.model,
            'size': device.size,
            'partitions': [partitionToJson(partition) for partition in device.partitions]
        }

    def networkRouteToJson(route: NetworkRoute):
        return {
            'type': route.routeType,
            'local-address': route.localAddress,
            'local-port': route.localPort,
            'remote-address': route.remoteAddress,
            'remote-port': route.remotePort,
            'status': route.routeStatus
        }

    cpu = CPU()
    cpuClockSource = clockSource()

    json['cpu'] = {
        'model-name': cpu.info.modelName,
        'cores': cpu.info.cores,
        'threads': cpu.info.threads,
        'dies': cpu.info.dies,
        'governors': cpu.info.governors,
        'max-frequency': cpu.info.maxFrequencyMHz,
        'clock-boost': cpu.info.clockBoost,
        'architecture': cpu.info.architecture,
        'byte-order': cpu.info.byteOrder,
        'usage': processorUsageToJson(cpu.averageUsage),
        'scheduler-policies': {sched.name: schedulerPolicyToJson(sched) for sched in cpu.schedulerPolicies},
        'frequency': cpu.averageFrequency.khz(),
        'clock-source': {
            'current': cpuClockSource.current,
            'available': cpuClockSource.available
        }
    }

    json['ram'] = {
        'usage': ramUsagePercent(),
        'size-gb': ramSize().gb,
        'size-gib': ramSize().gib
    }

    moboInfo = motherboardInfo()
    json['motherboard'] = {
        'name': moboInfo.name,
        'vendor': moboInfo.vendor,
        'version': moboInfo.version,
        'bios': {
            'vendor': moboInfo.bios.vendor,
            'release': moboInfo.bios.release,
            'version': moboInfo.bios.version,
            'date': moboInfo.bios.date
        }
    }

    nvmeDevicesList = nvmeDevices()
    json['nvme-devices'] = [nvmeDeviceToJson(device) for device in nvmeDevicesList]

    storageDevicesList = storageDevices()
    json['storage-devices'] = [storageDeviceToJson(device) for device in storageDevicesList]

    battery = batteryInfo()
    json['battery'] = {'status': battery.status, 'capacity': battery.capacity} if battery else None

    backlight = getBacklight()
    json['backlight'] = {
        'brightness': backlight.brightness, 'max-brightness': backlight.maxBrightness
    } if backlight else None

    rate = networkRate()
    routes = networkRoutes()

    json['network'] = {
        'rate': {
            'upload': rate.upload,
            'download': rate.download
        },
        'routes': [networkRouteToJson(route) for route in routes]
    }

    tempSensors = temperatureSensors()
    json['temperature-sensors'] = [
        {'label': sensor.label, 'temperature': sensor.temperature} for sensor in tempSensors
    ]

    json['vram-size'] = {
        'gb': vramSize().gb,
        'gib': vramSize().gib
    }

    metrics = gpuMetrics()
    json['gpu-metrics'] = {
        'temperature-edge': metrics.temperatureEdge,
        'temperature-hotspot': metrics.temperatureHotspot,
        'temperature-mem': metrics.temperatureMem,
        'temperature-vrgfx': metrics.temperatureVrgfx,
        'temperature-vrsoc': metrics.temperatureVrsoc,
        'temperature-vrmem': metrics.temperatureVrmem,
        'average-socket-power': metrics.averageSocketPower,
        'average-gfxclk-frequency': metrics.averageGfxclkFrequency,
        'average-sockclk-frequency': metrics.averageSockclkFrequency,
        'average-uclk-frequency': metrics.averageUclkFrequency,
        'current-gfxclk': metrics.currentGfxclk,
        'current-sockclk': metrics.currentSockclk,
        'throttle-status': metrics.throttleStatus,
        'current-fan-speed': metrics.currentFanSpeed,
        'pcie-link-width': metrics.pcieLinkWidth,
        'pcie-link-speed': metrics.pcieLinkSpeed
    }

    load = getLoad()
    json['load'] = {
        'one-minute': load.oneMinute,
        'five-minutes': load.fiveMinutes,
        'fifteen-minutes': load.fifteenMinutes
    }

    ipv4Addresses = getIPv4()
    json['ipv4'] = [
        {
            'address': address.address,
            'interface': address.interface,
            'broadcast': address.broadcast,
            'cidr': address.cidr,
            'netmask': address.netmask
        } for address in ipv4Addresses
    ]

    busInputs = busInput()
    json['bus-input'] = []
    for bus in busInputs:
        json['bus-input'].append(
            {
                'bus': bus.bus,
                'vendor': bus.vendor,
                'product': bus.product,
                'version': bus.version,
                'physical-path': bus.physicalPath,
                'sysfs-path': bus.sysfsPath,
                'name': bus.name,
                'handles': bus.handles,
                'properties': bus.properties,
                'events': bus.events,
                'keys': bus.keys,
                'miscellaneous-events': bus.miscellaneousEvents,
                'led': bus.led
            }
        )

    json['network-interfaces'] = {}
    for interface in networkInterfaces():
        json['network-interfaces'][interface.name] = {
            'mac': interface.macAddress,
            'interface-type': interface.interfaceType
        }

    return json


if __name__ == '__main__':
    print(cpuUsage())
    print(f'RAM usage:', ramUsagePercent())

    print(networkRate())
    print(f'GPU usage:', gpuUsage())

    print(temperatureSensors())
    print(cpuInfo())

    print(ramSize())
    print(schedulerInfo())

    print(batteryInfo())
    print(vramSize())

    print('VRAM usage:', vramUsage())
    print(networkRoutes())

    print(CPU())
    print(cpuFrequency())

    print(clockSource())
    print(motherboardInfo())

    print(gpuMetrics())
    print(storageDevices())

    print(nvmeDevices())
    print(getBacklight())

    print(getLoad())
    print(getIPv4())

    print(networkInterfaces())

    print(busInput())
    print(exportJson())
