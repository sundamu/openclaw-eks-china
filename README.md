# OpenClaw SaaS on EKS (China Region)

Multi-tenant OpenClaw SaaS platform running on Amazon EKS in **AWS China Region** (cn-northwest-1).

## Structure

```
platform/    - Management API + Web Console + Billing + Metrics Exporter
infra/       - CDK IaC + Helm + K8s manifests + Monitoring + CI/CD
contracts/   - Shared contracts: API specs, CRD conventions, event schemas
```

## Architecture

- **EKS** (K8s 1.30, Graviton arm64) — cn-northwest-1 (Ningxia)
- **RDS PostgreSQL** — tenant/agent/billing data
- **K8s Operator** — OpenClaw instance lifecycle management
- **Per-tenant namespace isolation** with ResourceQuota + NetworkPolicy + LimitRange
- **Metrics pipeline** — Prometheus sidecar → SQS → Billing aggregator

## China Region Differences

| Feature | Global | China (cn) |
|---|---|---|
| **ARN prefix** | `arn:aws` | `arn:aws-cn` |
| **STS endpoint** | `sts.amazonaws.com` | `sts.amazonaws.com.cn` |
| **ECR domain** | `.ecr.{region}.amazonaws.com` | `.ecr.{region}.amazonaws.com.cn` |
| **Bedrock** | ✅ Available | ❌ Not available |
| **LLM providers** | Bedrock (IRSA), OpenAI, Anthropic | OpenAI, Anthropic, OpenAI-compatible |
| **Default region** | us-west-2 | cn-northwest-1 |
| **AWS Account** | 956045422469 | 735091234506 |

## Branches

- `main` — Global region deployment (us-west-2)
- `cn` — China region deployment (cn-northwest-1)

## Deploy

```bash
# Set China region credentials
export AWS_PROFILE=cn
export CDK_DEFAULT_ACCOUNT=735091234506
export CDK_DEFAULT_REGION=cn-northwest-1

# Deploy infrastructure
cd infra/cdk && cdk deploy --all

# Or use the deploy script
cd infra && ./scripts/deploy.sh
```
