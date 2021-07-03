#!/usr/bin/env python3

import json
import argparse
import requests
from bs4 import BeautifulSoup

class EasynewsData:
    member_url = "https://members.easynews.com/"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.data = {}
        self.status = "unqueried"

    def query(self):
        r = requests.get(self.member_url, auth=(self.username, self.password))

        if r.status_code != 200:
            self.status = "errored"
            return

        soup = BeautifulSoup(r.text, 'html.parser')
        self.data['remaining'] = float(soup.find("div", class_="block").strong.string)
        self.data['username'] = soup.find("span", id="Login").strong.string
        self.status = "complete"

    def to_json(self):
        return json.dumps(self.data)

    def status(self):
        return self.status
        

def main(args):

    en = EasynewsData(args.username, args.password)
    en.query()
    print(en.to_json())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--user", action="store", dest="username")
    parser.add_argument("-p", "--pass", action="store", dest="password")

    args = parser.parse_args()
    main(args)
