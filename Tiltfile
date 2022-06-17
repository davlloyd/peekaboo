SOURCE_IMAGE = os.getenv("SOURCE_IMAGE", default='us.gcr.io/lloyd-266015/supply-chain/clientcapture-source')
LOCAL_PATH = os.getenv("LOCAL_PATH", default='/Users/lloydd/Documents/git/clientcapture-python')
NAMESPACE = os.getenv("NAMESPACE", default='alpha')

k8s_custom_deploy(
    'clientcapture',
    apply_cmd="tanzu apps workload apply -f config/workload.yaml --live-update" +
               " --local-path " + LOCAL_PATH +
               " --source-image " + SOURCE_IMAGE +
               " --namespace " + NAMESPACE +
               " --yes >/dev/null" +
               " && kubectl get workload tanzu-java-web-app --namespace " + NAMESPACE + " -o yaml",
    delete_cmd="tanzu apps workload delete -f config/workload.yaml --namespace " + NAMESPACE + " --yes",
    deps=['pom.xml', './target/classes'],
    container_selector='workload',
    live_update=[
      sync('./target/classes', '/workspace/BOOT-INF/classes')
    ]
)

k8s_resource('clientcapture', port_forwards=["8080:8080"],
            extra_pod_selectors=[{'serving.knative.dev/service': 'clientcapture'}])

allow_k8s_contexts('tap-aus-1')
