# Installing Logstash 7.16.3

## Install
```
oc create -f ./logstash-config.yaml
oc run logstash  --image=logstash:7.16.3 --env=LOGSTASH_HOME\=/usr/share/logstash --command=true bash -- /etc/logstash/logstash-wrapper.sh -f /etc/logstash/config
oc set volume --add=true --configmap-name=logstash --mount-path=/etc/logstash dc/logstash
oc set volume --add=true --mount-path=/var/log dc/logstash
oc set volume --add=true --type secret --secret-name=elastic-secret --mount-path=/etc/ssl/elastic dc/logstash
oc expose dc/logstash --port=5000
```

## Uninstall
```
oc delete dc/logstash
```

## Expose
```
```

## Connect
Connect to logstash.elastic.svc.cluster.local on port 5000 using TCP.

For example Ansible Tower can use these settings to log jobs to ElasticSearch.

![](../awx3/awx-logging.png?raw=true)
