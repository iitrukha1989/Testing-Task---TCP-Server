import datetime
import sqlite3
import socket
import art
import re


class server_socket:
    def __init__(self, ip_value, port_value, db_value):
        print(f'Server IP: {ip_value}\nServer PORT: {port_value}')
        self.server_address = (ip_value, port_value)
        self.count_correct = 0
        self.count_error = 0
        self.db_value = db_value
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.server.bind(self.server_address)
        self.server.listen(1)

    def start_server(self):
        while True:
            try:
                user_value, address_value = self.server.accept()
                print(
                    f'Connecting:\n\tUser address: {address_value[0]}\n\tUser port: {address_value[1]}')
                self.listen_server(user_value)
            except OSError or KeyboardInterrupt:
                break

    def sender_server(self, user_value, data_value):
        print(data_value)
        try:
            user_value.send(data_value.encode('utf-8'))
        except ConnectionResetError:
            pass

    def listen_server(self, user_value):
        try:
            status_value = True
            while status_value:
                data_value = user_value.recv(1024)
                if len(data_value) > 0:
                    message_value = data_value.decode('utf-8')
                    if message_value == 'disconnect':
                        break
                    else:
                        match = re.search(
                            r'\D+\d{4}\D{17}\d\D{3}\d{2}\:\d{2}\:\d{2}\.\d+', message_value)
                        if match:
                            self.count_correct += 1
                            bbbb_value = int(message_value[27:31])
                            nn_value = str(message_value[47:49])
                            time_value = str(message_value[52:64])
                            gg_value = int(message_value[-1:-3:-1][::-1])
                            if gg_value == 00:
                                print(
                                    f'спортсмен, нагрудный номер {bbbb_value:04} прошел отсечку {nn_value} в {time_value} {gg_value:02}')
                            db_connect = sqlite3.connect(self.db_value)
                            db_cursor = db_connect.cursor()
                            sql_value = f"""insert into tcp_data(nomer, id_nomer, time, group_nomer)
                                           values ({bbbb_value:04}, '{nn_value}', '{time_value}', {gg_value:02});"""
                            db_cursor.execute(sql_value)
                            db_connect.commit()
                            db_cursor.close()
                            db_connect.close()
                        else:
                            self.count_error += 1
            self.disconnect_server(user_value)
        except KeyboardInterrupt:
            self.disconnect_server(user_value)

    def disconnect_server(self, user_value):
        print(f"""Total accepted: {self.count_error + self.count_correct}
              Correct accepted: {self.count_correct}
              Error accepted: {self.count_error}""")
        self.server.close()


def main():
    art.tprint('TCP-Server', font='cybersmall')
    print('Start server on time:', datetime.datetime.today().strftime('%H:%M'))
    server_socket('localhost', 7000, 'tcp_database.db').start_server()
    print('Server disconnect on time:',
          datetime.datetime.today().strftime('%H:%M'))


if __name__ == '__main__':
    main()
