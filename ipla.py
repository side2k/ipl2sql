import re
from sys import argv

LENGTH_FIELD = 'LEN'
IN_FIELD = 'IN'
OUT_FIELD = 'OUT'
SRC_FIELD = 'SRC'
DST_FIELD = 'DST'

def short_number(number, multiplier=1000):
    if number > multiplier:
        divided = float(number) / multiplier
        floor, grade = short_number(divided, multiplier)
        return floor, grade + 1
    else:
        return number, 0

def str_bytes(bytes_count):
    suffixes = ['b', 'k', 'M', 'G', 'T']
    number, grade = short_number(bytes_count, multiplier=1024)
    return '%.1f%s' % (number, suffixes[grade])

if argv[0] == __file__:
    log_path = argv[1]
else:
    log_path = argv[0]

log = open(log_path, 'r')
fields_re = re.compile(r'([A-Z]+)=([^ ]+)( |$|\n)')

line_count = 0
try:
    for line in log:
        packet = {}
        for name,value,_ in fields_re.findall(line):
            if name == LENGTH_FIELD:
                value = int(value)
                if name in packet:
                    packet[name] += value
                    continue
            packet[name] = value

        packet_size = packet.get(LENGTH_FIELD, 0)
            
        keys_if = []

        dst_if = packet.get(IN_FIELD)

        src_if = packet.get(OUT_FIELD)        
        if src_if:
            keys_if += ['from_%s' % src_if]

        for key_if in keys_if:
            if key_if not in stats:
                stats[key_if] = {'_total':packet_size}
            else:
                stats[key_if]['_total'] += packet_size

        src_ip = packet.get(SRC_FIELD)
        if src_ip:

        line_count += 1
        if line_count and not (line_count % 10000):
            print 'Analyzed %d lines' % line_count
finally:
    log.close()
    print 'Analyzed %d lines' % line_count

for key in stats:
    print key, str_bytes(stats[key])

