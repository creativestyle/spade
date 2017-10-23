SPADE
=====

Simple CLI tool to aid deployment to a kubernetes cluster.

## Rationale

We have an internal tectonic/kubernetes cluster that we use for internal services and as a playground.
We needed a tool that would aid in deployment. Theoretically a bash script could do the same
but this way it's more flexible, readable and less error-prone.

## How it works

The basic process:
 - build the docker container (Dockerfile) form current directory
 - tag it with current date
 - push the image to the docker repository of your choosing
 - update k8s configs with the new image name (on the fly, not written to disk)
 - apply the k8s configs

## Prerequisites

### Kubectl

Set up kubernetes CLI tool `kubectl` first.

1. If on OSX install from brew - `brew install kubernetes-cli`.
2. Install your config at `~/.kube/config`
3. Verify it's working by typing `kubectl get pods`.

### Docker daemon

You should have a docker daemon for building images. Install it natively on your computer or on a VM.

_See https://docs.docker.com/docker-for-mac/install/ if using OSX_

Also locally insteall docker cli command via brew - `brew install docker`.

Unless it's on `localhost`, you should configure it's location in `~/.spade.yml`:

```
docker_build_host: localhost
```

If the client version is different than your daemon version (you receive errors about API incompatiblity) 
you should add to `~/.spade.yml` something like this:

```
docker_api_version: 1.22
```

### Docker repository

You should log into your docker repository first..

Type `docker login docker_repo_url` and enter credentials.

If your docker daemon is not on localhost use:
`docker -H your_docker_host docker_repo_url`

## Installation

Clone to your desired location and link the executable to your bin dir, for example (on OSX):

```
ln -s /path/to/spade/spade.py /usr/local/bin/spade
```

If you don't have PyYAML installed globally then install it via requirements (create a virtualenv first if you need).

```
pip install -r requirements.txt 
```

## Deploying existing projects with spade

Just type `spade deploy` in the project's directory.

## Configure project for the cluster deployment

Create `Dockerfile` and your kubernetes yml configs int the project directory, then create `spade.yml` file in the 
main project directory:

```
docker_image_name: name-of-the-image
docker_repo_uri: docker_repo_url/image_name
docker_build_args:
    BUILD_ARG_NAME: value
kubernetes_configs:
    - kubernetes_config_file.yml
    - or_more_of_them.yml
```

You can skip the build args if your dockerfile does not use them.

The name of the image in kubernetes configs must be the same as set in your `spade.yml` file, which is like:

```
docker.creativestyle.pl/yourname.yoursurname/name-of-the-image
```

Spade deploy will build the image and tag it with current date, then in order to force kubernetes to deploy new version
it will rewrite on-the-fly the kubernetes config changing the image tag to the one being deployed.

If you require to execute some commands before docker image build on the local machine, then use this setting in project's
`spade.yml` file:

```
pre_build_commands:
    - NODE_ENV=production webpack -p
```