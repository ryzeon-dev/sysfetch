import distros

content = {}

for dst in distros.distro:
    content[dst.lower()] = distros.distro[dst]

with open('distros.py', 'w') as file:
    file.write('distro = {\n')
    for distro in content:
        file.write(f'\'{distro}\' : {content[distro]},\n')
    file.write('}')