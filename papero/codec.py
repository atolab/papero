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
    return Property(k,v)


def encode_sequence(buf, xs, encoder):
    buf.put_vle(len(xs))
    for x in xs:
        encoder(buf, x)

def  decode_sequence(buf, decoder):    
    n = buf.get_vle()   
    xs = []
    for _ in range(0, n):
        xs.append(decoder(buf))
    return xs

def encode_properties(buf, ps):
    if len(ps) != 0:    
        encode_sequence(buf, ps, encode_property)

def decode_properties(buf):
    return decode_sequence(buf, decode_property)
    