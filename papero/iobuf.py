DEFAULT_IOBUF_SIZE = 1024 * 64


class IOBufException(IOError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'IOBufException: {}'.format(self.msg)


class IOBuf(object):

    def __init__(self, capacity=None, init_with=None):
        self.read_pos = 0
        self.write_pos = 0
        
        if init_with is None:
            if capacity is None:
                self.capacity = DEFAULT_IOBUF_SIZE                            
            else: 
                self.capacity = len(init_with)
            self.limit = self.capacity
            self.buf = bytearray(self.capacity)        
        else:
            ilen = len(init_with)
            self.buf = bytearray(init_with)        
            self.write_pos = ilen
            if capacity is None:        
                self.capacity = ilen
            else:
                self.capacity = max(capacity, len(init_with))

    
    @staticmethod
    def from_bytes(bs):        
        return IOBuf(init_with=bs)

    def __str__(self):
        return 'IOBuf(read_pos:{}, write_pos:{}, capacity:{})'.format(self.read_pos,  self.write_pos, self.capacity)

    def hex_dump(self):
        hd = ''
        for i in range(0, self.write_pos):            
            hd += ":" + hex(self.buf[i])
        print(hd)

    def clear(self):
        self.read_pos = 0
        self.write_pos = 0
        self.limit = self.capacity

    def reset_read_pos(self):
        self.read_pos = 0

    def put(self, b):        
        if self.write_pos == self.capacity:            
            self.buf.extend(bytes(DEFAULT_IOBUF_SIZE))
            self.capacity += DEFAULT_IOBUF_SIZE
        self.buf[self.write_pos] = b
        self.write_pos += 1

    def get(self):
        if self.read_pos < self.write_pos:
            v = self.buf[self.read_pos]
            self.read_pos += 1
            return v
        else:
            raise IOBufException('Cannot read beyond write position (read_pos : {}, write_pos: {})'.format(
                self.read_pos, self.write_pos))

    def put_vle(self, v):
        if v < 0x7f:
            self.put(v)
        else:
            c = (v & 0x7f) | 0x80
            r = v >> 7
            self.put(c)
            self.put_vle(r)

    def __extract_vle(self, cv, n):
        c = self.get()
        nv = ((c & 0x7f) << (7*n)) | cv
        if c > 0x7f:
            return self.__extract_vle(nv, n+1)
        else:
            return nv

    def get_vle(self):
        return self.__extract_vle(0, 0)

    def put_bytes(self, bs):
        l = len(bs)
        self.put_vle(l)
        i = self.write_pos
        j = i + l 
        self.buf[i:j] = bs
        self.write_pos += l

    def get_bytes(self):
        n = self.get_vle()
        i = self.read_pos
        self.read_pos += n
        return self.buf[i:self.read_pos]
        
    def put_string(self, s):
        if s == "":
            s = " "
        self.put_bytes(s.encode())

    def get_string(self):
        bs = self.get_bytes()
        return str(bs.decode())

    def get_raw_bytes(self):
        return self.buf[self.read_pos:self.write_pos]        

    def get_n_bytes(self, n):
        i = self.read_pos
        j = i + n
        self.read_pos += n        
        return self.buf[i:j]

    def append(self, other):
        for i in range(other.read_pos, other.write_pos):
            self.put(other.buf[i])
