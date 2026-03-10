# OpenClaw SaaS Platform

Management API, Web Console, Billing, and Metrics Exporter for OpenClaw on EKS.

## Components

| Component | Description | Tech |
|-----------|-------------|------|
| `api/` | Management API | Python FastAPI |
| `billing/` | Billing Worker (SQS consumer + Stripe) | Python |
| `metrics-exporter/` | Sidecar for Agent Pods | Python |
| `web-console/` | Frontend | React / Next.js |

## Documentation

| Document | Description |
|----------|-------------|
| [Access Agent Web UI](docs/access-agent-webui.md) | Port-forward + Gateway Token guide |
| [Channel Management](docs/channel-management.md) | Bind/unbind messaging channels |
| [Chromium Sidecar](docs/chromium-sidecar.md) | Browser automation sidecar setup |

## Architecture

See [openclaw-saas-contracts/docs/architecture.md](https://github.com/duchenxi/openclaw-saas-contracts/blob/main/docs/architecture.md)
