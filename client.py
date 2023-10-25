import socket
import argparse


arg_parser = argparse.ArgumentParser(prog='Simple Server-Client in Python',
                                     description='That\'s a client side for server-client project',
                                     epilog='I hope it will work..')
arg_parser.add_argument('-host', '--hostname', type=str, default='localhost',
                        help='Hostname for this sever (default is localhost)')
arg_parser.add_argument('-p', '--port', type=int, default=8080,
                        help='Port for this sever (default is 8080)')
arg_parser.add_argument('-f', '--file', type=str, default='.',
                        help='Directory from which server sends files')
arg_parser.add_argument('-m', '--method', type=str, default='GET',
                        help='Method which is used during HTTP request')
arg_parser.add_argument('-msg', '--message', type=str, default='',
                        help='Message(JSON) to post on server')


if __name__ == '__main__':
    args = arg_parser.parse_args()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((args.hostname, args.port))
    if args.method == 'GET':
        client.send(f'GET {args.file}'.encode('utf-8'))
    elif args.method == 'POST':
        client.send(f'POST {args.message}'.encode('utf-8'))
    elif args.method == 'OPTIONS':
        client.send(f'OPTIONS'.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    print(f'You recieved: {response}')

