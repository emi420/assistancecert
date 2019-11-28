#!/usr/bin/python
# -*- coding: utf-8 -*-

''' 
 Certificate Generator

 You may use any Certificate Generator project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2019 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    Certificate Generator
    
    Generate assistance or completion certificates
 
'''

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from PIL import Image, ImageDraw
from urllib.parse import urlparse, parse_qs
import secrets
import csv
import re
from config import *

import http.server

Handler = http.server.SimpleHTTPRequestHandler

SERVER = False

'''
create: generate certificate
'''
def create(name, role, id_hash):

    img_base = Image.open(BASE_FILE, 'r')
    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), (255,255,255))

    img.paste(img_base, (0,0))
    draw = ImageDraw.Draw(img)

    name = NAME_PREFIX + name
    role = ROLE_PREFIX + role

    name_w, name_h = draw.textsize(name, NAME_FONT)
    role_w, role_h = draw.textsize(role, ROLE_FONT)
    id_w, id_h = draw.textsize(id_hash, ID_FONT)

    draw.text(( (IMAGE_WIDTH - id_w) / 2, ID_TOP_POSITION), id_hash, (170,170,170), font=ID_FONT)
    draw.text(( (IMAGE_WIDTH - name_w) / 2, NAME_TOP_POSITION), name, (0,0,0), font=NAME_FONT)
    draw.text(( (IMAGE_WIDTH - role_w) / 2, ROLE_TOP_POSITION), role, (0,0,0), font=ROLE_FONT)

    del draw

    normalized_name = re.sub('[^A-Za-z0-9]+', '', name)
    img.save(OUT_DIR + normalized_name + "-" + id_hash + ".pdf", "PDF")

def create_from_csv(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:

            name = row[0]
            role = row[1]

            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t Name: {name} Role: {role}')
                create(name, role.upper(), OUT_PREFIX + secrets.token_hex(nbytes=2))
                line_count += 1
        print(f'Processed {line_count} lines.')

'''
APIServer: web server 
'''
class APIServer(BaseHTTPRequestHandler):

    def do_GET(self):
               
        mime = "text/html"

        self.send_response(200)
        self.send_header("Content-type", mime)
        self.send_header('Allow', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        params = parse_qs(urlparse(self.path).query)

        if params:
            name = params.get("name")[0]
            role = params.get("role")[0]
            create(name=name, role=role)
            return

def main():
    if SERVER:
        try:
            server = HTTPServer(('', PORT), APIServer)
            print ('Started httpserver on port ' + str(PORT))
            server.serve_forever()
            
        except KeyboardInterrupt:
            print ('^C received, shutting down server')
            server.socket.close()
    else:
        create_from_csv("./data/list.csv")


if __name__ == '__main__':
    main()
