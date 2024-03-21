#!/usr/bin/python3
""" creates and distributes an archive to the web servers """
from fabric.api import *
from datetime import datetime
import os
env.hosts = ['34.232.68.194', '54.173.210.20']


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
        run(f"ln -s {releases_path}/{raw_name}/ {current_path}")

        print("New version deployed!")
        return True

    except Exception as e:
        return False
