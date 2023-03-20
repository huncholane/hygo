from db_connection import django_cnx
import os
import sys
import base64


if len(sys.argv) != 3:
    print('usage: generate_referal.py <username> <password>')
    exit()

username, password = sys.argv[1:]
stmt = f'SELECT * FROM home_account WHERE username = "{username}" AND password = "{password}"'
account = django_cnx.query(stmt)
if len(account) == 0:
    print('Account does not exist')
    exit()

code = base64.b64encode(f'{username}:{password}'.encode())
link = f'https://ghostsystems.io/referral?code={code.decode()}'
print(link)
