Function: Provides a web page that reports on the calling client identity details and general data
Purpose:  To determine data that is passed through to server directly and via Proxies and Load balancers
Language: Python

Comment:
This is setuop to be containerised and deployed into a Kubernetes cluster. It was writtent to determine
what is passed through by Kubernetes Services and Ingress controllers to help with scenerios like 
feature set support and enablement as well as network policies.

Looks for header values such as HTTP_X_REAL_IP and X_FORWARDER_FOR as well as allows full request environment
and header data to be displayed


