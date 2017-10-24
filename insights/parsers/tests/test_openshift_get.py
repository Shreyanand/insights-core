from insights.parsers import openshift_get
from insights.tests import context_wrap
import datetime

OC_GET_POD = """
apiVersion: v1
items:
- apiVersion: v1
  kind: Pod
  metadata:
    annotations:
      openshift.io/scc: anyuid
    creationTimestamp: 2017-02-10T16:33:46Z
    labels:
      name: hello-openshift
    name: hello-pod
    namespace: default
  spec:
    containers:
    - image: openshift/hello-openshift
      imagePullPolicy: IfNotPresent
      name: hello-openshift
      ports:
      - containerPort: 8080
        protocol: TCP
      resources: {}
      securityContext:
        capabilities:
          drop:
          - MKNOD
          - SYS_CHROOT
        privileged: false
        seLinuxOptions:
          level: s0:c5,c0
      terminationMessagePath: /dev/termination-log
      volumeMounts:
      - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
        name: default-token-yk69f
        readOnly: true
    dnsPolicy: ClusterFirst
    host: node2.ose.com
    imagePullSecrets:
    - name: default-dockercfg-h7sl1
    nodeName: node2.ose.com
    restartPolicy: Always
    securityContext:
      seLinuxOptions:
        level: s0:c5,c0
    serviceAccount: default
    serviceAccountName: default
    terminationGracePeriodSeconds: 30
    volumes:
    - name: default-token-yk69f
      secret:
        secretName: default-token-yk69f
  status:
    conditions:
    - lastProbeTime: null
      lastTransitionTime: 2017-02-10T16:33:46Z
      status: "True"
      type: Initialized
    containerStatuses:
    - containerID: docker://a172a6945e207c0fd1c391cad31ccb76bc8323f3f024a50b5ba287034302853f
      image: openshift/hello-openshift
      imageID: docker-pullable://docker.io/openshift/hello-openshift@sha256:9b1b29dc4ed029220b2d87fce57fab43f450fa6521ab86f22ddbc5ecc978752a
      lastState:
        terminated:
          containerID: docker://9ea5647da89302437630e96728f9f65593c07d0e65a1b275854fcb4c738c8c46
          exitCode: 2
          finishedAt: 2017-02-13T18:59:47Z
          reason: Error
          startedAt: 2017-02-10T16:33:56Z
      name: hello-openshift
      ready: true
      restartCount: 1
      state:
        running:
          startedAt: 2017-02-13T19:00:49Z
    hostIP: 10.66.208.105
    phase: Running
    podIP: 10.1.0.3
    startTime: 2017-02-10T16:33:46Z
- apiVersion: v1
  kind: Pod
  metadata:
    annotations:
      kubernetes.io/created-by: |
        {"kind":"SerializedReference","apiVersion":"v1","reference":{"kind":"ReplicationController","namespace":"zjj-project","name":"router-1-1","uid":"12c1a374-f75a-11e6-80d0-001a4a0100d2","apiVersion":"v1","resourceVersion":"1638409"}}
      openshift.io/deployment-config.latest-version: "1"
      openshift.io/deployment-config.name: router-1
      openshift.io/deployment.name: router-1-1
      openshift.io/scc: hostnetwork
    creationTimestamp: 2017-02-20T10:48:14Z
    generateName: router-1-1-
    labels:
      deployment: router-1-1
      deploymentconfig: router-1
      router: router-1
    name: router-1-1-w27o2
  spec:
    containers:
    - env:
      - name: DEFAULT_CERTIFICATE_DIR
        value: /etc/pki/tls/private
      - name: ROUTER_EXTERNAL_HOST_HOSTNAME
      - name: ROUTER_EXTERNAL_HOST_HTTPS_VSERVER
      - name: ROUTER_EXTERNAL_HOST_HTTP_VSERVER
      - name: ROUTER_EXTERNAL_HOST_INSECURE
        value: "false"
      - name: ROUTER_EXTERNAL_HOST_PARTITION_PATH
      - name: ROUTER_EXTERNAL_HOST_PASSWORD
      - name: ROUTER_EXTERNAL_HOST_PRIVKEY
        value: /etc/secret-volume/router.pem
      - name: ROUTER_EXTERNAL_HOST_USERNAME
      - name: ROUTER_SERVICE_HTTPS_PORT
        value: "443"
      - name: ROUTER_SERVICE_HTTP_PORT
        value: "80"
      - name: ROUTER_SERVICE_NAME
        value: router-1
      - name: ROUTER_SERVICE_NAMESPACE
        value: zjj-project
      - name: ROUTER_SUBDOMAIN
      - name: STATS_PASSWORD
        value: jRmW4CiS6N
      - name: STATS_PORT
        value: "1936"
      - name: STATS_USERNAME
        value: admin
      image: openshift3/ose-haproxy-router:v3.3.1.7
      imagePullPolicy: IfNotPresent
      livenessProbe:
        failureThreshold: 3
        httpGet:
          host: localhost
          path: /healthz
          port: 1936
          scheme: HTTP
        initialDelaySeconds: 10
        periodSeconds: 10
        successThreshold: 1
        timeoutSeconds: 1
      name: router
      ports:
      - containerPort: 80
        hostPort: 80
        protocol: TCP
      - containerPort: 443
        hostPort: 443
        protocol: TCP
      - containerPort: 1936
        hostPort: 1936
        name: stats
        protocol: TCP
      readinessProbe:
        failureThreshold: 3
        httpGet:
          host: localhost
          path: /healthz
          port: 1936
          scheme: HTTP
        initialDelaySeconds: 10
        periodSeconds: 10
        successThreshold: 1
        timeoutSeconds: 1
      resources:
        requests:
          cpu: 100m
          memory: 256Mi
      securityContext:
        capabilities:
          drop:
          - KILL
          - MKNOD
          - SETGID
          - SETUID
          - SYS_CHROOT
        privileged: false
        runAsUser: 1000070000
        seLinuxOptions:
          level: s0:c8,c7
      terminationMessagePath: /dev/termination-log
      volumeMounts:
      - mountPath: /etc/pki/tls/private
        name: server-certificate
        readOnly: true
      - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
        name: router-token-0j7an
        readOnly: true
    dnsPolicy: ClusterFirst
    host: node1.ose.com
    hostNetwork: true
    imagePullSecrets:
    - name: router-dockercfg-dlu6n
    nodeName: node1.ose.com
    restartPolicy: Always
    securityContext:
      fsGroup: 1000070000
      seLinuxOptions:
        level: s0:c8,c7
      supplementalGroups:
      - 1000070000
    serviceAccount: router
    serviceAccountName: router
    terminationGracePeriodSeconds: 30
    volumes:
    - name: server-certificate
      secret:
        secretName: router-1-certs
    - name: router-token-0j7an
      secret:
        secretName: router-token-0j7an
  status:
    conditions:
    - lastProbeTime: null
      lastTransitionTime: 2017-02-20T10:48:14Z
      status: "True"
      type: Initialized
    containerStatuses:
    - containerID: docker://aa4348a647e0f3186e70a0ce9837f84a25060b4daebab370c1fc093cf8af3349
      image: openshift3/ose-haproxy-router:v3.3.1.7
      imageID: docker-pullable://registry.access.redhat.com/openshift3/ose-haproxy-router@sha256:f2f75cfd2b828c3143ca8022e26593a7491ca040dab6d6472472ed040d1c1b83
      lastState: {}
      name: router
      ready: true
      restartCount: 0
      state:
        running:
          startedAt: 2017-02-20T10:48:16Z
    hostIP: 10.66.208.229
    phase: Running
    podIP: 10.66.208.229
    startTime: 2017-02-20T10:48:14Z
kind: List
metadata: {}
""".strip()

OC_GET_SERVICE = """
apiVersion: v1
items:
- apiVersion: v1
  kind: Service
  metadata:
    creationTimestamp: 2016-12-27T03:24:03Z
    labels:
      component: apiserver
      provider: kubernetes
    name: kubernetes
    namespace: default
    resourceVersion: "9"
    selfLink: /api/v1/namespaces/default/services/kubernetes
    uid: ea9d8fb4-cbe3-11e6-b3c1-001a4a0100d2
  spec:
    clusterIP: 172.30.0.1
    portalIP: 172.30.0.1
    ports:
    - name: https
      port: 443
      protocol: TCP
      targetPort: 443
    - name: dns
      port: 53
      protocol: UDP
      targetPort: 8053
    - name: dns-tcp
      port: 53
      protocol: TCP
      targetPort: 8053
    sessionAffinity: ClientIP
    type: ClusterIP
  status:
    loadBalancer: {}
- apiVersion: v1
  kind: Service
  metadata:
    annotations:
      service.alpha.openshift.io/serving-cert-secret-name: router-1-certs
      service.alpha.openshift.io/serving-cert-signed-by: openshift-service-serving-signer@1480042702
    creationTimestamp: 2017-02-20T10:48:11Z
    labels:
      router: router-1
    name: router-1
    namespace: zjj-project
    resourceVersion: "1638401"
    selfLink: /api/v1/namespaces/zjj-project/services/router-1
    uid: 12bdf634-f75a-11e6-80d0-001a4a0100d2
  spec:
    clusterIP: 172.30.210.0
    portalIP: 172.30.210.0
    ports:
    - name: 80-tcp
      port: 80
      protocol: TCP
      targetPort: 80
    - name: 443-tcp
      port: 443
      protocol: TCP
      targetPort: 443
    - name: 1936-tcp
      port: 1936
      protocol: TCP
      targetPort: 1936
    selector:
      router: router-1
    sessionAffinity: None
    type: ClusterIP
  status:
    loadBalancer: {}
kind: List
metadata: {}
""".strip()

OC_GET_DC = """
apiVersion: v1
items:
- apiVersion: v1
  kind: DeploymentConfig
  metadata:
    creationTimestamp: 2017-02-14T15:21:51Z
    generation: 3
    labels:
      docker-registry: default
    name: docker-registry
    namespace: openshift
    resourceVersion: "1439616"
    selfLink: /oapi/v1/namespaces/openshift/deploymentconfigs/docker-registry
    uid: 4f1cf726-f2c9-11e6-8c0e-001a4a0100d2
  spec:
    replicas: 1
    selector:
      docker-registry: default
    strategy:
      resources: {}
      rollingParams:
        intervalSeconds: 1
        maxSurge: 25%
        maxUnavailable: 25%
        timeoutSeconds: 600
        updatePeriodSeconds: 1
      type: Rolling
    template:
      metadata:
        creationTimestamp: null
        labels:
          docker-registry: default
      spec:
        containers:
        - env:
          - name: REGISTRY_HTTP_ADDR
            value: :5000
          - name: REGISTRY_HTTP_NET
            value: tcp
          - name: REGISTRY_HTTP_SECRET
            value: cXk5GXTrWEG/hgVqeiQYHvX3xdH2JwYMn5GYmqwLXzs=
          - name: REGISTRY_MIDDLEWARE_REPOSITORY_OPENSHIFT_ENFORCEQUOTA
            value: "false"
          image: registry.access.redhat.com/openshift3/ose-docker-registry
          imagePullPolicy: Always
          livenessProbe:
            failureThreshold: 3
            httpGet:
              path: /healthz
              port: 5000
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 5
          name: registry
          ports:
          - containerPort: 5000
            protocol: TCP
          readinessProbe:
            failureThreshold: 3
            httpGet:
              path: /healthz
              port: 5000
              scheme: HTTP
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 5
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
          securityContext:
            privileged: false
          terminationMessagePath: /dev/termination-log
          volumeMounts:
          - mountPath: /registry
            name: registry-storage
        dnsPolicy: ClusterFirst
        terminationGracePeriodSeconds: 30
        volumes:
        - name: registry-storage
          persistentVolumeClaim:
            claimName: registry-claim-test1
    test: false
    triggers:
    - type: ConfigChange
  status:
    availableReplicas: 1
    details:
      causes:
      - type: ConfigChange
      message: caused by a config change
    latestVersion: 3
    observedGeneration: 3
    replicas: 1
    updatedReplicas: 1
- apiVersion: v1
  kind: DeploymentConfig
  metadata:
    creationTimestamp: 2017-02-20T10:48:11Z
    generation: 1
    labels:
      router: router-1
    name: router-1
    namespace: zjj-project
    resourceVersion: "1638435"
    selfLink: /oapi/v1/namespaces/zjj-project/deploymentconfigs/router-1
    uid: 12b9b90f-f75a-11e6-80d0-001a4a0100d2
  spec:
    replicas: 1
    selector:
      router: router-1
    strategy:
      resources: {}
      rollingParams:
        intervalSeconds: 1
        maxSurge: 0
        maxUnavailable: 25%
        timeoutSeconds: 600
        updatePercent: -25
        updatePeriodSeconds: 1
      type: Rolling
    template:
      metadata:
        creationTimestamp: null
        labels:
          router: router-1
      spec:
        containers:
        - env:
          - name: DEFAULT_CERTIFICATE_DIR
            value: /etc/pki/tls/private
          - name: ROUTER_EXTERNAL_HOST_HOSTNAME
          - name: ROUTER_EXTERNAL_HOST_HTTPS_VSERVER
          - name: ROUTER_EXTERNAL_HOST_HTTP_VSERVER
          - name: ROUTER_EXTERNAL_HOST_INSECURE
            value: "false"
          - name: ROUTER_EXTERNAL_HOST_PARTITION_PATH
          - name: ROUTER_EXTERNAL_HOST_PASSWORD
          - name: ROUTER_EXTERNAL_HOST_PRIVKEY
            value: /etc/secret-volume/router.pem
          - name: ROUTER_EXTERNAL_HOST_USERNAME
          - name: ROUTER_SERVICE_HTTPS_PORT
            value: "443"
          - name: ROUTER_SERVICE_HTTP_PORT
            value: "80"
          - name: ROUTER_SERVICE_NAME
            value: router-1
          - name: ROUTER_SERVICE_NAMESPACE
            value: zjj-project
          - name: ROUTER_SUBDOMAIN
          - name: STATS_PASSWORD
            value: jRmW4CiS6N
          - name: STATS_PORT
            value: "1936"
          - name: STATS_USERNAME
            value: admin
          image: openshift3/ose-haproxy-router:v3.3.1.7
          imagePullPolicy: IfNotPresent
          livenessProbe:
            failureThreshold: 3
            httpGet:
              host: localhost
              path: /healthz
              port: 1936
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 1
          name: router
          ports:
          - containerPort: 1936
            hostPort: 1936
            name: stats
            protocol: TCP
          readinessProbe:
            failureThreshold: 3
            httpGet:
              host: localhost
              path: /healthz
              port: 1936
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 1
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
          terminationMessagePath: /dev/termination-log
          volumeMounts:
          - mountPath: /etc/pki/tls/private
            name: server-certificate
            readOnly: true
        dnsPolicy: ClusterFirst
        volumes:
        - name: server-certificate
          secret:
            secretName: router-1-certs
    test: false
    triggers:
    - type: ConfigChange
  status:
    availableReplicas: 1
    details:
      causes:
      - type: ConfigChange
      message: caused by a config change
    latestVersion: 1
    observedGeneration: 1
    replicas: 1
    updatedReplicas: 1
kind: List
metadata: {}
""".strip()

OC_GET_ROLEBINDING = """
apiVersion: v1
items:
- apiVersion: v1
  groupNames: null
  kind: RoleBinding
  metadata:
    creationTimestamp: 2017-03-07T09:00:56Z
    name: admin
    namespace: foo
    resourceVersion: "11803596"
    selfLink: /oapi/v1/namespaces/foo/rolebindings/admin
    uid: 93256034-0314-11e7-b98e-001a4a0101f0
  roleRef:
    name: admin
  subjects:
  - kind: SystemUser
    name: system:admin
  userNames:
  - system:admin
- apiVersion: v1
  groupNames: null
  kind: RoleBinding
  metadata:
    creationTimestamp: 2017-03-07T09:00:56Z
    name: system:image-builders
    namespace: foo
    resourceVersion: "11803603"
    selfLink: /oapi/v1/namespaces/foo/rolebindings/system:image-builders
    uid: 93709567-0314-11e7-b98e-001a4a0101f0
  roleRef:
    name: system:image-builder
  subjects:
  - kind: ServiceAccount
    name: builder
    namespace: foo
  userNames:
  - system:serviceaccount:foo:builder
- apiVersion: v1
  groupNames: null
  kind: RoleBinding
  metadata:
    creationTimestamp: null
    name: myrole
    namespace: foo
    resourceVersion: "415"
    selfLink: /oapi/v1/namespaces/foo/rolebindings/myrole
  roleRef:
    name: myrole
    namespace: foo
  subjects: null
  userNames: null
kind: List
metadata: {}
""".strip()

OC_GET_PROJECT = """
apiVersion: v1
items:
- apiVersion: v1
  kind: Project
  metadata:
    annotations:
      openshift.io/description: ""
      openshift.io/display-name: ""
      openshift.io/requester: testuser
      openshift.io/sa.scc.mcs: s0:c8,c2
      openshift.io/sa.scc.supplemental-groups: 1000060000/10000
      openshift.io/sa.scc.uid-range: 1000060000/10000
    creationTimestamp: 2017-02-13T03:01:30Z
    name: zjj-project
    resourceVersion: "11040756"
    selfLink: /oapi/v1/projects/zjj-project
    uid: b83cdc59-f198-11e6-b98e-001a4a0101f0
  spec:
    finalizers:
    - openshift.io/origin
    - kubernetes
  status:
    phase: Active
- apiVersion: v1
  kind: Project
  metadata:
    annotations:
      openshift.io/description: ""
      openshift.io/display-name: ""
      openshift.io/requester: testuser
      openshift.io/sa.scc.mcs: s0:c11,c0
      openshift.io/sa.scc.supplemental-groups: 1000110000/10000
      openshift.io/sa.scc.uid-range: 1000110000/10000
    creationTimestamp: 2016-12-27T07:49:13Z
    name: test
    resourceVersion: "9401953"
    selfLink: /oapi/v1/projects/test
    uid: f5f2a52c-cc08-11e6-8b9b-001a4a0101f0
  spec:
    finalizers:
    - openshift.io/origin
    - kubernetes
  status:
    phase: Active
kind: List
metadata: {}
""".strip()

OC_GET_ROLE = """
apiVersion: v1
items:
- apiVersion: v1
  kind: Role
  metadata:
    creationTimestamp: 2016-08-30T16:13:03Z
    name: shared-resource-viewer
    namespace: openshift
    resourceVersion: "94"
    selfLink: /oapi/v1/namespaces/openshift/roles/shared-resource-viewer
    uid: a10c3f88-6ecc-11e6-83c6-001a4a0101f0
  rules:
  - apiGroups: null
    attributeRestrictions: null
    resources:
    - imagestreamimages
    - imagestreamimports
    - imagestreammappings
    - imagestreams
    - imagestreamtags
    - templates
    verbs:
    - get
    - list
  - apiGroups: null
    attributeRestrictions: null
    resources:
    - imagestreams/layers
    verbs:
    - get
kind: List
metadata: {}
""".strip()

OC_GET_PV = """
apiVersion: v1
items:
- apiVersion: v1
  kind: PersistentVolume
  metadata:
    annotations:
      pv.kubernetes.io/bound-by-controller: "yes"
    creationTimestamp: 2017-03-09T15:23:17Z
    name: registry-volume
    resourceVersion: "745"
    selfLink: /api/v1/persistentvolumes/registry-volume
    uid: 52394d79-04dc-11e7-ab1f-001a4a0101d2
  spec:
    accessModes:
    - ReadWriteMany
    capacity:
      storage: 5Gi
    claimRef:
      apiVersion: v1
      kind: PersistentVolumeClaim
      name: registry-claim
      namespace: default
      resourceVersion: "743"
      uid: 52c44068-04dc-11e7-ab1f-001a4a0101d2
    nfs:
      path: /exports/registry
      server: master.ose33.com
    persistentVolumeReclaimPolicy: Retain
  status:
    phase: Bound
- apiVersion: v1
  kind: PersistentVolume
  metadata:
    creationTimestamp: 2017-04-05T10:44:54Z
    name: registry-volume-zjj
    resourceVersion: "934892"
    selfLink: /api/v1/persistentvolumes/registry-volume-zjj
    uid: e7519f6c-19ec-11e7-ab1f-001a4a0101d2
  spec:
    accessModes:
    - ReadWriteMany
    capacity:
      storage: 10Gi
    nfs:
      path: /nfs
      server: 10.66.208.147
    persistentVolumeReclaimPolicy: Recycle
  status:
    phase: Available
kind: List
metadata: {}
""".strip()

OC_GET_PVC = """
apiVersion: v1
items:
- apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    annotations:
      pv.kubernetes.io/bind-completed: "yes"
      pv.kubernetes.io/bound-by-controller: "yes"
    creationTimestamp: 2017-03-09T15:23:18Z
    name: registry-claim
    namespace: default
    resourceVersion: "747"
    selfLink: /api/v1/namespaces/default/persistentvolumeclaims/registry-claim
    uid: 52c44068-04dc-11e7-ab1f-001a4a0101d2
  spec:
    accessModes:
    - ReadWriteMany
    resources:
      requests:
        storage: 5Gi
    volumeName: registry-volume
  status:
    accessModes:
    - ReadWriteMany
    capacity:
      storage: 5Gi
    phase: Bound
- apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    annotations:
      pv.kubernetes.io/bind-completed: "yes"
    creationTimestamp: 2017-04-12T18:40:43Z
    name: registry-claim-test1
    namespace: default
    resourceVersion: "1084833"
    selfLink: /api/v1/namespaces/default/persistentvolumeclaims/registry-claim-test1
    uid: 89169428-1faf-11e7-b236-001a4a0101d2
  spec:
    accessModes:
    - ReadWriteMany
    resources:
      requests:
        storage: 5Gi
    volumeName: registry-volume-zjj
  status:
    accessModes:
    - ReadWriteMany
    capacity:
      storage: 10Gi
    phase: Bound
kind: List
metadata: {}
""".strip()

OC_GET_ENDPOINTS = """
apiVersion: v1
items:
- apiVersion: v1
  kind: Endpoints
  metadata:
    creationTimestamp: 2017-06-15T05:53:47Z
    name: gluster-cluster
    namespace: default
    resourceVersion: "35151"
    selfLink: /api/v1/namespaces/default/endpoints/gluster-cluster
    uid: ffaf2c59-518e-11e7-a93b-001a4a01010c
  subsets:
  - addresses:
    - ip: 10.64.221.124
    - ip: 10.64.221.126
    ports:
    - port: 1
      protocol: TCP
- apiVersion: v1
  kind: Endpoints
  metadata:
    creationTimestamp: 2017-06-14T05:55:59Z
    name: kubernetes
    namespace: default
    resourceVersion: "449"
    selfLink: /api/v1/namespaces/default/endpoints/kubernetes
    uid: 240884a8-50c6-11e7-aae8-001a4a01010c
  subsets:
  - addresses:
    - ip: 10.66.219.113
    ports:
    - name: https
      port: 8443
      protocol: TCP
    - name: dns-tcp
      port: 8053
      protocol: TCP
    - name: dns
      port: 8053
      protocol: UDP
- apiVersion: v1
  kind: Endpoints
  metadata:
    creationTimestamp: 2017-06-14T07:32:51Z
    labels:
      app: registry-console
      createdBy: registry-console-template
      name: registry-console
    name: registry-console
    namespace: default
    resourceVersion: "2858"
    selfLink: /api/v1/namespaces/default/endpoints/registry-console
    uid: ac78a94e-50d3-11e7-aae8-001a4a01010c
  subsets:
  - addresses:
    - ip: 10.128.0.3
      nodeName: node1.ose35.com
      targetRef:
        kind: Pod
        name: registry-console-1-jckp2
        namespace: default
        resourceVersion: "2854"
        uid: d5baeab5-50d3-11e7-aae8-001a4a01010c
    ports:
    - name: registry-console
      port: 9090
      protocol: TCP
kind: List
metadata: {}
resourceVersion: ""
selfLink: ""
""".strip()


def test_oc_get_pod_yml():
    result = openshift_get.OcGetPod(context_wrap(OC_GET_POD))
    assert result.data['items'][0]['metadata']['annotations']['openshift.io/scc'] == 'anyuid'
    assert result.data['items'][0]['metadata']['creationTimestamp'] == datetime.datetime(2017, 2, 10, 16, 33, 46)
    assert result.data['items'][0]['spec']['host'] == 'node2.ose.com'
    assert result.get("items")[0]['spec']['host'] == 'node2.ose.com'
    assert result.get_pod()["router-1-1-w27o2"]["metadata"]["labels"]["deploymentconfig"] == "router-1"


def test_oc_get_service_yml():
    result = openshift_get.OcGetService(context_wrap(OC_GET_SERVICE))
    assert result.data['items'][0]['kind'] == 'Service'
    assert result.data['items'][0]['spec']['clusterIP'] == '172.30.0.1'
    assert result.data['items'][0]['metadata']['name'] == 'kubernetes'
    assert result.data['items'][1]['metadata']['name'] == 'router-1'
    assert result.data['items'][1]['spec']['ports'][0]['port'] == 80
    assert result.data['kind'] == 'List'
    assert result.data['metadata'] == {}
    assert result.get("items")[0]['spec']['clusterIP'] == '172.30.0.1'
    assert "zjj-project" in result.data['items'][1]['metadata']['namespace']
    assert result.get_service()["router-1"]["metadata"]["resourceVersion"] == "1638401"


def test_oc_get_dc_yml():
    result = openshift_get.OcGetDc(context_wrap(OC_GET_DC))
    assert result.data['items'][0]['kind'] == 'DeploymentConfig'
    assert result.data['items'][0]['metadata']['generation'] == 3
    assert result.get("items")[0]['metadata']['generation'] == 3
    assert result.get_dc()["router-1"]["metadata"]["namespace"] == "zjj-project"


def test_oc_get_rolebinding_yml():
    result = openshift_get.OcGetRolebinding(context_wrap(OC_GET_ROLEBINDING))
    assert result.data['items'][0]['kind'] == 'RoleBinding'
    assert result.data['items'][0]['metadata']['resourceVersion'] == "11803596"
    assert result.get("items")[0]['metadata']['resourceVersion'] == "11803596"
    assert result.get_rolebind()["myrole"]["roleRef"]["namespace"] == "foo"


def test_oc_get_project_yml():
    result = openshift_get.OcGetProject(context_wrap(OC_GET_PROJECT))
    assert result.data['items'][0]['kind'] == 'Project'
    assert result.data['items'][0]['metadata']['resourceVersion'] == "11040756"
    assert result.get('items')[0]['metadata']['resourceVersion'] == "11040756"
    assert result.get_project()["test"]["status"]["phase"] == "Active"


def test_oc_get_role_yml():
    result = openshift_get.OcGetRole(context_wrap(OC_GET_ROLE))
    assert result.data['items'][0]['kind'] == 'Role'
    assert result.data['items'][0]['metadata']['resourceVersion'] == "94"
    assert result.get('items')[0]['metadata']['resourceVersion'] == "94"
    assert result.get_role()["shared-resource-viewer"]["metadata"]["uid"] == "a10c3f88-6ecc-11e6-83c6-001a4a0101f0"


def test_oc_get_pv_yml():
    result = openshift_get.OcGetPv(context_wrap(OC_GET_PV))
    assert result.data['items'][0]['kind'] == 'PersistentVolume'
    assert result.data['items'][0]['metadata']['name'] == 'registry-volume'
    assert result.get('items')[0]['metadata']['name'] == 'registry-volume'
    assert result.get_pv()['registry-volume-zjj']['spec']['capacity']['storage'] == '10Gi'


def test_oc_get_pvc_yml():
    result = openshift_get.OcGetPvc(context_wrap(OC_GET_PVC))
    assert result.data['items'][0]['kind'] == 'PersistentVolumeClaim'
    assert result.data['items'][0]['metadata']['name'] == 'registry-claim'
    assert result.get('items')[0]['metadata']['name'] == 'registry-claim'
    assert result.get_pvc()['registry-claim-test1']['spec']['volumeName'] == 'registry-volume-zjj'


def test_oc_get_endpoints_yml():
    result = openshift_get.OcGetEndPoints(context_wrap(OC_GET_ENDPOINTS))
    assert result.data['items'][0]['kind'] == 'Endpoints'
    assert result.data['items'][0]['metadata']['name'] == 'gluster-cluster'
    assert result.get('items')[0]['metadata']['name'] == 'gluster-cluster'
    assert result.get_endpoints()['kubernetes']['subsets'][0]["addresses"][0]["ip"] == '10.66.219.113'
