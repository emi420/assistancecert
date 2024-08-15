#!/usr/bin/python
# -*- coding: utf-8 -*-

''' 
 Assistance Certificate Generator

 You may use any Assistance Certificate Generator project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2019 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    Assistance Certificate Generator
    
    A simple utility to make assistant certificates and save them on PDF. 
 
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

'''
create: generate certificate
'''
def create(name, field_2, id_hash):

    img_base = Image.open(BASE_FILE, 'r')
    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), (255,255,255))

    img.paste(img_base, (0,0))
    draw = ImageDraw.Draw(img)

    name_prefixed = NAME_PREFIX + name
    field_2_prefixed = FIELD_2_PREFIX + field_2

    name_w, name_h = draw.textsize(name_prefixed, NAME_FONT)
    field_2_w, field_2_h = draw.textsize(field_2_prefixed, FIELD_2_FONT)
    id_w, id_h = draw.textsize(id_hash, ID_FONT)

    if TEXT_LEFT_POSITION:
        draw.text(( IMAGE_WIDTH - 100, IMAGE_HEIGHT - 55), id_hash, (170,170,170), font=ID_FONT)
        draw.text(( TEXT_LEFT_POSITION, NAME_TOP_POSITION), name_prefixed, (0,0,0), font=NAME_FONT)
        draw.text(( TEXT_LEFT_POSITION, FIELD_2_TOP_POSITION), field_2_prefixed, (0,0,0), font=FIELD_2_FONT)
    else:
        draw.text(( (IMAGE_WIDTH - id_w) / 2, ID_TOP_POSITION), id_hash, (170,170,170), font=ID_FONT)
        draw.text(( (IMAGE_WIDTH - name_w) / 2, NAME_TOP_POSITION), name_prefixed, (0,0,0), font=NAME_FONT)
        draw.text(( (IMAGE_WIDTH - field_2_w) / 2, FIELD_2_TOP_POSITION), field_2_prefixed, (0,0,0), font=FIELD_2_FONT)

    del draw

    normalized_name = re.sub('[^A-Za-z0-9]+', '', name)
    img.save(OUT_DIR + (normalized_name if FILENAME == "name" else field_2)  + ("-" + id_hash if FILENAME_HASH else "") + ".pdf", "PDF")

def create_from_csv(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:

            name = row[0]
            field_2 = row[1]

            name = row[0].upper() if UPPERCASE else row[0]
            field_2 = row[1].upper() if UPPERCASE else row[1]

            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t Name: {name} Field 2: {field_2}')
                create(name, field_2.upper(), OUT_PREFIX + secrets.token_hex(nbytes=2))
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
            name = params.get("name")[0].upper() if UPPERCASE else params.get("name")[0]
            field_2 = params.get("field_2")[0].upper() if UPPERCASE else params.get("field_2")[0]
            create(name=name, field_2=field_2, id_hash=OUT_PREFIX + secrets.token_hex(nbytes=2))
            return

def main():
    if SERVER:
        try:
            server = HTTPServer(('', SERVER_PORT), APIServer)
            print ('Started httpserver on port ' + str(SERVER_PORT))
            server.serve_forever()
            
        except KeyboardInterrupt:
            print ('^C received, shutting down server')
            server.socket.close()
    else:
        create_from_csv("./data/list.csv")


if __name__ == '__main__':
    main()
