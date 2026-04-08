# Kubernetes 终端交互常用命令指南

这份文档面向日常通过终端操作 Kubernetes 集群的场景，重点覆盖 `kubectl` 的常见交互动作：查看集群状态、定位资源、进入 Pod、看日志、发布变更和排查问题。

## 1. 基础准备

确认 `kubectl` 已安装并且当前 kubeconfig 可用。

```bash
kubectl version --client
kubectl config get-contexts
kubectl config current-context
kubectl cluster-info
```

如果本机管理多个集群，先切换上下文：

```bash
kubectl config use-context <context-name>
```

如果你经常操作某一个 namespace，可以设置默认 namespace：

```bash
kubectl config set-context --current --namespace=<namespace>
```

查看当前上下文的详细配置：

```bash
kubectl config view --minify
```

## 2. 提高终端交互效率

建议配置别名和自动补全。

```bash
alias k=kubectl
complete -F __start_kubectl k
```

在 zsh 中常见配置方式：

```bash
echo 'alias k=kubectl' >> ~/.zshrc
echo 'source <(kubectl completion zsh)' >> ~/.zshrc
echo 'compdef k=kubectl' >> ~/.zshrc
source ~/.zshrc
```

后续示例中，`kubectl` 和 `k` 可以等价替换。

## 3. 查看集群和节点

查看节点列表：

```bash
kubectl get nodes
kubectl get nodes -o wide
```

查看节点详情：

```bash
kubectl describe node <node-name>
```

查看所有 namespace：

```bash
kubectl get ns
```

查看集群中所有 Pod：

```bash
kubectl get pods -A
kubectl get pods -A -o wide
```

## 4. 最常用的资源查看命令

查看某个 namespace 下的核心资源：

```bash
kubectl get pods
kubectl get svc
kubectl get deploy
kubectl get rs
kubectl get ds
kubectl get sts
kubectl get ing
kubectl get cm
kubectl get secret
```

跨 namespace 查看：

```bash
kubectl get pods -n <namespace>
kubectl get deploy -n <namespace>
kubectl get svc -n <namespace>
```

输出更详细的信息：

```bash
kubectl get pod <pod-name> -o wide
kubectl get pod <pod-name> -o yaml
kubectl get deploy <deploy-name> -o yaml
```

根据 label 过滤资源：

```bash
kubectl get pods -l app=<app-name>
kubectl get pods -l app=<app-name>,version=<version>
```

只看某类资源名称：

```bash
kubectl get pods -o name
kubectl get deploy -o name
```

持续观察资源变化：

```bash
kubectl get pods -w
kubectl get pod <pod-name> -w
```

## 5. describe 是排障第一入口

当资源状态异常时，优先看 `describe`。

```bash
kubectl describe pod <pod-name>
kubectl describe deploy <deploy-name>
kubectl describe svc <svc-name>
kubectl describe ingress <ingress-name>
```

重点关注以下内容：

- `Events`：调度失败、镜像拉取失败、探针失败等信息通常都在这里。
- `Conditions`：Pod 是否 Ready，Deployment 是否 Available。
- `Containers`：镜像、启动命令、端口、探针、挂载卷是否符合预期。

## 6. 进入 Pod 进行交互

进入单容器 Pod：

```bash
kubectl exec -it <pod-name> -- /bin/sh
```

如果镜像里有 bash：

```bash
kubectl exec -it <pod-name> -- /bin/bash
```

进入多容器 Pod 中指定容器：

```bash
kubectl exec -it <pod-name> -c <container-name> -- /bin/sh
```

在容器中直接执行单条命令：

```bash
kubectl exec <pod-name> -- env
kubectl exec <pod-name> -- ps aux
kubectl exec <pod-name> -- ls /app
```

执行网络联通性测试：

```bash
kubectl exec -it <pod-name> -- curl http://<service-name>:<port>
kubectl exec -it <pod-name> -- nslookup <service-name>
```

## 7. 查看日志

查看单个 Pod 日志：

```bash
kubectl logs <pod-name>
```

实时跟踪日志：

```bash
kubectl logs -f <pod-name>
```

查看最近 100 行：

```bash
kubectl logs --tail=100 <pod-name>
```

查看带时间戳的日志：

```bash
kubectl logs --timestamps <pod-name>
```

多容器 Pod 指定容器日志：

```bash
kubectl logs <pod-name> -c <container-name>
kubectl logs -f <pod-name> -c <container-name>
```

查看上一次崩溃前的日志：

```bash
kubectl logs --previous <pod-name>
kubectl logs --previous <pod-name> -c <container-name>
```

根据 label 批量查看一组 Pod 日志：

```bash
kubectl logs -l app=<app-name> --tail=100
```

## 8. Deployment 常见操作

查看 Deployment：

```bash
kubectl get deploy
kubectl describe deploy <deploy-name>
```

查看滚动发布状态：

```bash
kubectl rollout status deploy/<deploy-name>
```

查看发布历史：

```bash
kubectl rollout history deploy/<deploy-name>
```

回滚到上一个版本：

```bash
kubectl rollout undo deploy/<deploy-name>
```

回滚到指定 revision：

```bash
kubectl rollout undo deploy/<deploy-name> --to-revision=<revision>
```

重启 Deployment：

```bash
kubectl rollout restart deploy/<deploy-name>
```

扩缩容：

```bash
kubectl scale deploy/<deploy-name> --replicas=3
```

## 9. 资源创建和更新

基于 YAML 创建或更新资源：

```bash
kubectl apply -f app.yaml
kubectl apply -f k8s/
```

查看 apply 差异：

```bash
kubectl diff -f app.yaml
```

删除资源：

```bash
kubectl delete -f app.yaml
kubectl delete pod <pod-name>
kubectl delete deploy <deploy-name>
```

直接编辑在线资源：

```bash
kubectl edit deploy <deploy-name>
kubectl edit cm <configmap-name>
```

导出当前资源定义作为排查参考：

```bash
kubectl get deploy <deploy-name> -o yaml > deploy.yaml
kubectl get pod <pod-name> -o yaml > pod.yaml
```

## 10. 镜像、标签和注解

更新 Deployment 的镜像：

```bash
kubectl set image deploy/<deploy-name> <container-name>=<image>:<tag>
```

给资源添加标签：

```bash
kubectl label pod <pod-name> env=test
```

覆盖已有标签：

```bash
kubectl label pod <pod-name> env=prod --overwrite
```

添加注解：

```bash
kubectl annotate pod <pod-name> owner=janil
```

## 11. Service 与端口转发

查看 Service：

```bash
kubectl get svc
kubectl describe svc <svc-name>
```

把集群内服务映射到本地端口：

```bash
kubectl port-forward svc/<svc-name> 8080:80
kubectl port-forward pod/<pod-name> 8080:8080
```

这在本地调试 HTTP 接口、Prometheus、Grafana、内部管理页面时非常常用。

## 12. 文件拷贝

从本地复制到 Pod：

```bash
kubectl cp ./local.txt <pod-name>:/tmp/local.txt
```

从 Pod 复制到本地：

```bash
kubectl cp <pod-name>:/var/log/app.log ./app.log
```

多容器 Pod 指定容器：

```bash
kubectl cp ./local.txt <namespace>/<pod-name>:/tmp/local.txt -c <container-name>
```

## 13. 资源使用情况

查看节点资源使用：

```bash
kubectl top nodes
```

查看 Pod 资源使用：

```bash
kubectl top pods
kubectl top pods -A
```

如果提示 `Metrics API not available`，通常表示集群还没有安装 metrics-server。

## 14. 查看事件

排查问题时，事件流经常比日志更快暴露根因。

```bash
kubectl get events
kubectl get events -n <namespace>
kubectl get events --sort-by=.metadata.creationTimestamp
```

只看某个 Pod 相关事件：

```bash
kubectl describe pod <pod-name>
```

## 15. 常见故障排查路径

### 15.1 Pod 一直 Pending

先看调度信息：

```bash
kubectl get pod <pod-name>
kubectl describe pod <pod-name>
```

常见原因：

- 节点资源不足。
- `nodeSelector`、`affinity`、`taints/tolerations` 不匹配。
- PVC 没绑定成功。

### 15.2 Pod CrashLoopBackOff

建议排查顺序：

```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs --previous <pod-name>
```

重点看：

- 启动命令是否正确。
- 配置文件、环境变量、密钥是否缺失。
- liveness/readiness probe 是否过严。

### 15.3 Service 不通

建议排查顺序：

```bash
kubectl get svc <svc-name>
kubectl describe svc <svc-name>
kubectl get endpoints <svc-name>
kubectl get pods -l app=<app-name> -o wide
```

重点看：

- Service selector 是否匹配到 Pod。
- Pod 是否 Ready。
- 端口映射 `port/targetPort` 是否正确。

### 15.4 Deployment 发布卡住

```bash
kubectl rollout status deploy/<deploy-name>
kubectl describe deploy <deploy-name>
kubectl get rs
kubectl get pods -l app=<app-name>
```

重点看：

- 新 Pod 是否启动失败。
- readiness probe 是否导致无法切流。
- 镜像拉取是否失败。

## 16. 调试型命令

临时起一个调试 Pod：

```bash
kubectl run debug --rm -it --image=busybox -- /bin/sh
```

起一个带 curl 的临时容器：

```bash
kubectl run curl-test --rm -it --image=curlimages/curl -- sh
```

在支持 ephemeral containers 的集群中，也可以给现有 Pod 注入调试容器：

```bash
kubectl debug -it <pod-name> --image=busybox --target=<container-name>
```

## 17. 实用输出技巧

只打印某个字段：

```bash
kubectl get pod <pod-name> -o jsonpath='{.status.podIP}'
kubectl get pods -o custom-columns=NAME:.metadata.name,IP:.status.podIP,NODE:.spec.nodeName
```

查看镜像列表：

```bash
kubectl get pods -A -o custom-columns=NS:.metadata.namespace,POD:.metadata.name,IMAGE:.spec.containers[*].image
```

结合 grep 过滤：

```bash
kubectl get pods -A | grep Running
kubectl get events -A | grep Failed
```

## 18. 推荐的日常操作习惯

- 操作生产集群前，先执行 `kubectl config current-context`。
- 删除和变更资源前，优先 `get` 或 `describe` 再执行写操作。
- 发布前先 `kubectl diff -f ...`，确认变更范围。
- 排障时先看 `describe` 和 `events`，再深入看日志和容器内部状态。
- 对频繁使用的 namespace 设置默认值，减少误操作。

## 19. 一组高频命令速查

```bash
# 上下文与命名空间
kubectl config current-context
kubectl config use-context <context-name>
kubectl config set-context --current --namespace=<namespace>

# 查看资源
kubectl get pods -A
kubectl get svc -n <namespace>
kubectl describe pod <pod-name>

# 日志与进入容器
kubectl logs -f <pod-name>
kubectl logs --previous <pod-name>
kubectl exec -it <pod-name> -- /bin/sh

# 发布与回滚
kubectl apply -f app.yaml
kubectl rollout status deploy/<deploy-name>
kubectl rollout undo deploy/<deploy-name>

# 调试
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl port-forward svc/<svc-name> 8080:80
kubectl top pods -A
```

如果只记住一条排障思路，可以按下面这个顺序执行：

```bash
kubectl get pod <pod-name> -o wide
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs --previous <pod-name>
kubectl exec -it <pod-name> -- /bin/sh
```
