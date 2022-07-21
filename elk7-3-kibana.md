# Installing Kibana 7.9.x

## Install
```
oc create -f ./kibana-svc.yaml
oc create -f ./kibana-app.yaml
oc create -f ./kibana-route.yaml
```

## Using Kibana

https://kibana.yaocp.local

Make sure to create an index for logstash-* during initial setup.

![](kibana-discovery.png?raw=true)

## Importing Kibana Dashboard

Kibana Dashboard can be imported using ndjson (newline-delimited json) file. DX team (Ivan Sobotik/John Davis) normally provide those. Check with them for latest version.

[CACF Dashboards (Executive and Incident)](https://github.kyndryl.net/cacf/elk/blob/master/CACF_dashboards.ndjson)

[BPAC Dashboard](https://github.kyndryl.net/cacf/elk/blob/master/config/bpac_dashboard.ndjson)

To import the ndjson file, Click the collapsed menu option -> Stack Management -> Saved Objects -> Import -> Import -> Select ndjson File -> Import

![](images/kibana1.png?raw=true)   ![](images/kibana2.png?raw=true)   ![](images/kibana3.png?raw=true)

![](images/kibana4.png?raw=true)

After import, you should see a message like below - 

![](images/kibana5.png?raw=true)

Check and confirm that you are able to view the dashboards - 

Click the collapsed menu option -> Dashboard

![](images/kibana6.png?raw=true)

You should be able to see atleast the 3 CACF related dashboards - 

![](images/kibana7.png?raw=true)
