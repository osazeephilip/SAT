# Installing Elasticsearch 7.17.0

## Install
Install the application container and expose the service
```
oc create -f ./elasticsearch-svc.yaml
oc create -f ./elasticsearch-app.yaml
```

## Updating elastic search image to 7.17.0 in existing deployments.

```
You can change the image to 7.17.0 by editing the elasticsearch sts.

1. oc get sts
2. oc edit es-cluster
3. Change the image version to 7.17.0 as below.

  - name: path.repo
          value: /usr/share/elasticsearch/data
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
    imagePullPolicy: IfNotPresent
    name: elasticsearch
 4. save and exit. New container will start automatically.
 ```

