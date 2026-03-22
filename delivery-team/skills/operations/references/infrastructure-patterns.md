# Infrastructure Patterns

## Infrastructure as Code Principles

### Core Tenets

- **Declarative over imperative** -- Describe the desired end state, not the steps to get there. The tool determines what changes are needed.
- **Idempotent** -- Running the same configuration multiple times produces the same result. No side effects from re-application.
- **Version controlled** -- All infrastructure definitions live in Git. Changes go through pull requests and code review.
- **Tested** -- Infrastructure changes are validated before application: syntax checking, plan review, policy checks, integration tests against ephemeral environments.
- **Self-documenting** -- The code is the documentation of the current infrastructure state. No separate infrastructure wiki that drifts from reality.

### Repository Structure

- Separate infrastructure code from application code (dedicated infra repository or top-level directory)
- Organize by environment, region, or service depending on scale
- Pin provider and module versions -- do not use "latest" for infrastructure modules
- Include a README describing how to plan, apply, and destroy infrastructure

---

## Terraform Patterns

### Module Design

- Encapsulate reusable infrastructure components into modules (networking, compute, database, monitoring)
- Modules accept inputs via variables and expose outputs for composition
- Version modules independently using Git tags or a module registry
- Keep modules focused: one module per logical resource group (e.g., a "vpc" module, not a "everything" module)

### State Management

- **Remote state** is mandatory for team environments -- never store state locally in production workflows
- Use state locking (DynamoDB for AWS, GCS for GCP) to prevent concurrent modifications
- Separate state files per environment (dev, staging, production) -- never share state across environments
- State contains sensitive data -- encrypt at rest and restrict access to the state backend
- Periodically audit state for drift using `terraform plan` in CI

### Workspaces vs Separate State Files

- **Workspaces** -- Suitable for environments with identical structure differing only in variables (e.g., dev/staging/prod with same topology)
- **Separate state files** -- Preferred when environments have structural differences or when teams need independent blast radius
- Do not use workspaces as a substitute for proper environment isolation

### Remote Backends

| Backend | Locking | Encryption | Access Control | Best For |
|---------|---------|------------|----------------|----------|
| S3 + DynamoDB | Yes | Yes (SSE) | IAM policies | AWS environments |
| GCS | Yes | Yes | IAM policies | GCP environments |
| Azure Blob | Yes | Yes | RBAC | Azure environments |
| Terraform Cloud | Yes | Yes | Team/org permissions | Multi-cloud, team collaboration |

---

## Container Orchestration

### Kubernetes Core Concepts

**Pods** -- The smallest deployable unit. One or more containers sharing network and storage. Pods are ephemeral -- they can be killed and recreated at any time.

**Deployments** -- Manage ReplicaSets and pod lifecycle. Define desired state (replicas, image version, resource limits). Handle rolling updates and rollbacks.

**Services** -- Stable network endpoint for a set of pods. Types: ClusterIP (internal), NodePort (external via node), LoadBalancer (cloud LB), ExternalName (DNS alias).

**Ingress** -- HTTP/HTTPS routing from outside the cluster to services. Supports path-based and host-based routing, TLS termination, and rate limiting.

**Horizontal Pod Autoscaler (HPA)** -- Scales pod replicas based on CPU, memory, or custom metrics. Configure min/max replicas and target utilization.

### Resource Management

- **Always set resource requests and limits** -- Requests guarantee minimum resources; limits cap maximum consumption
- **Requests drive scheduling** -- The scheduler uses requests to place pods on nodes with sufficient capacity
- **Limits prevent noisy neighbors** -- A runaway process cannot consume all node resources
- Right-size resources based on actual usage data, not guesses -- use metrics from monitoring

### Namespace Strategy

- Separate namespaces per environment (dev, staging, production) or per team
- Apply resource quotas per namespace to prevent one team from consuming all cluster resources
- Use network policies to restrict cross-namespace communication
- Apply RBAC at the namespace level -- teams get admin on their namespace, read-only on others

---

## Networking Patterns

### VPC Architecture

- **Public subnets** -- For resources that need direct internet access (load balancers, bastion hosts, NAT gateways)
- **Private subnets** -- For application servers, databases, internal services. No direct internet access. Outbound traffic via NAT gateway.
- **Data subnets** -- For databases and persistent storage. Most restrictive access. No internet access.
- Spread subnets across multiple availability zones for high availability

### Security Groups and Network Policies

- Default deny: no traffic allowed unless explicitly permitted
- Allow only the minimum required ports and source ranges
- Use security group references (not CIDR blocks) between internal services
- Log denied traffic for security monitoring
- Review security group rules regularly -- remove unused rules

### Load Balancers

- **Application Load Balancer (L7)** -- HTTP/HTTPS routing, path-based routing, host-based routing, SSL termination. Use for web applications and APIs.
- **Network Load Balancer (L4)** -- TCP/UDP routing, static IP, high throughput, low latency. Use for non-HTTP protocols, high-performance services.
- Configure health checks on the load balancer -- unhealthy targets are automatically removed from rotation
- Enable access logging for auditing and debugging

### DNS Management

- Use infrastructure-as-code for DNS records -- no manual DNS changes
- Set appropriate TTLs: low (60s) for records that change during deployments, higher (300s+) for stable records
- Use aliases/CNAMEs for service endpoints -- do not hardcode IP addresses
- Implement DNS-based failover for multi-region deployments

---

## Environment Parity

### Dev/Staging/Production Consistency

- All environments use the same deployment mechanism (same CI/CD pipeline, same infrastructure-as-code)
- Same operating system, runtime versions, and dependency versions across environments
- Same network topology (subnets, security groups) -- scaled down for cost but structurally identical
- Same monitoring and alerting configuration -- catch monitoring gaps before production

### What Can Differ

- **Scale** -- Fewer instances, smaller instance types, reduced replicas in non-production
- **Data** -- Anonymized/synthetic data in non-production, never copy production PII
- **External integrations** -- Sandbox endpoints for payment processors, email services, etc.
- **Access controls** -- Broader access in dev, more restrictive in production

### Infrastructure Drift Detection

- Run `terraform plan` on a schedule (daily) against all environments -- alert on unplanned differences
- Compare environment configurations programmatically -- flag any structural divergence
- Treat drift as a bug -- investigate and resolve, do not accept as normal
- After manual emergency changes, reconcile back to code within 24 hours

---

## Cost Optimization

### Right-Sizing

- Analyze actual resource utilization (CPU, memory, network) over a representative period (at least 2 weeks)
- Downsize instances where utilization is consistently below 30%
- Upsize instances where utilization regularly exceeds 80% (performance risk)
- Use cloud provider's right-sizing recommendations as a starting point, not a final answer

### Spot and Preemptible Instances

- Use for stateless, fault-tolerant workloads: batch processing, CI runners, development environments
- Never use for stateful services or databases
- Implement graceful shutdown handling -- spot instances can be reclaimed with 2-minute warning
- Mix spot with on-demand for critical workloads: spot for burst capacity, on-demand for baseline

### Reserved Capacity

- Commit to reserved instances for stable, predictable workloads (databases, baseline application servers)
- Analyze usage patterns before committing -- reserved instance mistakes are expensive
- Use savings plans over reserved instances when flexibility is needed across instance families
- Review reservations quarterly -- adjust as workload patterns change

### Cleanup Automation

- Automatically identify and flag unused resources: unattached volumes, idle load balancers, stale snapshots, orphaned DNS records
- Auto-terminate development resources outside business hours
- Set expiration tags on temporary resources (experiments, spikes, demos)
- Budget alerts at 80% and 100% of expected spend per team/project

---

## Multi-Cloud and Hybrid Strategies

### When Multi-Cloud Makes Sense

- Regulatory requirements mandate data residency in regions served by different providers
- Acquisition brings workloads on a different provider -- migration is not immediately feasible
- Specific services are best-of-breed on different providers (e.g., ML on GCP, enterprise integration on Azure)
- Vendor risk mitigation is a board-level requirement

### When Multi-Cloud Does Not Make Sense

- "Avoiding vendor lock-in" without a concrete scenario where switching is required
- The team is not large enough to maintain expertise across multiple providers
- The added complexity outweighs the theoretical benefit

### Hybrid Patterns

- **Consistent tooling** -- Use Terraform or Pulumi across all providers; do not use provider-specific IaC tools for each
- **Abstraction at the right level** -- Abstract networking and compute; do not abstract managed services (that defeats the purpose of using them)
- **Centralized observability** -- Aggregate metrics, logs, and traces from all providers into a single observability platform
- **Identity federation** -- Single identity provider (IdP) across all environments; do not maintain separate user directories

---

## Infrastructure Anti-Patterns

- **Snowflake servers** -- Servers configured manually with undocumented changes. Every server should be reproducible from code. If a server cannot be destroyed and recreated from code, it is a snowflake.
- **Manual configuration** -- SSH-ing into servers to edit configuration files. All configuration changes must go through version control and automated deployment.
- **No state management** -- Running Terraform without remote state and locking. Concurrent runs corrupt state. Lost state means lost track of managed resources.
- **Pet servers** -- Servers with names, personalities, and institutional knowledge. Servers are cattle, not pets. They should be interchangeable and disposable.
- **Hardcoded values** -- IP addresses, account IDs, region names hardcoded in infrastructure code. Use variables and data sources.
- **No resource tagging** -- Resources without ownership, environment, or cost-center tags. Tagging is mandatory for cost attribution, access control, and lifecycle management.
- **Ignoring provider limits** -- Not tracking API rate limits, service quotas, or resource limits. Hit a limit during an incident and the recovery is blocked.
- **Over-engineering for scale** -- Building for 10x current load from day one. Right-size for current needs with a clear scaling plan. Premature scaling wastes money and adds complexity.
