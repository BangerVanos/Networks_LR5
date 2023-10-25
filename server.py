import socket
import argparse
import logging
import datetime
import os
import json


arg_parser = argparse.ArgumentParser(prog='Simple Server-Client in Python',
                                     description='That\'s a server side for server-client project',
                                     epilog='I hope it will work..')
arg_parser.add_argument('-host', '--hostname', type=str, default='localhost',
                        help='Hostname for this sever (default is localhost)')
arg_parser.add_argument('-p', '--port', type=int, default=8080,
                        help='Port for this sever (default is 8080)')
arg_parser.add_argument('-d', '--directory', type=str, default='',
                        help='Directory from which server sends files')


class Server:
    DEFAULT_HDRS = {'200': 'HTTP 1.1 200 OK\r\n Content-Type: text/html; charset: utf-8\r\n\r\n',
                    '404': 'HTTP 1.1 404 OK\r\n Content-Type: text/html; charset: utf-8\r\n\r\n',
                    '500': 'HTTP 1.1 500 OK\r\n Content-Type: text/html; charset: utf-8\r\n\r\n'}

    def __init__(self, hostname, port, directory):
        self.hostname = hostname
        self.port = port
        self.directory = directory

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        logging.basicConfig(filename='server_log.log', filemode='a', level=logging.INFO)

    def start_server(self):
        self.server.bind((self.hostname, self.port))
        self.server.listen(4)
        print('START SERVER')
        logging.info(f'{datetime.datetime.now()} START SERVER')
        try:
            while True:
                client, address = self.server.accept()
                data = client.recv(1024).decode('utf-8')
                data_info = data.split(' ')
                method = data_info[0]
                if method == 'GET':
                    path = os.path.join(os.path.normpath(self.directory),
                                        os.path.normpath(data_info[1].replace('/', '')))
                    response = self.handle_get(path)
                elif method == 'POST':
                    data = data_info[1]
                    response = self.handle_post(data)
                elif method == 'OPTIONS':
                    response = (self.DEFAULT_HDRS['200'] +
                                'Access-Control-Allow-Methods: GET, POST, OPTIONS').encode('utf-8')
                    logging.info(f'{datetime.datetime.now()} USED OPTIONS METHOD')
                else:
                    response = (self.DEFAULT_HDRS['500'] + 'WARNING: Method does not exist').encode('utf-8')
                    logging.warning(f'{datetime.datetime.now()} METHOD {method} DOES NOT EXIST')
                client.send(response)
                client.shutdown(socket.SHUT_WR)
        except KeyboardInterrupt:
            self.server.close()
            logging.warning(f'{datetime.datetime.now()} SERVER SHUTDOWN')
            print('Server shutdown')

    def handle_get(self, path):
        try:
            with open(path, 'rb') as file:
                response = file.read()
            logging.info(f'{datetime.datetime.now()} SEND FILE TO CLIENT WITH PATH {path}')
            print(self.DEFAULT_HDRS['200'] + path)
            return self.DEFAULT_HDRS['200'].encode('utf-8') + response
        except FileNotFoundError:
            logging.error(f'{datetime.datetime.now()} CANNOT SEND FILE WITH PATH {path}.'
                          f' FILE DOES NOT EXIST')
            print(self.DEFAULT_HDRS['404'] + path + 'ERROR: File not found')
            return (self.DEFAULT_HDRS['404'] + path + 'ERROR: File not found').encode('utf-8')

    def handle_post(self, data):
        try:
            headers = json.loads(data)
        except json.decoder.JSONDecodeError as err:
            logging.error(f'{datetime.datetime.now()} CANNOT HANDLE DATA WITH JSON {data}. {err}')
            return (self.DEFAULT_HDRS['500'] + f' {err}').encode('utf-8')
        logging.info(f'{datetime.datetime.now()} GET DATA FOR POST {data}')
        for key in headers:
            print(f'{key} - {headers[key]}')
        logging.info(f'{datetime.datetime.now()} HANDLED DATA WITH JSON {data}')
        return (self.DEFAULT_HDRS['200'] + f'POST: {data}').encode('utf-8')


if __name__ == '__main__':
    args = arg_parser.parse_args()
    server = Server(args.hostname, args.port, args.directory)
    server.start_server()
