#!/usr/bin/python3
""" creates and distributes an archive to the web servers """
from fabric.api import *
from datetime import datetime
import os
env.hosts = ['34.232.68.194', '54.173.210.20']


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


def do_deploy(archive_path):
    """ distributes the archive to the server """
    if not os.path.exists(archive_path):
        return False

    try:
        # Put the archive on the server
        put(archive_path, '/tmp')

        # Extract archive filename without extension
        raw_name = os.path.basename(archive_path)[:-4]

        # Define remote paths
        releases_path = '/data/web_static/releases'
        current_path = '/data/web_static/current'

        # Create directory structure
        run(f"mkdir -p {releases_path}/{raw_name}/")

        # Extract archive contents
        run(f"tar -xzf /tmp/{raw_name}.tgz -C {releases_path}/{raw_name}/")

        # Remove archive file
        run(f"rm /tmp/{raw_name}.tgz")

        # Move contents to appropriate location
        run("mv {}/{}/web_static/* {}/{}/".format(releases_path, raw_name,
                                                  releases_path, raw_name))

        # Remove empty web_static directory
        run(f"rm -rf {releases_path}/{raw_name}/web_static")

        # Update symbolic link
        run(f"rm -rf {current_path}")
        run("ln -sf {releases_path}/{raw_name}/ {current_path}")

        print("New version deployed!")
        return True

    except Exception as e:
        return False


def deploy():
    """ creates and distributes an archive to the web servers """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
