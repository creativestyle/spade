from __future__ import print_function

import argparse

from spade import out
from spade import cfg
from spade import action

APP_DESCRIPTION = '''
     /------\              -
     |       =============| |
     \------/              -
     _______  ___   ___  ____
    / __/ _ \/ _ | / _ \/ __/
   _\ \/ ___/ __ |/ // / _/
  /___/_/  /_/ |_/____/___/
'''

ACTIONS_DESCRIPTION = '''\
deploy      builds, pushes, tags the image then applies the k8s config
build       builds the docker image
push        pushes (to specified repo) and tags the docker image with new version
config      display current config
run         runs the docker image on your docker daemon
'''


def create_parser():
    parser = argparse.ArgumentParser(description=APP_DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('action',
                        help=ACTIONS_DESCRIPTION)

    parser.add_argument('--dry-run',
                        dest='dry_run',
                        action='store_true',
                        help='display commands to be executed, but do nothing')

    parser.add_argument('--version',
                        dest='version',
                        action='store',
                        help='version of the docker image')

    return parser


def execute():
    parser = create_parser()
    cli_args = parser.parse_args()
    config = cfg.Config()
    actions = action.Actions(config)

    config.set('dry_run', cli_args.dry_run)

    if cli_args.action == 'deploy':
        actions.deploy(cli_args.version)
    elif cli_args.action == 'build':
        actions.build()
    elif cli_args.action == 'push':
        actions.push(cli_args.version)
    elif cli_args.action == 'run':
        actions.run()
    elif cli_args.action == 'apply':
        actions.apply(cli_args.version)
    elif cli_args.action == 'config':
        actions.config()
    else:
        out.fail('Unknown action "%s"' % cli_args.action)

