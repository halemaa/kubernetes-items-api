# 5. Self-healing, scaling, and the workflow

## Health probes — how K8s knows a Pod's real state
A container being "started" doesn't mean it's healthy. Probes tell Kubernetes
the truth:

- **liveness** — "is it alive?" Fails → kubelet **restarts** the container.
  Self-heals a hung or deadlocked app.
- **readiness** — "can it take traffic *yet*?" Fails → the Service **stops
  sending it requests** (without restarting it). This is what makes rolling
  updates zero-downtime: a new Pod receives traffic only once it reports ready.
- **startup** — grace period for slow-booting apps before liveness kicks in.

Both probes in this project hit `/health` — see
[`k8s/deployment.yaml`](../k8s/deployment.yaml).

## Self-healing in action
A node dies → its Pods vanish → the ReplicaSet controller sees "2 of 3 running"
→ schedules replacements on healthy nodes. No human. Try it:

```bash
kubectl -n items-api delete pod -l app=items-api | head -1
kubectl -n items-api get pods -w     # a replacement appears in seconds
```

## Scaling
- **Manual**: change `replicas` and re-apply.
- **HPA (HorizontalPodAutoscaler)**: watches CPU and changes the replica count
  automatically between a floor and ceiling. This project's
  [`k8s/hpa.yaml`](../k8s/hpa.yaml) scales 3→10 Pods when average CPU passes 70%.

## Rolling updates and rollbacks
Change the image and re-apply, and the Deployment swaps Pods a few at a time
(`maxSurge`/`maxUnavailable` control the pace), so the app stays up. If the new
version is bad:

```bash
kubectl -n items-api rollout undo deployment/items-api
```

## The workflow, precisely
1. Write YAML manifests (Deployment, Service, ConfigMap, Secret…).
2. `kubectl apply -f k8s/` → the **API server** stores desired state in **etcd**.
3. Controllers create Pods → the **scheduler** places them on nodes → **kubelets**
   pull images and start containers → report status.
4. `kubectl get` / `describe` / `logs` to observe; the loop self-heals and scales.
5. Update by editing YAML and re-applying → rolling update. `rollout undo` to revert.

## The one-sentence version
> Probes tell Kubernetes which Pods are healthy, the control loop replaces the
> ones that aren't, the HPA adds Pods under load, and a rolling update swaps
> versions without downtime — all from you changing YAML and running
> `kubectl apply`.

That's the whole system. Back to the [README](../README.md) to run it.
