#!/usr/bin/env python3

import sys
from argparse import ArgumentParser

uuid = b'\xDC\x45\xE9\xBD\xE6\xD9\x48\xB7\x96\x2C\xD8\x20\xD9\x23\xEE\xEF'
sei_user_data_header = b'\x00\x00\x00\x01\x06\x05'


def enc_sei_user_data(_uuid: bytes, _data: str) -> bytes:
    data_byte = _data.encode()
    data_length = len(data_byte) + len(_uuid) + 1
    sei_length = b''
    for _ in range(data_length // 255):
        sei_length += b'\xff'
    sei_length += int.to_bytes(data_length % 255, byteorder="little", length=1)
    return sei_user_data_header + sei_length + _uuid + data_byte + b'\x00\x80'


def pipe_v3(_input, _output, _str):
    _flag = 0
    '''
    0
    
    1   =>  00
    2   =>  00 00
    3   =>  00 00 00

    6   =>  00 00 01
    7   =>  00 00 00 01
    '''
    buf = b''
    _output.write(enc_sei_user_data(uuid, _str))
    while 1:
        b = _input.read(1)
        if len(b) == 0:
            # EOF
            _output.write(buf)
            break

        buf += b

        if b == b'\x00':
            if _flag in [0, 1, 2]:
                _flag += 1
            else:
                _flag = 0
                _output.write(buf)
                buf = b''
                continue
        elif b == b'\x01':
            if _flag == 2:
                _flag = 6
            elif _flag == 3:
                _flag = 7
            else:
                _flag = 0
                _output.write(buf)
                buf = b''
                continue
        else:
            _flag = 0
            _output.write(buf)
            buf = b''
            continue

        if _flag in [6, 7]:
            # find NALU
            b = _input.read(2)
            buf += b
            if len(b) < 2:
                # EOF
                _output.write(buf)
                break
            if b != b'\x06\x05':
                _flag = 0
                _output.write(buf)
                continue
            length = 0
            while 1:
                b = _input.read(1)
                if b != b'\xff':
                    length += int.from_bytes(b, byteorder="little")
                    break
                else:
                    length += 255
            print("[Original Writing library]: {}".format(_input.read(length + 1)[16:-2].decode()), file=sys.stderr)
            _flag = 0
            buf = b''
            break
    while 1:
        b = _input.readlines()
        if len(b) == 0:
            break
        _output.writelines(b)
    _input.close()
    _output.close()


def _open_input(s):
    if s == '-':
        return sys.stdin.buffer
    else:
        return open(s, 'rb')


def _open_output(s):
    if s == '-':
        return sys.stdout.buffer
    else:
        return open(s, 'wb')


def parse_args():
    parser = ArgumentParser(prog='h264EncodeInfoEditor', description='A script to edit H.264 encoder information')
    parser.add_argument('-i', '--input', required=True, type=_open_input,
                        help='input h264 bit stream, \' - \' will read stream from stdin')
    parser.add_argument('-o', '--output', required=True, type=_open_output,
                        help='output h264 bit stream, \' - \' will write stream from stdout')
    parser.add_argument('-s', '--string', required=True, type=str, help='info what you want write')
    return parser.parse_args()


def main():
    args = parse_args()
    pipe_v3(args.input, args.output, args.string)


if __name__ == '__main__':
    main()
