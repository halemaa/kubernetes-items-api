# Theory — start here

These notes explain this project from zero. No prior Kubernetes knowledge
assumed. Read in order:

1. [`01-what-is-kubernetes.md`](01-what-is-kubernetes.md) — the problem K8s solves and the one idea behind all of it (the control loop).
2. [`02-pods-and-deployments.md`](02-pods-and-deployments.md) — Pods, ReplicaSets, Deployments: what runs your containers.
3. [`03-services-and-labels.md`](03-services-and-labels.md) — how a stable address finds disposable Pods (the label trick).
4. [`04-config-and-secrets.md`](04-config-and-secrets.md) — ConfigMaps, Secrets, and the base64 truth.
5. [`05-healing-scaling-workflow.md`](05-healing-scaling-workflow.md) — self-healing, autoscaling, rolling updates, and the day-to-day workflow.

Running analogy throughout: a **shipping port**. Containers are cargo, Pods are
the crates they ship in, Nodes are the ships, and the control plane is the
harbour master who keeps the whole operation running to plan.
