#!/usr/bin/python3
#  Fabric script that generates a .tgz archive from the
# contents of the web_static folder of your AirBnB Clone repo
# using the function do_pack
import os
from fabric.api import run, put, env

env.hosts = ['52.207.208.66', '54.236.239.243']
env.user = "ubuntu"


def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        return False

    archive_filename = os.path.basename(archive_path)
    archive_name = os.path.splitext(archive_filename)[0]

    try:
        put(archive_path, '/tmp/')
        run(' sudo mkdir -p /data/web_static/releases/{}/'.format(archive_name))
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(archive_filename, archive_name))
        run('sudo rm /tmp/{}'.format(archive_filename))
        run('sudo mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(archive_name, archive_name))
        run('sudo rm -rf /data/web_static/releases/{}/web_static'.format(archive_name))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(archive_name))
        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", str(e))
        return False

