Local running
-------------

* Lazy option just run on your local machine

```
# env $(cat providers/local/env/* | xargs) docker-compose -f compose/local.yaml up --build
```

Aiven running
-------------

* Setup your account and services
* Edit config files provider/aiven/env/
* Replace certs provider/aiven/{kafka,pg}/
* And run docker-compose

```
# env $(cat providers/aiven/env/* | xargs) docker-compose -f compose/aiven.yaml up --build
```
