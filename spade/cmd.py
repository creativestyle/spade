import os
import sys
import subprocess

from spade import out


class Command(object):
    def __init__(self, config):
        self.cfg = config

    def execute(self, args, env=None, cwd=None, input_data=None, shell=False):
        process_env = os.environ.copy()

        if isinstance(args, list):
            cmd_string = ' '.join(args)
        else:
            cmd_string = args

        if env is not None:
            process_env.update(env)

        out.print_step('Executing %s' % out.fmt_info(cmd_string))

        if self.cfg.get('dry_run'):
            return

        if input_data is not None:
            p = subprocess.Popen(args, stdout=sys.stdout, stdin=subprocess.PIPE, env=process_env, cwd=cwd, shell=shell)
            p.communicate(input_data)
        else:
            p = subprocess.Popen(args, stdout=sys.stdout, stderr=sys.stderr, env=process_env, cwd=cwd, shell=shell)
            p.communicate()

        if p.returncode != 0:
            out.fail('The command has failed: ' + out.fmt_info(cmd_string))
            out.fail('Terminating')

    def docker(self, args):
        cmd_args = [self.cfg.get('docker_client_command')]

        if self.cfg.get('docker_build_host'):
            cmd_args.extend(['-H', self.cfg.get('docker_build_host')])

        cmd_args.extend(args)
        penv = {}

        if self.cfg.has('docker_api_version'):
            penv['DOCKER_API_VERSION'] = str(self.cfg.get('docker_api_version'))

        self.execute(cmd_args, penv)

    def kubectl(self, args, input_data=None):
        cmd_args = [self.cfg.get('kubectl_client_command')]
        cmd_args.extend(args)

        self.execute(cmd_args, input_data=input_data)




