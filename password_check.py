import requests
import hashlib
import sys



def request_api_data(query_char):
    url = f'https://api.pwnedpasswords.com/range/{query_char}'
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching:{res.status_code}, check the api and try again ')
    return res

def get_password_leaks_count(hashes, hast_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    return next((count for h, count in hashes if h == hast_to_check), 0)

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        if count := pwned_api_check(password):
            print(f'{password} was found {count} times .. you should probably change you password')
        else:
            print(f'{password} was not found. Carry On!')
    return 'done'
main(sys.argv[1:])