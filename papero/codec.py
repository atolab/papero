# This file contains all message codec necessary
# for the client. Notice that it does not necessarily
# provide both encoder and decored for all messages since
# in some cases messages will either only be sent or only received.

import logging
from .property import Property


def encode_property(buf, p):
    buf.put_string(p.key)
    buf.put_string(p.value)


def decode_property(buf):
    k = buf.get_string()
    v = buf.get_string()
    return Property(k, v)


def encode_sequence(buf, xs, encoder):
    buf.put_vle(len(xs))
    for x in xs:
        encoder(buf, x)


def decode_sequence(buf, decoder):
    n = buf.get_vle()
    xs = []
    for _ in range(0, n):
        xs.append(decoder(buf))
    return xs


def encode_properties(buf, ps):
    s = ''
    length = len(ps)
    if length > 0:
        for i in range(0, length):
            s = s + ps[i].key + '=' + ps[i].value
            if i < length - 1:
                s = s + ';'
        buf.put_string(s)


def decode_properties(buf):
    ps = []
    s = buf.get_string()
    if len(s) == 0:
        return ps
    s = s.split(';')
    for ss in s:
        p = ss.split('=')
        if len(p) == 1:
            p.append('')
        ps.append(Property(p[0], p[1]))
    return ps
