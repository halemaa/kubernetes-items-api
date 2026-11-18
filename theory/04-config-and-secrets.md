# 4. Config and Secrets

Apps need settings (a greeting, a limit) and sensitive values (a token). You
*could* bake them into the image — but then every change means a rebuild, and
secrets end up in image layers forever. Kubernetes separates them out.

## ConfigMap — non-secret settings
A **ConfigMap** holds plain configuration and injects it into Pods as
environment variables or files. Change it and re-apply to reconfigure the app
**without rebuilding the image**. In this project
[`k8s/configmap.yaml`](../k8s/configmap.yaml) sets `GREETING` and `MAX_ITEMS`,
and the Deployment pulls them in with `envFrom`.

## Secret — sensitive values
A **Secret** works the same way for things like tokens and passwords. Here it
holds `API_TOKEN`.

## The truth about Secrets (important for a security CV)
A Kubernetes Secret is only **base64-encoded, not encrypted.** Base64 is just a
reversible text encoding — anyone who can read the Secret can decode it in one
command:

```bash
echo "ZGVtby10b2tlbg==" | base64 -d
```

So a Secret protects against *shoulder-surfing in YAML*, not against an attacker
with cluster access. Real protection needs:

- **Encryption at rest for etcd** (so the stored value is actually encrypted).
- **RBAC** restricting who can read Secrets in the namespace.
- **Sealed Secrets or an external vault** so you never commit a real secret to git.

The token in this repo is a deliberately fake demo value, safe to be public.
Knowing this base64-vs-encryption distinction is exactly the kind of detail that
makes a security-minded candidate stand out.

## The one-sentence version
> **ConfigMaps** and **Secrets** inject settings into Pods at runtime instead of
> baking them into the image — but a Secret is only base64-encoded, so real
> safety comes from encrypting etcd and locking down who can read it.

Next: [self-healing, scaling, and the workflow →](05-healing-scaling-workflow.md)
