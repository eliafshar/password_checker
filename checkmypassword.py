import requests
import hashlib
import sys
import getpass  # Import the getpass module

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwnd_api_check(password):
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    firt5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(firt5_char)
    return get_password_leaks_count(response, tail)

def main():
    passwords = getpass.getpass("Enter passwords (separated by spaces): ").split()
    for idx, password in enumerate(passwords, start=1):
        count = pwnd_api_check(password)
        if count:
            print(f"The {ordinal_number(idx)} password was found {count} times... You should probably change your password")
            print("Here are some tips to create a secure password:")
            print("- Use a mix of uppercase and lowercase letters")
            print("- Include numbers and special characters")
            print("- Avoid using easily guessable information like birthdays or names")
            print("- Make it at least 12 characters long")
            print("- Use a passphrase or a combination of random words")
        else:
            print(f"The {ordinal_number(idx)} password was NOT found. Carry on!")

def ordinal_number(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

if __name__ == '__main__':
    main()
