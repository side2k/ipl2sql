import re
from sys import argv, stderr

LENGTH_FIELD = 'LEN'
IN_FIELD = 'IN'
OUT_FIELD = 'OUT'
SRC_FIELD = 'SRC'
DST_FIELD = 'DST'

USED_FIELDS = [
    IN_FIELD,
    OUT_FIELD,
    SRC_FIELD,
    DST_FIELD,
    LENGTH_FIELD
]

PACKETS_PER_BLOCK = 1000

ARG_NAMES = ['log_path', 'table_name']
class Settings:
    pass

def for_sql(value):
    if value is None:
        return "NULL"
    elif type(value) == int:
        return "%d" % value
    else:
        return '"%s"' % value

def parse_args(args):
    settings = Settings()
    for arg_index, arg in enumerate(args):
        arg_name = ARG_NAMES[arg_index]
        setattr(settings, arg_name, arg)
    return settings


def values_block(fields, packet):
    fields_str = []
    for field in fields:
        value = packet.get(field)
        fields_str += [for_sql(value)]
    return ','.join(fields_str)

def packets_block(fields, packets):
    return ','.join(['(%s)' % values_block(fields, packet) for packet in packets])

def insert_block(table_name, fields, packets):
    return "INSERT INTO %(table_name)s (%(value_names)s) VALUES %(values)s;" % {
        'table_name': table_name,
        'value_names': ','.join(['`%s`' % field for field in fields]),
        'values': packets_block(fields, packets)
    }

def clear_table(table_name):
    return "DELETE FROM %s;" % table_name

if argv[0] == __file__:
    settings = parse_args(argv[1:])
else:
    settings = parse_args(argv)


log = open(settings.log_path, 'r')
fields_re = re.compile(r'([A-Z]+)=([^ ]+)( |$|\n)')
line_count = 0

try:
    current_block = []
    print clear_table(settings.table_name)
    for line in log:
        packet = {}
        for name,value,_ in fields_re.findall(line):
            if name == LENGTH_FIELD:
                value = int(value)
                if name in packet:
                    packet[name] += value
                    continue
            packet[name] = value

        current_block += [packet]
        if len(current_block) >= PACKETS_PER_BLOCK:
            print insert_block(settings.table_name, USED_FIELDS, current_block)
            current_block = []

        line_count += 1
        if line_count and not (line_count % 10000):
            stderr.write('Analyzed %d lines\n' % line_count)

    if len(current_block):
        print insert_block(settings.table_name, USED_FIELDS, current_block)

finally:
    log.close()
    stderr.write('Analyzed %d lines\n' % line_count)