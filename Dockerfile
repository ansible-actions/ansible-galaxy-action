# hadolint ignore=DL3007
FROM python:latest

LABEL "maintainer"="L3D <l3d@c3woc.de>"
LABEL "repository"="https://github.com/ansible-actions/ansible-publish-galaxy.git"
LABEL "homepage"="https://github.com/ansible-actions/ansible-publish-galaxy"

# hadolint ignore=DL3008,DL3013,SC1091
RUN pip3 install --no-cache-dir ansible \
      && ansible --version

# Fix potential UTF-8 errors
RUN locale-gen en_US.UTF-8

COPY ansible-docker.sh /ansible-docker.sh
ENTRYPOINT ["/ansible-docker.sh"]
