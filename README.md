# Deploy a foundationdb cluster on Azure Redhat OpenShift (ARO) using the https://github.com/FoundationDB/fdb-kubernetes-operator and running a benchmark test with YCSB Yahoo Cloud Service Benchmark https://github.com/brianfrankcooper/YCSB

## Create 60 Node ARO cluster

- Nodes: 60
- NodeType: Standard_F8s_v2
- Disks: NvME
- Region: Sweeden
-

## Build and push YCSB image to repository

## Install fdb-kubernetes operator

```
oc apply -f https://raw.githubusercontent.com/FoundationDB/fdb-kubernetes-operator/main/config/crd/bases/apps.foundationdb.org_foundationdbclusters.yaml

#backup
oc apply -f https://raw.githubusercontent.com/FoundationDB/fdb-kubernetes-operator/main/config/crd/bases/apps.foundationdb.org_foundationdbbackups.yaml
#restore
oc apply -f https://raw.githubusercontent.com/FoundationDB/fdb-kubernetes-operator/main/config/crd/bases/apps.foundationdb.org_foundationdbrestores.yaml

#deployment
oc apply -f https://raw.githubusercontent.com/foundationdb/fdb-kubernetes-operator/main/config/samples/deployment.yaml

```

## Deploy foundationdb cluster

```
apiVersion: apps.foundationdb.org/v1beta2
kind: FoundationDBCluster
metadata:
  name: fdb-cluster
  namespace: default
spec:
  automationOptions:
    replacements:
      enabled: true
  faultDomain:
    key: foundationdb.org/none
  labels:
    filterOnOwnerReference: false
    matchLabels:
      foundationdb.org/fdb-cluster-name: fdb-cluster
    processClassLabels:
    - foundationdb.org/fdb-process-class
    processGroupIDLabels:
    - foundationdb.org/fdb-process-group-id
  minimumUptimeSecondsForBounce: 60
  processCounts:
    cluster_controller: 1
    storage: 4
    log: 2
    stateless: 1
  processes:
    general:
      customParameters:
      - knob_disable_posix_kernel_aio=1
      podTemplate:
        spec:
          containers:
          - name: foundationdb
            resources:
              # TODO: Is there where we attach to PVC?
              requests:
                cpu: 100m
                memory: 128Mi
            securityContext:
              runAsUser: 0
          - name: foundationdb-kubernetes-sidecar
            resources:
              limits:
                cpu: 100m
                memory: 128Mi
              requests:
                cpu: 100m
                memory: 128Mi
            securityContext:
              runAsUser: 0
          initContainers:
          - name: foundationdb-kubernetes-init
            resources:
              limits:
                cpu: 100m
                memory: 128Mi
              requests:
                cpu: 100m
                memory: 128Mi
            securityContext:
              runAsUser: 0
      volumeClaimTemplate:
        spec:
          resources:
            requests:
              storage: 16G
  routing:
    headlessService: true
  sidecarContainer:
    enableLivenessProbe: true
    enableReadinessProbe: false
  useExplicitListenAddress: true
  version: 7.1.26




```

```
 oc apply -f fdb_cluster.yaml

```

## Deploy YCSB on the fdb cluster and run benchmark tests

```
oc apply -f ycsb_run_fdb_benchmark.yaml
```
