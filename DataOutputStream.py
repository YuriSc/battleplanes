
"""
Writing to Java DataInputStream format.
"""

import struct


class StreamToSocketWriter:
    def __init__(self, socket):
        self.socket = socket

    def write(self, data):
        if isinstance(data, str):
            self.socket.sendall(data.encode())
        else:
            self.socket.sendall(data)


class DataOutputStream:
    def __init__(self, stream):
        self.stream = StreamToSocketWriter(stream)

    def write_boolean(self, bool):
        self.stream.write(struct.pack('?', bool))

    def write_byte(self, val):
        self.stream.write(struct.pack('b', val))

    def write_unsigned_byte(self, val):
        self.stream.write(struct.pack('B', val))

    def write_char(self, val):
        self.stream.write(struct.pack('>H', ord(val)))

    def write_double(self, val):
        self.stream.write(struct.pack('>d', val))

    def write_float(self, val):
        self.stream.write(struct.pack('>f', val))

    def write_short(self, val):
        self.stream.write(struct.pack('>h', val))

    def write_unsigned_short(self, val):
        self.stream.write(struct.pack('>H', val))

    def write_long(self, val):
        self.stream.write(struct.pack('>q', val))

    def write_utf(self, string):
        data = string.encode()
        self.stream.write(struct.pack('>H', len(data)))
        self.stream.write(data)

    def write_int(self, val):
        self.stream.write(struct.pack('>i', val))