 Action Ansible Galaxy Roles Release
===============================

This Action will import ansible roles on [galaxy-ng](https://galaxy.ansible.com). Caution, this action is only for roles, for collections maybe you want to consider using the [ansible-publish](https://github.com/marketplace/actions/ansible-publish) action.

## Example usage
Example of ``.github/workflows/galaxy.yml``
```yaml
---
name: Galaxy-NG Roles Import

# yamllint disable-line rule:truthy
on:
  release:
    types: ['created']

jobs:
  build:
    name: Galaxy Role Importer
    runs-on: ubuntu-latest

    steps:
      - name: 'Checkout git repo'
        uses: actions/checkout@v4
        with:
          submodules: true
          fetch-depth: 0

      - name: 'Release on galaxy'
        uses: ansible-actions/ansible-galaxy-action@v1.2.0
        with:
          galaxy_api_key: ${{ secrets.galaxy_api_key }}
```

You can define the described variables like this:
```yaml
[...]
        with:
          galaxy_api_key: ${{ secrets.galaxy_api_key }}
          galaxy_version: '1.2.3'
          path: './'
          galaxy_api: 'https://galaxy.ansible.com/api/'
```

## Variables

| name | default value | description |
| --- | --- | --- |
| ``galaxy_api_key`` | - | Your personal Galaxy-NG API Token |
| ``path`` | ``./`` | The location of your role. (relative path) |
| ``galaxy_api`` | ``https://galaxy.ansible.com/api/`` | Ansible Galaxy API |
| ``galaxy_version`` | - | The galaxy version for galaxy-ng.|
## Some Hints
+ You find your [Galaxy-NG Token](https://galaxy.ansible.com/ui/token/) on Galaxy-NG -> Collections -> API-Token. The collections token is valid for roles too.
+ You can only import new role releases on ansible-galaxy
+ The galaxy version is provided with the ``ansible-galaxy role import --branch "$galaxy_version"`` option on the galaxy import tool. The default value ``main`` as branch name.
