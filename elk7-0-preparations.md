# Preparing for Elastic Stack

## Create a project
```
oc new-project elastic
```
## Service Account
Create service account. Allow the service account to run privileged containers.
```
oc create -f ./elastic-sa.yaml
oc adm policy add-scc-to-user privileged -z elastic
```
## Persistent Volumes
The elasticsearch configuration uses volumeClaimTemplate for it's PVC. After installing you should see PVC's similar to:
```
NAME                STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS       AGE
data-es-cluster-0   Bound     pvc-bfbb4f83-c9d8-11e9-b63b-00505692d555   50Gi       RWO            vsphere-standard   1d
data-es-cluster-1   Bound     pvc-cbde71b0-c9d8-11e9-b63b-00505692d555   50Gi       RWO            vsphere-standard   1d
data-es-cluster-2   Bound     pvc-dfddd89c-c9d8-11e9-b63b-00505692d555   50Gi       RWO            vsphere-standard   1d
```
You should either
* enable dynamic persistent volumes in order to have the cluster create the PVC's
* create the PVC's yourself for each of the data-es-cluster-[0-2] 
For example,
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-es-cluster-0
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
```
## SSL

Enabling SSL requires a certificate to be used on SSL connections. We put the certificate in a secret for reuse in deployments

### Create an SSL certificate
You should use a CA certified certificate. For testing purposed we can however use a self-signed certificate instead.
```
openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out elastic.crt -keyout elastic.key
```
```
Generating a 4096 bit RSA private key
..............++
............................++
writing new private key to 'elastic.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:NL
State or Province Name (full name) [Some-State]:NH
Locality Name (eg, city) []:Amsterdam
Organization Name (eg, company) [Internet Widgits Pty Ltd]:IBM
Organizational Unit Name (eg, section) []:GTS
Common Name (e.g. server FQDN or YOUR name) []:elastic
Email Address []:
```
Resulting in two files
* elastic.crt
* elastic.key

### Create the secret
```
oc create secret generic elastic-secret --from-file=./elastic.key --from-file=./elastic.crt
```

### Sample secret usage
```
oc set volume --add=true --type secret --secret-name=elastic --mount-path=/etc/ssl/elastic dc/logstash
```
