import re
from datetime import datetime
from spade import out
from spade import cmd


class Actions(object):
    def __init__(self, config):
        self.cfg = config
        self.cmd = cmd.Command(config)

    def __get_docker_image_uri(self):
        return self.cfg.get('docker_repo_uri') + self.cfg.get('docker_image_name')

    def __update_k8s_config(self, content, image_version):
        repo = self.__get_docker_image_uri()
        new_container = repo + ':' + image_version

        return re.sub(re.escape(repo) + r'(:[^\s"\']+)?', new_container, content)

    @staticmethod
    def __generate_version_tag():
        return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    @staticmethod
    def __read_file(fname):
        with open(fname) as f:
            return f.read()

    def build(self):
        if self.cfg.has('pre_build_commands'):
            out.print_header('Executing pre build steps')

            for command in self.cfg.get('pre_build_commands'):
                self.cmd.execute(command, shell=True)

        out.print_header('Building the docker image')

        args = ['build', '--pull', '-t', self.cfg.get('docker_image_name'), self.cfg.get('docker_build_dir')]

        if self.cfg.has('docker_build_args'):
            for k, v in self.cfg.get('docker_build_args').iteritems():
                args.extend(['--build-arg', '%s=%s' % (k, v)])

        self.cmd.docker(args)

    def push(self, image_version):
        image_repo = self.__get_docker_image_uri()

        if image_version is None:
            image_version = self.__generate_version_tag()

        out.print_header('Pushing the updated docker image')

        full_image = image_repo + ':' + image_version

        self.cmd.docker(['tag', self.cfg.get('docker_image_name'), full_image])
        self.cmd.docker(['push', full_image])

    def apply(self, image_version):
        out.print_header('Applying kubernetes provisioning')

        if image_version:
            k8s_config = '\n---\n'.join(map(lambda fname: self.__read_file(fname), self.cfg.get('kubernetes_configs')))
            k8s_config = self.__update_k8s_config(k8s_config, image_version)

            self.cmd.kubectl(['apply', '-f', '-'], input_data=k8s_config)
        else:
            args = ['apply']

            for conf in self.cfg.get('kubernetes_configs'):
                args.extend(['-f', conf])

            self.cmd.kubectl(args)

    def run(self):
        out.print_header('Running the docker image')

        self.cmd.docker(['run', '-i', '-t', self.cfg.get('docker_image_name')])

    def deploy(self, image_version):
        if image_version is None:
            image_version = self.__generate_version_tag()

        self.build()
        self.push(image_version)
        self.apply(image_version)

        out.print_success('Deployment finished. Wait for kubernetes to finish the rolling update...')

    def config(self):
        out.print_header('Computed configuration')
        print('  ' + '  '.join(self.cfg.dump().splitlines(True)))
