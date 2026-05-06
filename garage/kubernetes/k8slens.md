# K8s Lens
The new standard for Cloud Native software development & operations.
可视化k8s资源管理客户端


## 1 References
    - https://docs.k8slens.dev/
    - https://lenshq.io/
    - https://github.com/lensapp/lens

## 2 Quickstart

### 2.1 Download
download pkg from official site & install
- https://lenshq.io/download
### 2.2 check your remote host k8s info
```bash
ssh /to/your/remote/host
kubectl config view --minify --raw
```

e.g. outputs
```bash
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: Lxxxxxxx3NxeUphOXRpMFBna2ZRY3NmaWNJTxxxxTIyZEt3aVo5RlpZRXNFaXhJOWZJdzg4ZVdMRHEKbE5rWTE1L2FiNjZPcnpwQWZCbnRzNmZPWFZoVmc3bnNveWNoV2pOL2kvTWI4b2pnVy80anY0ZmozdnVsdzNvUAp0MTIrVjdTZWR6YTdkeWc1VExkalVmenMvOTRWT2xxxxxiRWxtWXA0RzZQYS9EVQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://<k8s-host>:<port>
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    namespace: <namespace>
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
current-context: kubernetes-admin@kubernetes
kind: Config
preferences: {}
users:
- name: kubernetes-admin
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUxxxxYlRYZHEyWjNiCjFRTkkvZVFDZUJSY0t5exxxtLS0tLQo=
    client-key-data: LS0xxxxxCSWM0TEo2VzUwbmovQW9HQkFbsTVdLUmpxbWh3OVNBYWhpTm01SGhJME9rYklQUGNBR0lXdGQ1ZUZmVUNvS2JYdEVSblZucDl1exxxVkJWem9XdmdhOURiUElKdk1uCmVKM1NidysrbEdseGJoRDFQcDRiQk9aa2tmaExxxxF2CkhzNktXWkbbbR0Fmck5iajgzKzI1eTJaUFo0Y1pnTFhvcjV2dm0rc3Q1R1lkxxxxRZXlrOXVNcmVhYmJFPQotLS0tddRSBLRVktLS0tLQo=

```
### 2.3 paste your k8s config to lens/local_kubeconfigs
you shall run it directly