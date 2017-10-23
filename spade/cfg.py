import os
import yaml

from spade import out

DEFAULT_USER_CONFIG_FNAME = os.path.expanduser('~') + '/.spade.yml'
DEFAULT_PROJ_CONFIG_FNAME = 'spade.yml'
DEFAULT_CONFIG = {
    'docker_client_command': 'docker',
    'kubectl_client_command': 'kubectl',
    'docker_build_host': None,
    'docker_build_dir': './',
    'kubernetes_configs': ['./k8s.yml'],
    'dry_run': False
}


class Config:
    def __init__(self, user_config_fname=DEFAULT_USER_CONFIG_FNAME, project_config_fname=DEFAULT_PROJ_CONFIG_FNAME):
        self.config = DEFAULT_CONFIG

        out.print_header('Reading config')

        self.config.update(self.load_config_file(user_config_fname))
        self.config.update(self.load_config_file(project_config_fname))

    @staticmethod
    def load_config_file(fname):
        fname = os.path.abspath(fname)

        if not os.path.isfile(fname):
            out.print_warn('No config file "%s" found' % fname)
            return {}

        out.print_step('Loaded config file %s' % out.fmt_info(fname))

        with open(fname) as f:
            return yaml.load(f)

    def dump(self):
        return yaml.dump(self.config, default_flow_style=False)

    def set(self, key, value):
        self.config[key] = value

    def has(self, key):
        return key in self.config

    def get(self, key):
        if not self.has(key):
            out.fail('Config variable "%s" is not set' % key)

        return self.config[key]

