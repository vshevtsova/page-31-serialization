from struct import pack, unpack

def pack_int(x):
    type_name = 'i'
    len_of_pack = 9
    pack_str = pack('=i', x)
    return pack('=s', type_name) + pack('=i', len_of_pack) + pack_str

def unpack_int(x):
    x = x[5:]
    return unpack('=i', x[:4])[0]

def pack_str(x):
    type_name = 's'
    len_of_data = len(x)
    pack_str = pack('=' + str(len_of_data) + 's', x)
    len_of_pack = len_of_data + 9
    return pack('=s', type_name) + pack('=i', len_of_pack) +\
           pack('=i', len_of_data) + pack_str

def unpack_str(x):
    x = x[5:]
    len_of_data = unpack('=i', x[:4])[0]
    x = x[4:]
    return unpack('=' + str(len_of_data) + 's', x[:len_of_data])[0]

def pack_tuple(x):
    type_name = 't'
    len_of_data = len(x)
    pack_str = ''
    for i in x:
        pack_str += serialize(i)
    len_of_pack = len(pack_str) + 9
    return pack('=s', type_name) + pack('=i', len_of_pack) + \
           pack('=i', len_of_data) + pack_str

def unpack_tuple(x):
    x = x[5:]
    len_of_data = unpack('=i', x[:4])[0]
    x = x[4:]
    res = ()
    for i in xrange(len_of_data):
        type_name = unpack('=s', x[0])[0]
        len_of_items = unpack('=i', x[1:5])[0]
        res += (TYPE_DICT_UNPACK[type_name](x[:len_of_items]), )
        x = x[len_of_items:]
    return res

def pack_list(x):
    type_name = 'l'
    len_of_data = len(x)
    pack_str = ''
    for i in x:
        pack_str += serialize(i)
    len_of_pack = len(pack_str) + 9
    return pack('=s', type_name) + pack('=i', len_of_pack) + \
           pack('=i', len_of_data) + pack_str

def unpack_list(x):
    x = x[5:]
    len_of_data = unpack('=i', x[:4])[0]
    x = x[4:]
    res = []
    for i in xrange(len_of_data):
        type_name = unpack('=s', x[0])[0]
        len_of_items = unpack('=i', x[1:5])[0]
        res.append(TYPE_DICT_UNPACK[type_name](x[:len_of_items]))
        x = x[len_of_items:]
    return res

def pack_dict(x):
    type_name = 'd'
    len_of_data = len(x)
    pack_str = ''
    for k in x:
        pack_str += serialize(k)
        pack_str += serialize(x[k])
    len_of_pack = len(pack_str) + 9
    return pack('=s', type_name) + pack('=i', len_of_pack) + \
           pack('=i', len_of_data) + pack_str

def unpack_dict(x):
    x = x[5:]
    len_of_data = unpack('=i', x[:4])[0]
    x = x[4:]
    res = {}
    for i in xrange(len_of_data):
        type_name = unpack('=s', x[0])[0]
        len_of_items = unpack('=i', x[1:5])[0]
        k = TYPE_DICT_UNPACK[type_name](x[:len_of_items])
        x = x[len_of_items:]
        type_name = unpack('=s', x[0])[0]
        len_of_items = unpack('=i', x[1:5])[0]
        res[k] = TYPE_DICT_UNPACK[type_name](x[:len_of_items])
        x = x[len_of_items:]
    return res

TYPE_DICT_PACK = {int: pack_int,
                  str: pack_str,
                  tuple: pack_tuple,
                  list: pack_list,
                  dict: pack_dict}

TYPE_DICT_UNPACK = {'i': unpack_int,
                    's': unpack_str,
                    't': unpack_tuple,
                    'l': unpack_list,
                    'd': unpack_dict}

def serialize(x):
    return TYPE_DICT_PACK[type(x)](x)

def deserialize(x):
    type_name = unpack('=s', x[0])[0]
    return TYPE_DICT_UNPACK[type_name](x)

x = {'a':1, 'b':[1,2,3,['3']], 4:7}
print x
s = serialize(x)
print s.__repr__()
ds = deserialize(s)
print ds
