# hadolint ignore=DL3007
FROM python:latest

LABEL "maintainer"="L3D <l3d@c3woc.de>"
LABEL "repository"="https://github.com/ansible-actions/ansible-publish-galaxy.git"
LABEL "homepage"="https://github.com/ansible-actions/ansible-publish-galaxy"

# hadolint ignore=DL3008,DL3013,SC1091
RUN pip3 install --no-cache-dir ansible

COPY ansible_docker.py /ansible_docker.py
CMD [ "/usr/local/bin/python3", "/ansible_docker.py" ]
