'''
THIS FILE COMES FROM `sysutil-lib` package written by ryzeon-dev (me)
This is a stripped down version, only containing the code needed by sysfetch
'''

import dataclasses
import os
import sys
import time


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
class RamSize:
    gb: float
    gib: float


@dataclasses.dataclass
class VramSize:
    gb: float
    gib: float

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

def __linuxCheck():
    if not os.path.exists('/sys') or not os.path.exists('/proc'):
        raise Exception('Detected non-Linux system')

def __readFile(filePath):
    try:
        with open(filePath, 'r') as file:
            return file.read()

    except:
        return ''

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
    for addr, netAddress, broadcast, netmask, cidr in addresses:
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

def __broadcastFromAddressAndNetmask(address, netmask):
    intAddress = sum(int(octet) << (8 * i) for i, octet in enumerate(address.split('.')))
    intReverseMask = ~sum(int(octet) << (8 * i) for i, octet in enumerate(netmask.split('.')))

    intBroadcast = intAddress | intReverseMask

    broadcastChunks = [0, 0, 0, 0]
    broadcastChunks[0] = intBroadcast & 0xFF
    broadcastChunks[1] = (intBroadcast >> 8) & 0xFF
    broadcastChunks[2] = (intBroadcast >> 16) & 0xFF
    broadcastChunks[3] = (intBroadcast >> 24) & 0xFF

    return '.'.join(str(chunk) for chunk in broadcastChunks)

def getIPv4():
    ipv4Addresses = []
    addresses = []

    routes = __readFile("/proc/net/route")
    fibTrie = __readFile("/proc/net/fib_trie")

    index = 0
    lines = fibTrie.split('+--')

    while index < len(lines):
        line = lines[index]
        chunks = line.split('\n')

        if len(chunks) == 1 or ':' in line:
            index += 1
            continue

        networkBaseAddress = chunks[0].strip().split(' ')[0]

        cidr = networkBaseAddress.split('/')[1]
        netAddress = networkBaseAddress.split('/')[0]

        mask = __netmaskFromCidr(cidr)
        broadcast = __broadcastFromAddressAndNetmask(netAddress, mask)

        address = chunks[1].strip().replace('|--', '').strip()

        if not __containsAddress(addresses, address):
            addresses.append((address, netAddress, broadcast, cidr, mask))

        index += 1

    for line in routes.split('\n'):
        if not line or 'Gateway' in line:
            continue

        splittedLine = line.split('\t')
        if int(splittedLine[3]) == 3:
            continue
        device = splittedLine[0].strip()

        network = __bytesToAddress(splittedLine[1], '.')
        ip = None
        brd = None

        mask = None
        cidr = None

        for address, netAddres, broadcast, cidrAddr, netmask in addresses:
            if network == netAddres:
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