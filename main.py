import requests
import os
import json
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse


def shorten_link(link, token):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        'Authorization': token
    }
    payload = {
        "long_url": link
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink


def count_clicks(bitlink, token):
    url = 'https://api-ssl.bitly.com/v4/bitlinks/\
{0}/clicks/summary'.format(bitlink)
    headers = {
        'Authorization': token
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(url, token):
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{0}'.format(url)
    headers = {
        'Authorization': token
    }
    response = requests.get(url, headers=headers)
    return response.ok


def main():
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
    link_components = f"{link_components.netloc}{link_components.path}"
    if is_bitlink(link_components, token):
        try:
            print(f"Кол-во кликов - {count_clicks(link_components, token)}")
        except requests.exceptions.HTTPError as error:
            exit("Error:\n{0}".format(error))
    else:
        try:
            print(shorten_link(link, token))
        except requests.exceptions.HTTPError as error:
            exit("Error:\n{0}".format(error))


if __name__ == '__main__':
    load_dotenv()
    main()
