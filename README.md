# Assistance Certificate Generator

 A simple utility to make assistant certificates and save them on PDF. 

 <img width="995" alt="Screenshot 2023-07-06 at 00 16 54" src="https://github.com/emi420/assistancecert/assets/1226194/90587e42-7948-4b14-a632-5cf52db09dd8">

## Install

Just create and activate a virtualenv, then install requirements typing `pip install -r reqs.txt`

## Usage 

1. Edit `data/list.csv` with your own data
2. Edit `assets/base.png` with your own certificate image
3. If you want to modify sizes, positions, fonts, etc, edit `config.py`
4. Run `python certgen.py` 

# CSV

The CSV file should have two columns, `name` and  `field 2`, like this:

| Name          | Field 2       |
| ------------- | ------------- |
| Annie García  | Student       |

## Running as a webserver

You can also run a webserver for creating certificates on demand, setting the
`SERVER` config variable to `True` and then running `python certgen.py`

This will start a webserver to which you can send requests with the fields:

`http://localhost:8001?name=Annie Garcia&field_2=Student`

PDF files will be saved in the `OUT_DIR` directory.

# Config

Name, _field 2_ and a random hash (id) will be rendered over the background image (base file).

* `NAME_FONT` - Path for using when rendering the the `name`
* `FIELD_2_FONT` - Path for using when rendering the the `field 2`
* `ID_FONT` - Path for using when rendering the the `id`
* `FIELD_2_PREFIX` - A prefix for the _field 2_
* `NAME_PREFIX` - A prefix for the name
* `FILENAME` - Field to use for the PDF filename (`name` or `field_2`)
* `FILENAME_HASH` - Include the id (random hash) into the filename
* `UPPERCASE` - Transform texts to uppercase
* `TEXT_LEFT_POSITION` - Position from the left for texts (in pixels)
* `NAME_TOP_POSITION` - Position from the top for name (in pixels)
* `FIELD_2_TOP_POSITION` - Position from the top for _field_2_ (in pixels)
* `ID_TOP_POSITION` - Position from the top for the id text (in pixels)
* `IMAGE_WIDTH` - Width of the background image (in pixels)
* `IMAGE_HEIGHT` - Height of the background image (in pixels)
* `BASE_FILE` - Path of the background image
* `OUT_DIR` - Output directory for PDF certificate files
* `OUT_PREFIX` - A prefix for PDF certificate files
* `SERVER` - Run as a webswerver
* `SERVER_PORT` - Port when using the web server

## License

You may use this project under the terms of either the MIT License or the GNU General Public License (GPL) Version 3.

(c) 2019-2024 Emilio Mariscal
