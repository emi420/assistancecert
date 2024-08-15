from PIL import ImageFont


NAME_FONT = ImageFont.truetype("assets/BarlowCondensed-SemiBold.ttf", 90)
FIELD_2_FONT = ImageFont.truetype("assets/BarlowCondensed-Thin.ttf", 47)
ID_FONT = ImageFont.truetype("assets/BarlowCondensed-Thin.ttf", 30)
TEXT_LEFT_POSITION = 515

FIELD_2_PREFIX = "DNI "
NAME_PREFIX = ""

# FILENAME = "name"
FILENAME = "field_2"
FILENAME_HASH = False

UPPERCASE = True

ID_TOP_POSITION = 1200
NAME_TOP_POSITION = 390
FIELD_2_TOP_POSITION = 510

IMAGE_WIDTH = 1650
IMAGE_HEIGHT = 1275

BASE_FILE = "assets/base.png"
OUT_DIR = "out/"
OUT_PREFIX = ""

SERVER = True
SERVER_PORT = 8001
