import sqlite3


def sql_request(request_value):
    db_connect = sqlite3.connect('tcp_database.db')
    db_cursor = db_connect.cursor()
    # sql_value = """Create table tcp_data(
    #             nomer int,
    #             id_nomer nvarchar(2),
    #             time nvarchar(13),
    #             group_nomer int
    #             );"""
    if request_value == 1:
        sql_value = 'select * from tcp_data'
    else:
        sql_value = 'delete from tcp_data'
    db_cursor.execute(sql_value)
    for tmp_value in db_cursor:
        print(tmp_value)
    db_connect.commit()
    db_cursor.close()
    db_connect.close()


def main():
    print('SQL type request:\n1 - Select\n2 - Delete')
    try:
        request_value = int(input())
        while request_value not in [1, 2]:
            print('SQL type request:\n1 - Select\n2 - Delete')
            request_value = int(input())
        sql_request(request_value)
    except ValueError:
        main()


if __name__ == '__main__':
    main()
