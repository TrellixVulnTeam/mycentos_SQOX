#! /usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import getpass
import shutil
import tarfile

from src.util import *

if __name__ == '__main__':
    # parse = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    # parse = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parse = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    def_ins_path = '/opt/module'
    def_pkg_path = '/opt/software/apache-flume-1.9.0-bin.tar.gz'

    parse.add_argument('-p', '--package-path', default=f'{def_pkg_path}'
                       , help='the software package path to be installed')
    parse.add_argument('-i', '--install-path', default=f'{def_ins_path}'
                       , help='the destination path where the software will be installed to')
    parse.add_argument('-n', '--non-interactive', action='store_true'
                       , help='whether silently install software or not')

    # parse command line arguments
    args = parse.parse_args()

    # print(args)
    # sys.exit()

    package_path = args.package_path
    install_path = args.install_path
    interactive = not args.non_interactive

    software = os.path.basename(package_path).replace('-bin.tar.gz', '')

    flume_home = os.path.normpath(f'{install_path}/{software}')

    # make install directory if not exists
    if not os.path.exists(install_path):
        os.makedirs(install_path)

    if os.path.exists(flume_home) and interactive:
        logging.info(f'{flume_home} already existed, continue or exit (y/n)')
        if 'y' != readchar():
            logging.info('exit install...')
            sys.exit()

    # uninstall
    if os.path.exists(flume_home):
        shutil.rmtree(flume_home)

    logging.info('install...')
    with tarfile.open(package_path, 'r:gz') as tar:
        tar.extractall(install_path)

    os.rename(f'{install_path}/{software}-bin', flume_home)
    os.remove(f'{flume_home}/lib/guava-11.0.2.jar')
    os.remove(f'{flume_home}/lib/slf4j-log4j12-1.7.25.jar')

    putenv(interactive, f'/home/{getpass.getuser()}/.bash_profile', 'FLUME_HOME', flume_home)

    if interactive:
        logging.info('the software needs to reboot after installation (y/n)')
        if 'y' != readchar():
            logging.warning('please reboot manually to make the installatin take effect')
            sys.exit()

    logging.info(f'{flume_home} has been successfully installed')
    logcall('sync && sudo reboot')
