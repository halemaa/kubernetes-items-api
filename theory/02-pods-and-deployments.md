# 2. Pods, ReplicaSets, Deployments

## Pod — the smallest unit
A **Pod** is one (or a few tightly-coupled) containers that share a network
identity (one IP) and storage. It's the crate your cargo ships in. Two key
facts:

- Pods are **disposable**. They get a random name and IP, and when one dies it's
  *gone* — replaced by a brand-new Pod with a new IP.
- You almost **never create a Pod directly**, because a lone Pod has no
  self-healing. Kill it and nothing brings it back.

## ReplicaSet — keep N alive
A **ReplicaSet** has one job: keep exactly N identical Pods running. If a Pod
dies, it makes a new one. This is the control loop in its simplest form.

## Deployment — the one you actually use
A **Deployment** manages ReplicaSets to give you **rolling updates and
rollbacks**:

```
Deployment  ->  ReplicaSet  ->  Pods
```

When you change the container image, the Deployment creates a *new* ReplicaSet
and scales it up while scaling the old one down, a few Pods at a time — so the
app never fully goes offline. Roll back (`kubectl rollout undo`) and it simply
scales the old ReplicaSet back up.

In this project, [`k8s/deployment.yaml`](../k8s/deployment.yaml) declares
`replicas: 3`. That single line is a desired state the ReplicaSet controller
defends around the clock.

## Other controllers (for other shapes)
- **StatefulSet** — Pods with stable identities and their own persistent storage
  (databases).
- **DaemonSet** — exactly one Pod per node (log/metric agents).
- **Job / CronJob** — run-to-completion tasks, once or on a schedule.

## The one-sentence version
> You declare a **Deployment**; it manages a **ReplicaSet**; the ReplicaSet keeps
> your **Pods** alive — so the unit you think about is "the app and how many
> copies," not individual containers.

Next: [how traffic finds disposable Pods →](03-services-and-labels.md)
