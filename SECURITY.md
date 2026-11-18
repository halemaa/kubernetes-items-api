# Security considerations

Security was designed into the manifests, not added later. This documents what
is protected and how — and, just as importantly, what is deliberately left for
production hardening, with the fix for each.

## What this project does well

### 1. Containers run as non-root
The Dockerfile creates an unprivileged `appuser` (UID 10001) and the Deployment
enforces `runAsNonRoot: true`. If an attacker breaks out of the app, they land
as a low-privilege user, not root.

### 2. A hardened container runtime
The Pod sets `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`,
`capabilities: drop: [ALL]`, and `seccompProfile: RuntimeDefault`. That removes
the most common breakout paths: no new privileges, no writing to the container
filesystem, no Linux capabilities, syscalls filtered.

### 3. Resource limits (a security control, not just cost)
CPU and memory `limits` stop a compromised or buggy Pod from starving the node
and taking down its neighbours (a denial-of-service by resource exhaustion).

### 4. Health probes for safe recovery
Liveness restarts a hung container; readiness keeps traffic off a Pod until it
is actually ready, so a bad rollout never serves errors.

### 5. Config and secrets kept out of the image
Configuration comes from a ConfigMap and the token from a Secret, injected at
runtime — nothing sensitive is baked into the image layers.

### 6. Minimal, pinned base image
`python:3.12-slim` with no extra packages (standard library only) means a small
attack surface and nothing extra to patch or scan.

## Known limitations (and the production fix for each)

| # | Limitation | Risk | Fix |
|---|------------|------|-----|
| 1 | **The Secret is only base64-encoded, not encrypted**, and committed to git as a demo value. | Anyone with cluster/repo read access can decode it. | Never commit real Secrets. Use Sealed Secrets or an external vault (e.g. Vault, AWS/GCP secret managers) and enable **encryption at rest for etcd**. |
| 2 | **No NetworkPolicy** — any Pod in the cluster can reach these Pods. | Lateral movement if another workload is compromised. | Add a NetworkPolicy allowing traffic only from the Service/Ingress. |
| 3 | **No RBAC / dedicated ServiceAccount** shown. | Over-broad permissions by default. | Bind a least-privilege ServiceAccount; restrict who can read Secrets in the namespace. |
| 4 | **The API token check is simple string equality**, and the API is unauthenticated otherwise. | Weak access control. | Use an ingress-level authenticator (OAuth2 proxy, JWT) for real auth. |
| 5 | **No image signing or scanning in CI** (the pipeline builds but doesn't scan). | A vulnerable image could ship. | Add Trivy image scanning and Cosign signing to the workflow. |
| 6 | **In-memory data, no encryption of data in transit inside the cluster.** | Plaintext east-west traffic. | Terminate TLS at an Ingress; consider a service mesh (mTLS) for internal traffic. |

## Reporting

This is a personal portfolio project. If you spot a security issue, please open
an issue on the repository.
