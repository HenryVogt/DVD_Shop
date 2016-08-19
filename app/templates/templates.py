# -*- coding: utf-8 -*-
import os
import re, math

import config

templates = {}

for f_name in os.listdir(config.TEMPLATE_DIR):
    rel_path = os.path.join(config.TEMPLATE_DIR, f_name)

    if f_name.endswith(config.TEMPLATE_FILE_EXT) and os.path.isfile(rel_path):
        templates[f_name[:-len(config.TEMPLATE_FILE_EXT)]] = file(rel_path, "r").read()
