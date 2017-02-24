from falafel.mappers import openshift_get
from falafel.tests import context_wrap
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


def test_oc_get_pod_yml():
    result = openshift_get.OcGetPod(context_wrap(OC_GET_POD))
    assert result.data['items'][0]['metadata']['annotations']['openshift.io/scc'] == 'anyuid'
    assert result.data['items'][0]['metadata']['creationTimestamp'] == datetime.datetime(2017, 2, 10, 16, 33, 46)
    assert result.data['items'][0]['spec']['host'] == 'node2.ose.com'
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
    assert "zjj-project" in result.data['items'][1]['metadata']['namespace']
    assert result.get_service()["router-1"]["metadata"]["resourceVersion"] == "1638401"


def test_oc_get_dc_yml():
    result = openshift_get.OcGetDc(context_wrap(OC_GET_DC))
    assert result.data['items'][0]['kind'] == 'DeploymentConfig'
    assert result.data['items'][0]['metadata']['generation'] == 3
    assert result.get_dc()["router-1"]["metadata"]["namespace"] == "zjj-project"
