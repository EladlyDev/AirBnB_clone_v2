#!/usr/bin/python3
""" generates a .tgz archive from the contents of the web_static """
from fabric.api import *
from datetime import datetime
import os


def do_pack():
    """ packs the webs_static and puts it on the server """
    arch_name = "web_static_" + datetime.now().strftime("%Y%m%d%H%M%S") \
        + ".tgz"
    print(f'Packing web_static to versions/{arch_name}')
    if not os.path.exists('versions'):
        os.makedirs('versions')
    try:
        local(f"tar -cvzf versions/{arch_name} ./web_static")
    except Exception:
        return None
    else:
        size = os.path.getsize(f'versions/{arch_name}')
        print(f"web_static packed: versions/{arch_name} -> {size}Bytes")
        return f"versions/{arch_name}"
