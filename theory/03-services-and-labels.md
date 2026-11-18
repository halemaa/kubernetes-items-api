# 3. Services and labels

## The problem a Service solves
Pods are disposable and their IPs change constantly. So how does anything find
them reliably? You can't hand out a Pod's IP — it'll be gone by lunchtime.

A **Service** gives a **permanent virtual IP and DNS name** and load-balances
across whichever Pods are currently healthy. It's the receptionist with a fixed
phone number in front of a room of staff who come and go.

Service types:
- **ClusterIP** (default) — reachable only *inside* the cluster. Used here.
- **NodePort** — opens a fixed port on every node for basic external access.
- **LoadBalancer** — provisions a real cloud load balancer for proper external access.
- **Ingress** — an HTTP router in front, directing by hostname/path through one entry point.

## The hidden glue: labels and selectors
Here's the part most tutorials skip, and interviewers love. Kubernetes objects
are **not wired together by name or nesting — they're connected by labels**, which
are just key-value tags.

- The Pods carry a label: `app: items-api`.
- The Deployment's `selector` says "I manage Pods matching `app: items-api`."
- The Service's `selector` says "I route to Pods matching `app: items-api`."

Nothing holds a direct reference to anything else. They **find each other by
matching labels at runtime.** That loose coupling is exactly *why* Pods can be
replaced freely: the Service doesn't track specific Pods, it tracks a *label*,
and whichever Pods currently wear it get traffic.

**The classic bug:** if the Pod label and the Service selector don't match, the
Service routes to nothing and you get connection errors with everything looking
"up." Diagnose it with `kubectl -n items-api get endpoints` — empty endpoints
means the labels don't line up.

## DNS
Every Service gets an internal DNS name
(`items-api.items-api.svc.cluster.local`), so apps reach each other by name,
never by IP.

## The one-sentence version
> A **Service** is a stable front door that finds its **Pods** by matching a
> **label**, not by name — which is what lets Pods be disposable without ever
> breaking the address clients use.

Next: [feeding config and secrets in →](04-config-and-secrets.md)
