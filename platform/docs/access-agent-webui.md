# 访问 Agent OpenClaw Web UI (Control UI)

每个 Agent Pod 内置了 OpenClaw Control UI，可以通过端口转发直接访问，用于调试、查看日志、测试对话等。

## 前提条件

- `kubectl` 已配置并可访问 EKS 集群
- Agent Pod 处于 Running 状态

## 步骤

### 1. 查找 Agent Pod

```bash
# 列出所有租户 namespace 的 Agent Pod
kubectl get pods -A -l app.kubernetes.io/managed-by=openclaw-operator

# 或指定租户 namespace
kubectl get pods -n tenant-<tenant-name>
```

### 2. 获取 Gateway Token

Gateway Token 是访问 Control UI 的认证凭证，存储在 operator 自动创建的 Secret 中。

命名规则：`{agent-name}-gateway-token`

```bash
# 获取 token（替换 <agent-name> 和 <namespace>）
kubectl get secret <agent-name>-gateway-token -n <namespace> \
  -o jsonpath='{.data.token}' | base64 -d
```

示例：

```bash
# 租户 tenant-03 下的 agent-0308
kubectl get secret agent-0308-gateway-token -n tenant-tenant-03 \
  -o jsonpath='{.data.token}' | base64 -d
```

### 3. 端口转发

```bash
# 转发 Pod 的 18790 端口（nginx gateway-proxy）
kubectl port-forward pod/<agent-name>-0 18790:18790 -n <namespace>
```

示例：

```bash
kubectl port-forward pod/agent-0308-0 18790:18790 -n tenant-tenant-03
```

> **注意**：Pod 名称格式为 `{agent-name}-0`（StatefulSet 的第一个副本）。

### 4. 访问 Web UI

浏览器打开：**http://localhost:18790**

在登录页面输入上一步获取的 Gateway Token 即可进入。

## 端口说明

| 端口 | 服务 | 说明 |
|------|------|------|
| 18789 | openclaw gateway | 主进程 API（仅 loopback） |
| 18790 | nginx gateway-proxy | 反向代理入口（对外） |
| 18793 | openclaw canvas | Canvas 服务（仅 loopback） |
| 18794 | nginx canvas-proxy | Canvas 反向代理 |
| 9222 | chromium CDP | Chrome DevTools Protocol（如启用） |
| 9090 | metrics-exporter | Prometheus metrics |

## 一键脚本

```bash
#!/bin/bash
# Usage: ./access-agent.sh <agent-name> <namespace>
AGENT=${1:?Usage: $0 <agent-name> <namespace>}
NS=${2:?Usage: $0 <agent-name> <namespace>}

TOKEN=$(kubectl get secret ${AGENT}-gateway-token -n $NS -o jsonpath='{.data.token}' | base64 -d)
echo "Gateway Token: $TOKEN"
echo ""
echo "Starting port-forward... Open http://localhost:18790"
kubectl port-forward pod/${AGENT}-0 18790:18790 -n $NS
```

## 中国区（cn-northwest-1）

CN 区使用单独的 kubeconfig：

```bash
# 生成 CN kubeconfig
aws eks update-kubeconfig --name openclaw-saas-dev-cluster \
  --region cn-northwest-1 --kubeconfig /tmp/cn-kubeconfig --profile cn

# 使用 CN kubeconfig
export KUBECONFIG=/tmp/cn-kubeconfig
kubectl get secret <agent-name>-gateway-token -n <namespace> \
  -o jsonpath='{.data.token}' | base64 -d

kubectl port-forward pod/<agent-name>-0 18790:18790 -n <namespace>
```

## 安全注意事项

- Gateway Token 是敏感凭证，不要提交到代码仓库
- 端口转发仅在本地有效，不会暴露到公网
- 建议在调试完成后关闭端口转发
- Control UI 提供了对 Agent 的完全控制权限（查看对话、修改配置等）
