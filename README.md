# Peekaboo 
## Web Request Information Exposure

### Function:
Provides a web page that reports on the calling client identity details and general data.


### Purpose:
To determine data that is passed through to server directly and via Proxies and Load balancers
This is setup to be containerised and deployed into a Kubernetes cluster. It was writtent to determine
what is passed through by Kubernetes Services and Ingress controllers to help with scenerios like 
feature set support and enablement as well as network policies.

Looks for header values such as HTTP_X_REAL_IP and X_FORWARDER_FOR as well as allows full request environment
and header data to be displayed

There is also a /status form for using for load simulation and status querying from LB services

### Code Overview
Written in Python3 (requires minimum 3.10 due to the use of the case statement) with the Flask web framework and SQLAchemy for DB interaciton. Utilises either SqLite or MySQL for data persistence. The default is to use sqlite but to use mysql the URL can either by passed via environment variable **DATABASE_URL** or via a service binding associated to the K8s deployment (service binding default name is **peekaboo-binding**)





### To Do
- Put a paging control on the history tab
- Create tests for TAP supplychain
- Tart up the chart object
