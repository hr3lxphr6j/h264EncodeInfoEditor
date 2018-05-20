import sys
import getopt

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


def pipe_v2(_input, _output, _str):
    # Write SEI NAL as first NAL
    _output.write(enc_sei_user_data(uuid, _str))
    # Parse input stream
    buf = b''
    while 1:
        b = _input.read(1)
        if len(b) == 0:
            _output.write(buf)
            break
        else:
            buf += b

        if buf[-3:] == b'\x00\x00\x01':  # New NAL
            if buf[-4::1] == b'\x00':  # Start code is 0x00 0x00 0x00 0x01
                _output.write(buf[:-4])  # flush last nal to output
                buf = buf[-4:] + _input.read(2)
            else:  # Start code is 0x00 0x00 0x01
                _output.write(buf[:-3])  # flush last nal to output
                buf = buf[-3:] + _input.read(2)
            if buf[-2:] == b'\x06\x05':  # sei user data
                length = 0
                while 1:
                    b = _input.read(1)
                    if b != b'\xff':
                        length += int.from_bytes(b, byteorder="little")
                        break
                    else:
                        length += 255
                print("[Original Writing library]: " + _input.read(length + 1)[16:-2].decode(), file=sys.stderr)
                buf = b''
                pass


def print_help():
    print("""A script to edit H.264 encoder information.
usage: h264EncodeInfoEditor.py [options]
    
[Options]
-h  print this help.
-i  input h264 bit stream, '-' will read stream from std in.
-o  output h264 bit stream, '-' will write stream from std out.
-s  info what you want write.
""", file=sys.stderr)


def parse_arg(argv: list) -> dict:
    try:
        opts, args = getopt.getopt(argv, 'i:o:s:h')
    except getopt.GetoptError:
        print_help()
        exit(2)
    flag = {}
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            exit(0)
        elif opt == '-i':
            flag['input'] = arg
        elif opt == '-o':
            flag['output'] = arg
        elif opt == '-s':
            flag['str'] = arg
        pass
    return flag


def main():
    if len(sys.argv[1:]) == 0:
        print_help()
        exit(1)
    flag = parse_arg(sys.argv[1:])
    i = sys.stdin.buffer if flag['input'] == "-" else open(flag['input'], 'rb')
    o = sys.stdout.buffer if flag['output'] == "-" else open(flag['output'], 'wb')
    pipe_v2(i, o, flag['str'])


if __name__ == '__main__':
    main()
