import requests
import os
import json
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse
import sys


def shorten_link(link, token):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        'Authorization': f"Bearer {token}"
    }
    payload = {
        "long_url": link
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink


def count_clicks(bitlink, token):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{0}/clicks/summary".format(
        bitlink
    )
    headers = {
        'Authorization': f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(url, token):
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{0}'.format(url)
    headers = {
        'Authorization': f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='short links bitly'
    )
    parser.add_argument('-link', help='long link')
    args = parser.parse_args()
    if args.link:
        link = args.link
    else:
        link = input("Input link - ")
    token = os.getenv('BITLY_TOKEN')
    link_components = urlparse(link)
    short_link = f"{link_components.netloc}{link_components.path}"
    try:
        if is_bitlink(short_link, token):
            print(f"Кол-во кликов - {count_clicks(short_link, token)}")
        else:
            print(shorten_link(link, token))
    except requests.exceptions.HTTPError as error:
        sys.exit("Вы ввели неправильную ссылку или неверный токен.")


if __name__ == '__main__':
    main()
