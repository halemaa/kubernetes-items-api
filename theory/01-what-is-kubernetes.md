# 1. What is Kubernetes?

## The problem

Docker lets you put an app in a **container** that runs anywhere. Great — until
you have many containers across many machines, and they crash, get overloaded,
or need updating without downtime. Doing that by hand, at 3am, is impossible.

**Kubernetes is the manager that runs your containers for you and keeps them
alive.** You tell it what you want running; it makes that true and keeps it true.

## The one idea: the control loop

Everything in Kubernetes is the same loop, repeated for every object:

> Read the **desired state** (what you asked for). Read the **actual state**
> (what's really running). If they differ, act to close the gap. Repeat forever.

Every object has a `spec` (desired) and a `status` (actual). "3 replicas" is a
spec. "2 running, one just crashed" is a status. A controller sees the gap and
starts a third Pod — no human involved. That continuous reconciliation is why
Kubernetes **self-heals**, and it's the difference from Terraform, which
reconciles once when you run it.

## The pieces that run the loop

- **Control plane** (the harbour master):
  - **API server** — the only front door; everything goes through it.
  - **etcd** — the cluster's memory; stores all desired state.
  - **Scheduler** — picks which node each new Pod runs on.
  - **Controllers** — run the reconciliation loops.
- **Nodes** (the ships, where work happens):
  - **kubelet** — the agent that starts containers and reports status.
  - **container runtime** — actually runs the containers.
  - **kube-proxy** — wires up Service networking.

You declare intent to the control plane; the nodes make it real and report back.

## The one-sentence version

> Kubernetes keeps a continuous loop comparing what you *want* running to what
> *is* running, and fixes any difference automatically — so your app survives
> crashes, updates, and traffic spikes without you watching.

Next: [what actually runs your containers →](02-pods-and-deployments.md)
