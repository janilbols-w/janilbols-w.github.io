---
title: Kubernetes
---

这个分区目前包含两篇互补文档：一篇讲概念，一篇讲终端交互命令。

## Documents

- [Kubernetes 核心概念概览指南]({{ '/garage/kubernetes/overview/' | relative_url }})
- [Kubernetes 终端交互常用命令指南]({{ '/garage/kubernetes/quickstart/' | relative_url }})

## Reading Order

1. 先看概念概览，建立 `Namespace -> Deployment -> Pod -> Service -> Ingress` 的对象关系。
2. 再看终端命令指南，把 `kubectl get/describe/logs/exec` 和这些对象对应起来。
