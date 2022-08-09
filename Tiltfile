SOURCE_IMAGE = os.getenv("SOURCE_IMAGE", default='.')
LOCAL_PATH = os.getenv("LOCAL_PATH", default='.')
NAMESPACE = os.getenv("NAMESPACE", default='alpha')
APP_NAME = "peekaboo"
K8S_CONTEXT = os.getenv("K8S_CONTEXT", default="tap-aus-1")

local_resources(
    APP_NAME,
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

k8s_resource(APP_NAME, port_forwards=["80:80"],
            extra_pod_selectors=[{'serving.knative.dev/service': APP_NAME}])

allow_k8s_contexts(K8S_CONTEXT)
