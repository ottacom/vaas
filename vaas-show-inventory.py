#!/usr/bin/python
import argparse
from lib import loadconfig
from lib import tinydbengine

loadconfig.load()
tinydbengine.db_init_database()
tinydbengine.db_show_inventory()
