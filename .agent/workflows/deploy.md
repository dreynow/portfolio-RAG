---
description: How to deploy changes to the portfolio project
---

# Deployment Process

Follow these steps to deploy changes based on the type of update.

## 1. For Code Changes (Frontend/Backend)

Run these commands from `/home/mother/homelab/portfolio`:

1. **Commit changes**:
   ```bash
   git add .
   git commit -m "Your change description"
   ```

2. **Build and push Docker image**:
   ```bash
   docker build -t dreyybaba/chat:latest .
   docker push dreyybaba/chat:latest
   ```

3. **Restart the pod to pull new image**:
   ```bash
   KUBECONFIG=/home/mother/homelab/kubeconfig kubectl delete pod -n portfolio -l app=portfolio
   ```

## 2. For Kubernetes Config Changes (Memory, Replicas, Env Vars)

Run these commands from `/home/mother/homelab/volta/alpha-uno`:

1. **Commit and push**:
   ```bash
   git add .
   git commit -m "Your change description"
   git push
   ```
   *FluxCD will automatically sync within ~30 seconds.*

---

## Quick Reference Table

| Change Type | Location | Deploy Method |
| :--- | :--- | :--- |
| **Python/Frontend code** | `/home/mother/homelab/portfolio/` | Docker build → push → delete pod |
| **K8s deployment config** | `volta/alpha-uno/apps/portfolio/` | Git push (FluxCD auto-syncs) |
| **Cloudflare tunnel config** | `volta/alpha-uno/apps/cloudflared/` | Git push (FluxCD auto-syncs) |
| **vLLM config** | `/home/mother/homelab/portfolio/gpu/` | `sudo systemctl restart vllm` |
