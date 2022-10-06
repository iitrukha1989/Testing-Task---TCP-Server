import telnetlib
import datetime
import random
import string
import time


class client_socket:
    def __init__(self, ip_value, port_value):
        self.client = telnetlib.Telnet(ip_value, port_value)
        self.client.get_socket()

    def sender_client(self, text_value):
        try:
            self.client.write(text_value.encode('utf-8'))
            time.sleep(0.1)
        except ConnectionAbortedError:
            pass

    def connect_client(self):
        try:
            status_client = True
            while status_client:
                request_value = self.generator_data()
                while request_value == '':
                    request_value = self.generator_data()
                if request_value.lower() == 'disconnect':
                    self.sender_client(request_value)
                    break
                else:
                    self.sender_client(request_value)
            self.client.close()
        except KeyboardInterrupt:
            pass

    def generator_data(self):
        return random.choice([self.genarator_payload(), self.generator_empty(), self.generator_random()])

    def genarator_payload(self):
        bbbb_value = random.randint(1, 9999)
        nn_value = str(random.choice(
            list(string.ascii_uppercase)) + str(random.randint(1, 9)))
        gg_value = random.randint(0, 99)
        time_value = datetime.datetime.today().strftime("%H:%M:%S.%f")
        return f'спортсмен, нагрудный номер {bbbb_value:04} прошел отсечку {nn_value} в {time_value} {gg_value:02}'

    def generator_empty(self):
        return ''

    def generator_random(self):
        check_value = random.randint(1, 500)
        if check_value == 500:
            return 'disconnect'
        else:
            list_value = list()
            for _ in range(random.randint(1, 5)):
                list_value.append(''.join([tmp_value for tmp_value in random.sample(
                    list(string.ascii_letters), random.randint(3, 9))]))
            return ' '.join(list_value)


def main():
    client_socket('localhost', 7000).connect_client()


if __name__ == '__main__':
    main()
