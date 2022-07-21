# Installing Logstash 7.16.3

### Create image repo secret it not present already. This is used in logstash-app.yaml for pulling the image from cacf artifcatory.

```
oc create secret docker-registry --docker-email='emailID' --docker-username='emailID' --docker-password='repo-token' --docker-server='https://gts-cacf-global-team-prod-docker-local.artifactory.swg-devops.com' cacf-repo-prod-artifactory-secret

Eg: oc create secret docker-registry --docker-email='ankreddy@in.ibm.com' --docker-username='ankreddy@in.ibm.com' --docker-password='mySecretRepoToken' --docker-server='https://gts-cacf-global-team-prod-docker-local.artifactory.swg-devops.com' cacf-repo-prod-artifactory-secret
```

Note: If you already have an existing repo secret, then you can use the same secret. You need to update secret name under imagePullCredentials section of  logstash-app.yaml file.

Eg:

```
   imagePullSecrets:
   - name: my-existing-cacf-repo-prod-artifactory-secret

```

## Install
Note: All the yaml files are present in config directory.
NOTE: Below step is to be done during initial installation.

You can edit the logstash-config.yaml with your custom settings and create the configuration.

```
oc create -f ./logstash-config.yaml
oc create -f ./logstash-svc.yaml
oc create -f ./logstash-app.yaml
```

## For upgrading
```
oc replace -f ./logstash-app.yaml
```

## Connect
Connect to logstash.elastic.svc.cluster.local on port 5000 using TCP.

For example, Ansible Tower External Logging sends Activity streams and event logs to Logstash using this setting.

![](../awx3/awx-logging.png?raw=true)
