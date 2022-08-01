SOURCE_IMAGE = os.getenv("SOURCE_IMAGE", default='.')
LOCAL_PATH = os.getenv("LOCAL_PATH", default='.')
NAMESPACE = os.getenv("NAMESPACE", default='alpha')
APP_NAME = "clientcapture"

local_resources(
    'clientcapture',
    'date +%s > start-time.txt'
)

k8s_custom_deploy(
    APP_NAME,
    apply_cmd="tanzu apps workload apply -f config/workload.yaml --live-update" +
               " --local-path " + LOCAL_PATH +
               " --source-image " + SOURCE_IMAGE +
               " --namespace " + NAMESPACE +
               " --yes >/dev/null" +
               " && kubectl get workload " + APP_NAME + " --namespace " + NAMESPACE + " -o yaml",
    delete_cmd="tanzu apps workload delete -f config/workload.yaml --namespace " + NAMESPACE + " --yes",
    container_selector='workload',
    live_update=[
      sync('/app', '/app')
      sync('/__init__.py', '/__init__.py')
      sync('/requirements.txt', '/requirements.txt')
    ]
)

k8s_resource('clientcapture', port_forwards=["80:80"],
            extra_pod_selectors=[{'serving.knative.dev/service': 'clientcapture'}])

allow_k8s_contexts('tap-aus-1')
