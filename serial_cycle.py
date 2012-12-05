from struct import pack, unpack
import importlib

list_id = []
list_ref = []

def pack_int(x):
    type_name = 'i'
    list_id.append(id(x))
    type_name = 'i'
    len_of_pack = 10
    packed = pack('=B', 0) + pack('=i', x)
    return pack('=s', type_name) + pack('=i', len_of_pack) + packed

def unpack_int(x):
    x = x[6:]
    res = unpack('=i', x[:4])[0]
    list_ref.append(res)
    return res

def pack_float(x):
    type_name = 'f'
    list_id.append(id(x))
    len_of_pack = 14
    packed = pack('=B', 0) + pack('=d', x)
    return pack('=s', type_name) + pack('=i', len_of_pack) + packed

def unpack_float(x):
    x = x[6:]
    res = unpack('=d', x[:8])[0]
    list_ref.append(res)
    return res

def pack_str(x):
    type_name = 's'
    list_id.append(id(x))
    len_of_data = len(x)
    packed = pack('=B', 0) + pack('=i', len_of_data) + \
             pack('=' + str(len_of_data) + 's', x)
    len_of_pack = len(packed) + 5
    return pack('=s', type_name) + pack('=i', len_of_pack) + packed

def unpack_str(x):
    x = x[6:]
    len_of_data = unpack('=i', x[:4])[0]
    x = x[4:]
    res = unpack('=' + str(len_of_data) + 's', x[:len_of_data])[0]
    list_ref.append(res)
    return res

def pack_tuple(x):
    type_name = 't'
    list_id.append(id(x))
    len_of_data = len(x)
    packed = pack('=B', 0) + pack('=i', len_of_data)
    for i in x:
        packed += serial(i)
    len_of_pack = len(packed) + 5
    return pack('=s', type_name) + pack('=i', len_of_pack) + packed

def unpack_tuple(x):
    x = x[6:]
    len_of_data = unpack('=i', x[:4])[0]
    x = x[4:]
    res = ()
    index = len(list_ref)
    list_ref.append(res)
    for i in xrange(len_of_data):
        type_name = unpack('=s', x[0])[0]
        len_of_items = unpack('=i', x[1:5])[0]
        res += (deserial(x[:len_of_items]), )
        x = x[len_of_items:]
    list_ref[index] = res
    return res


def pack_list(x):
    type_name = 'l'
    list_id.append(id(x))
    len_of_data = len(x)
    packed = pack('=B', 0) + pack('=i', len_of_data)
    for i in x:
        packed += serial(i)
    len_of_pack = len(packed) + 5
    return pack('=s', type_name) + pack('=i', len_of_pack) + packed

def unpack_list(x):
    x = x[6:]
    len_of_data = unpack('=i', x[:4])[0]
    x = x[4:]
    res = []
    list_ref.append(res)
    for i in xrange(len_of_data):
        len_of_items = unpack('=i', x[1:5])[0]
        res.append(deserial(x[:len_of_items]))
        x = x[len_of_items:]
    return res

def pack_dict(x):
    type_name = 'd'
    list_id.append(id(x))
    len_of_data = len(x)
    packed = pack('=B', 0) + pack('=i', len_of_data)
    for k in x:
        packed += serial(k)
        packed += serial(x[k])
    len_of_pack = len(packed) + 5
    return pack('=s', type_name) + pack('=i', len_of_pack) + packed

def unpack_dict(x):
    x = x[6:]
    len_of_data = unpack('=i', x[:4])[0]
    x = x[4:]
    res = {}
    list_ref.append(res)
    for i in xrange(len_of_data):
        len_of_items = unpack('=i', x[1:5])[0]
        k = deserial(x[:len_of_items])
        x = x[len_of_items:]
        len_of_items = unpack('=i', x[1:5])[0]
        res[k] = deserial(x[:len_of_items])
        x = x[len_of_items:]
    return res

def pack_class(x):
    type_name = 'c'
    packed_flag = pack('=B', 0)
    packed_module = pack_str(x.__module__)
    packed_name = pack_str(x.__class__.__name__)
    list_id.append(id(x))
    packed_dict = pack_dict(x.__dict__)
    len_of_pack = len(packed_module) + len(packed_name) + len(packed_dict) + 6
    return pack('=s', type_name) + pack('=i', len_of_pack) + packed_flag + \
           packed_module + packed_name + packed_dict

def unpack_class(x):
    x = x[6:]
    len_of_module_name = unpack('=i', x[1:5])[0]
    module_name = unpack_str(x[:len_of_module_name])
    x = x[len_of_module_name:]
    len_of_class_name = unpack('=i', x[1:5])[0]
    class_name = unpack_str(x[:len_of_class_name])
    x = x[len_of_class_name:]
    m = importlib.import_module(module_name)
    c = getattr(m, class_name)
    c = c.__new__(c)
    list_ref.append(c)
    len_of_dict = unpack('=i', x[1:5])[0]
    class_dict = deserial(x[:len_of_dict])
    x = x[len_of_dict:]
    c.__dict__ = class_dict
    return c

TYPE_DICT_NAME = {int: 'i',
                  float: 'f',
                  str: 's',
                  tuple: 't',
                  list: 'l',
                  dict: 'd'}

TYPE_DICT_PACK = {int: pack_int,
                  float: pack_float,
                  str: pack_str,
                  tuple: pack_tuple,
                  list: pack_list,
                  dict: pack_dict}

TYPE_DICT_UNPACK = {'i': unpack_int,
                    'f' :unpack_float,
                    's': unpack_str,
                    't': unpack_tuple,
                    'l': unpack_list,
                    'd': unpack_dict,
                    'c': unpack_class}

def serial(x):
    if id(x) in list_id:
        list_id.append(id(x))
        packed = pack('=B', 1) + pack('=i', list_id.index(id(x)))
                 # flag of cycle = 1, number of reference
        if type(x) in TYPE_DICT_NAME:
            pack_name = pack('=s', TYPE_DICT_NAME[type(x)])
        else:
            pack_name = pack('=s', 'c')
        len_of_pack = len(packed) + 5
        res = pack_name + pack('=i', len_of_pack) + packed
    elif type(x) in TYPE_DICT_PACK:
        res = TYPE_DICT_PACK[type(x)](x)
    else:
        res = pack_class(x)
    return res

def serialize(x):
    list_id = []
    return serial(x)

def deserial(x):
    type_name = unpack('=s', x[0])[0]
    is_cycle = unpack('=B', x[5])[0]
    if is_cycle == 1:
        x = x[6:]
        ref = unpack('=i', x[:4])[0]
        list_ref.append(list_ref[ref])
        res = list_ref[ref]
    else:
        res = TYPE_DICT_UNPACK[type_name](x)
    return res

def deserialize(x):
    list_ref = []
    return deserial(x)


class A(object):
    pass

x = A()
x.a = 5
x.c = x

#x1 = ["asd", 78]
#x1.append(x1)
#x = ["qwe", x1, 12.3]

#x = ["asd", 78]
#x.append(x)
#x.append('qwe')
#x.append(x)

#x = ('qwwe',)
#l = [x, x]
#x = (l, l)

#x = {}
#x['a'] = x

#x = ([],)
#x[0].append(x)

print 'x =', x
if isinstance(x, A):
    print 'x.a =', x.a
    print 'x.c =', x.c

s = serialize(x)

print s.__repr__()

ds = deserialize(s)
print 'ds =', ds
if isinstance(ds, A):
    print 'ds.a =', ds.a
    print 'ds.c =', ds.c



