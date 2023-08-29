# RSS Assistant

The application pulls RSS items and sends them as notifications to various receivers.

---

![Rss](https://img.shields.io/badge/rss-F88900?style=for-the-badge&logo=rss&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)


## Features

* Pull multiple RSS sources as scheduled
* Store RSS history to select only newer items
* Use CRON syntax for a scheduler
* Define **receivers** and **message format** for notifications


## Deployment

### Docker

Public image repository: https://github.com/thevops/RSSAssistant/pkgs/container/rss-assistant

```sh
# check out VERSION file in this repository
docker pull ghcr.io/thevops/rss-assistant:$VERSION
```

### Docker Compose

Download requirements and prepare the environment using `init.sh` file:

```sh
curl -sL https://raw.githubusercontent.com/thevops/RSSAssistant/master/deployment/docker-compose/init.sh > init.sh
sh init.sh
```

### Kubernetes - Helm chart

in progress


## ToDo

* `notifications`: Add interface for `apprise` to use all of apprises receivers
without defining them here
* `database`: Add interface for an external database (eg. https://restdb.io/).
It will allow RSSAssistant to be running serverless (eg. Cloud Functions).
* `receivers`: Add simple URL webhook receiver.
* Add configuration examples
