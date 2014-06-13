#!/usr/bin/env python3

import asyncio
import argparse


def split_message(data):
    priority, message = data.split(b'>', 1)
    # Section 6.2.1 of RFC5424 explains this
    priority = int(priority[1:]) % 8
    message = message[:-1]  # no NUL today folks
    return priority, message


class Logger:
    def __init__(self, fontpath='/usr/share/figlet/fonts/big.flf'):
        self.hardblank, self.letters, self.height = self.load_big_font(fontpath)

    def load_big_font(self, fontpath):
        with open(fontpath) as f:
            header = f.readline().split(' ')
            hardblank = header[0][-1]
            height = int(header[1])
            comments = int(header[5])

            while comments:
                f.readline()
                comments -= 1

            letters = {}
            # I am terribly sorry, but for simplicity's sake, only support printable ASCII characters.
            for i in range(128 - 32):
                big_letter = [f.readline()[:-1].replace('@', '') for i in range(height)]
                letters[i+32] = big_letter

        return hardblank, letters, height

    def log(self, message, priority=5):
        # quick and dirty parsing, because who wants to read a huge date?
        meta, message = message.split(b']', 1)
        meta = meta + b']'
        message = message[1:]
        if priority <= 4:
            message = self.embiggen(message)
        message = b':'.join([meta, message])
        with open('log.out', 'wb') as f:
            f.write(message)
            f.write(b'\n')

    def embiggen(self, message):
        lines = [[] for i in range(self.height)]
        for c in message:
            for i, line in enumerate(self.letters[c]):
                lines[i].append(line.replace(self.hardblank, ' '))

        sentence = '\n'
        for line in lines:
            chunk = ''.join(line)
            if chunk:
                sentence += chunk + '\n'

        return sentence.encode('utf8')


class SysLolUDP:
    def connection_made(self, transport):
        self.transport = transport
        self.logger = Logger()

    def datagram_received(self, data, addr):
        priority, message = split_message(data)
        self.logger.log(message, priority=priority)

    def connection_refused(self, exc):
        print('Connection refused:', exc)

    def connection_lost(self, exc):
        print('stop', exc)


def start_server(loop, addr):
    t = asyncio.Task(loop.create_datagram_endpoint(
        SysLolUDP, local_addr=addr))
    loop.run_until_complete(t)


def parse_args():
    parser = argparse.ArgumentParser(prog='syslol')
    parser.add_argument('--port', type=int, default=514,
                        help='UDP port to listen on. Default is standard 514')
    parser.add_argument('--interface', type=str, default='0.0.0.0',
                        help='Interface to bind on. Default is 0.0.0.0')

    return parser.parse_args()

if __name__ == '__main__':
    options = parse_args()
    loop = asyncio.get_event_loop()
    start_server(loop, (options.interface, options.port))
    loop.run_forever()
