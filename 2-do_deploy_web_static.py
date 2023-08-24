#!/usr/bin/python3
#  Fabric script that generates a .tgz archive from the
# contents of the web_static folder of your AirBnB Clone repo
# using the function do_pack
import os
from fabric.api import run, put, env

env.hosts = ['44.192.38.3', '3.239.82.120']
env.user = "ubuntu"

def do_deploy(archive_path):
"""
    Deploy a compressed archive to the web servers.

    This function uploads the specified archive to the remote servers, extracts
    its contents, updates the symbolic link, and deploys the new version of the
    static website.

    Args:
        archive_path (str): Path to the archive file to be deployed.

    Returns:
        bool: True if deployment is successful, False otherwise.
 """

    if not os.path.exists(archive_path):
        return False

    archive_filename = os.path.basename(archive_path)
    archive_name = os.path.splitext(archive_filename)[0]

    try:
	"""Upload the archive to the server's /tmp/ directory"""
        put(archive_path, '/tmp/')
         """ Create the necessary release directory"""
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(archive_name))
         """ Extract the archive contents"""
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(archive_filename, archive_name))
        """ Clean up the uploaded archive"""
        run('sudo rm /tmp/{}'.format(archive_filename))
        """ Move the contents to the appropriate location"""
        run('sudo mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(archive_name, archive_name))
        """ Clean up the old web_static directory"""
        run('sudo rm -rf /data/web_static/releases/{}/web_static'.format(archive_name))
        """ Update the symbolic link to point to the new version"""
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(archive_name))
        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", str(e))
        return False

