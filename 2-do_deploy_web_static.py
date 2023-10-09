#!/usr/bin/python3
"""
Fabric script to deploy a web_static archive to a web server.
This script uploads a web_static archive to a web server, uncompresses it,
and creates a symbolic link to the new release.
"""

from fabric.api import run, put, env, local, sudo
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['18.207.2.67', '52.91.120.49']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if exists(archive_path) is False:
        return False
    try:
        # Upload the archive to /tmp/
        put(archive_path, '/tmp/')
        # Create target filename without extension
        file_name_ext = archive_path.split("/")[-1]
        tar_file_name = file_name_ext.split(".")[0]
        run('sudo mkdir -p /data/web_static/releases/{}/'.
            format(tar_file_name))
        # Uncompress archive and delete archive from web server
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.
            format(file_name_ext, tar_file_name))
        run('sudo rm /tmp/{}'.format(file_name_ext))
        # Move content into host web_static
        cmd_mv = 'sudo mv /data/web_static/releases/{}/web_static/*' \
                 ' /data/web_static/releases/{}/'.format(tar_file_name,
                                                         tar_file_name)
        run(cmd_mv)
        # Remove redundant content folder
        cmd_rm_dir = 'sudo rm -rf /data/web_static/releases/{}/web_static'.\
            format(tar_file_name)
        run(cmd_rm_dir)
        # Delete existing symbolic link
        run('sudo rm -rf /data/web_static/current')
        # Reestablish symbolic link with new content folder
        sym_link = 'sudo ln -s /data/web_static/releases/{}/' \
                   ' /data/web_static/current'.\
            format(tar_file_name)
        run(sym_link)
        print('New version deployed!')
        return True
    except Exception:
        return False
