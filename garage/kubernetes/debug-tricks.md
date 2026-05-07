# DEBUG TRICKS FOR K8S

## 1 Pod Status
```bash
# search your pod
kubectl --namespace <ns> get pods -o wide

# check pod status
kubectl --namespace <ns> describe pod <pod-name>
```

## 2 Get Pod by Service
```bash
kubectl --namespace <ns> get svc -o wide
```

## 3 Get Ingress
```bash
kubectl --namespace <ns> get ingress -o wide
```
