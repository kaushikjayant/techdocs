

---

# Enterprise Application Access (EAA)

## Table of contents

1. [Overview & Purpose](#overview--purpose)
2. [Quick Start (Minimal viable deployment)](#quick-start-minimal-viable-deployment)
3. [Core Architecture & Components](#core-architecture--components)
4. [Supported Application Types & Use Cases](#supported-application-types--use-cases)
5. [Prerequisites & Planning Checklist](#prerequisites--planning-checklist)
6. [Full Installation – Management Plane (on-prem/self-hosted) — exhaustive](#full-installation--management-plane-on-premself-hosted----exhaustive)
7. [Full Installation – Enterprise Connector (VM/Container/Cloud) — exhaustive](#full-installation--enterprise-connector-vmcontainercloud----exhaustive)
8. [Full Installation – Data Plane & Gateway configuration (exhaustive)](#full-installation--data-plane--gateway-configuration-exhaustive)
9. [Client Installation & Configuration (Windows/macOS/Linux) — exhaustive](#client-installation--configuration-windowsmacoslinux----exhaustive)
10. [Application Onboarding: Web / SaaS / SSH / RDP / Custom TCP/UDP](#application-onboarding-web--saas--ssh--rdp--custom-tcpudp)
11. [Access Policies & Device Posture — examples & templates](#access-policies--device-posture----examples--templates)
12. [TLS / Certificate Management & DNS setup](#tls--certificate-management--dns-setup)
13. [Firewall & Network Rules (explicit)](#firewall--network-rules-explicit)
14. [High Availability, Scaling & Capacity Planning](#high-availability-scaling--capacity-planning)
15. [Logging, Monitoring, Metrics & SIEM Integration (schema & examples)](#logging-monitoring-metrics--siem-integration-schema--examples)
16. [Automation: REST API examples & CLI scripts (practical snippets)](#automation-rest-api-examples--cli-scripts-practical-snippets)
17. [Backup, Restore & Disaster Recovery Procedures](#backup-restore--disaster-recovery-procedures)
18. [Troubleshooting — common scenarios, diagnostics & fixes](#troubleshooting----common-scenarios-diagnostics--fixes)
19. [Security Hardening Checklist](#security-hardening-checklist)
20. [Operational Best Practices & Runbook Ideas](#operational-best-practices--runbook-ideas)
21. [Release Notes / Change Log (how to maintain)](#release-notes--change-log-how-to-maintain)
22. [FAQ](#faq)
23. [Appendices & Reference Snippets](#appendices--reference-snippets)
24. [Glossary](#glossary)

---

# Overview & Purpose

Enterprise Application Access (EAA) provides secure, application-level access to internal enterprise resources using a Zero-Trust approach. EAA grants least-privilege access to applications (web and non-web) without exposing the internal network through inbound firewall rules or network-level VPN tunnels.

Goals:

* Protect internal apps while enabling remote/hybrid work.
* Enforce identity + device posture + context before access.
* Provide audit trails and integration points for automation and SIEM.
* Be deployable in on-premises, cloud, and hybrid models.

---

# Quick Start (Minimal viable deployment)

This section gives the fastest path to a working PoC (single site, single connector, one web app).

1. **Provision a single connector VM** (Linux VM, 2 vCPU, 4 GB RAM, 20 GB) in the network containing the application.
2. **Open outbound TLS (TCP/443)** from the connector host to the management/data plane IPs or FQDNs.
3. **Register connector** with management plane (copy registration token/command from manager → run on connector).
4. **Create identity integration**: configure an IdP (SAML/OIDC) or connect to LDAP/AD; test authentication.
5. **Publish a web app**: add internal hostname/IP and port 80/443; assign connector; test browser login and application access.
6. **Install client** (only if testing non-web app): install lightweight client on test device and test RDP/SSH connection through connector.

Result: working proof of concept for internal web app with authenticated access and no inbound ports.

---

# Core Architecture & Components

* **Management Plane** (control): UI/API to configure directories, apps, policies, connectors, certificates, logs and RBAC. Can be cloud-hosted or self-hosted.
* **Data Plane / Gateway** (optional intermediate): proxies traffic, applies runtime policies, handles session termination/translation and protocol adaptation. May be combined with management or be a separate cluster.
* **Enterprise Connector**: lightweight appliance inside private network that initiates outbound TLS tunnels to the data plane and routes requests to internal hosts.
* **EAA Client (Endpoint Agent)**: optional lightweight software on user devices (Windows/macOS/Linux) to enable TCP/UDP and DNS interception / loopback-based access to client-based apps.
* **IdP / Directory**: Active Directory, LDAP, SAML/OIDC providers for authentication and group membership.
* **Logging & Observability**: central log ingestion (ELK, Splunk, Graylog, SIEM) for access and audit logs.

---

# Supported Application Types & Use Cases

* Web-based (HTTP/HTTPS) portals, internal dashboards, admin consoles.
* SaaS access via SAML/OIDC federation (SSO).
* Non-web (RDP, SSH, VNC, database ports, proprietary TCP/UDP).
* Legacy thick-clients requiring specific ports or IPs.
* Bookmark / portal links for convenience.

Key use cases: remote workers, contractors, third-party vendors, secure legacy app access, Zero-Trust migrations away from VPNs.

---

# Prerequisites & Planning Checklist

Before starting, collect:

* Service account for management (create admin user; enable MFA).
* IdP/LDAP credentials and read access for user/group sync.
* DNS administration access for external CNAME/A records.
* TLS certificates (public, private key, intermediates) if using custom domains.
* Network information: CIDR ranges, internal hostnames, NAT/Gateway details.
* VM/Container hosting capability (hypervisor, cloud subscription, container runtime).
* Storage for logs/backups and access to your SIEM/monitoring stack.

Recommended planning steps:

* Identify scoping: PoC site vs production multi-site.
* Name conventions for apps/connectors/policies.
* RBAC model for admin users (least privilege).
* Compliance requirements for logging retention & encryption.

---

# Full Installation – Management Plane (on-prem/self-hosted) — exhaustive

> Note: If you are using a vendor-hosted management service, these steps are optional; they describe how to self-host a management plane.

## Architecture choices for self-hosting

* Single-node for PoC (not recommended for production)
* Multi-node HA cluster behind a load-balancer for production
* Database backend (PostgreSQL recommended), object storage for backups/logs (S3 compatible), TLS termination at load balancer.

## System requirements (per management node)

* CPU: 4 vCPU (8 recommended)
* RAM: 16 GB (32 recommended for production)
* Disk: 200 GB SSD (separate volumes for OS / DB / logs)
* OS: Linux (Ubuntu LTS 22.04 / RHEL 8+ recommended)
* Java / runtime: as required by the chosen management software stack
* Database: PostgreSQL ≥ 12 (clustered for production)
* Reverse proxy: Nginx or HAProxy for TLS termination & routing

## Step-by-step (example on Ubuntu 22.04)

1. Provision server(s), configure static IP and FQDN (e.g., `eaa-mgmt.example.com`).
2. Install updates and basic packages:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y nginx postgresql postgresql-contrib certbot
```

3. Configure PostgreSQL (create user/database):

```bash
sudo -u postgres psql -c "CREATE ROLE eaa WITH LOGIN PASSWORD 'strongpassword';"
sudo -u postgres psql -c "CREATE DATABASE eaa_db OWNER eaa;"
```

4. Install management application (example generic package):

```bash
# hypothetical package install
sudo dpkg -i eaa-mgmt-server_1.0.0_amd64.deb
```

5. Configure management service to point to DB and object storage; set environment variables or config file (`/etc/eaa/config.yml`).
6. Configure Nginx reverse proxy with TLS (see TLS section).
7. Start and enable service:

```bash
sudo systemctl enable --now eaa-mgmt
sudo systemctl status eaa-mgmt
```

8. Harden OS: disable unused services, configure fail2ban, set up logging rotation and monitoring.

## Management high-availability

* Use at least 3 management nodes in production behind load balancer.
* Use a clustered RDBMS (Postgres streaming replication or managed DB).
* Store configs in version control and use configuration management (Ansible/Terraform).

---

# Full Installation – Enterprise Connector (VM/Container/Cloud) — exhaustive

The connector is the on-network bridge; we’ll include VM, container, and cloud instance deployments plus advanced configuration and hardening.

## System requirements (connector)

* CPU: 2 vCPU (4 recommended for heavy use)
* RAM: 4 GB (8 recommended)
* Disk: 20–40 GB
* Network: outbound HTTPS (443) allowed; DNS resolvable for internal hosts
* OS: Linux (Ubuntu LTS, RHEL/CentOS, or minimal container base)

## Deployment options and steps

### A. VM (bare-metal / hypervisor)

1. Download connector VM image/OVA and import to your hypervisor.
2. Assign CPU/RAM/disk as above; configure network (DHCP or static IP).
3. Boot and log into console (default credentials for first boot).
4. Run initial configuration wizard:

   * set hostname, timezone
   * configure NTP, DNS
   * register connector with management plane using registration token/URL:

```bash
sudo /opt/connector/bin/register --token <REG_TOKEN> --url https://eaa-mgmt.example.com
```

5. Confirm connector shows as healthy in management UI.

### B. Containerized (Docker/Podman)

1. Pull image and run:

```bash
docker pull registry.example.com/eaa/connector:latest
docker run -d --name eaa-connector \
  --restart unless-stopped \
  -e EAA_REGISTRATION_TOKEN="<REG_TOKEN>" \
  -e EAA_MGMT_URL="https://eaa-mgmt.example.com" \
  -v /var/log/eaa:/var/log/eaa \
  registry.example.com/eaa/connector:latest
```

2. Expose only necessary host volumes; avoid exposing host network unless needed.
3. Persist configuration in mounted volume to survive container reboots.
4. Monitor container logs:

```bash
docker logs -f eaa-connector
```

### C. Cloud (AWS EC2 / Azure VM / GCP)

* Use prebuilt AMI/image if provided, or install connector package on a base Linux image.
* When on cloud, attach IAM role or managed identity if connector needs to access object storage for logs.
* Use private subnets and NAT gateway to permit outbound TLS only (connector should not have public IP).

## Connector advanced configuration

* **Connector Pools**: assign connectors to pools by data-center/region for locality and failover.
* **Health Probes**: configure management probe ports and health-checking intervals.
* **Logging**: set logging levels (info/debug), configure central log shipping (Fluentd/Filebeat).
* **Metrics**: expose Prometheus metrics endpoint for scraping.
* **High-Availability**: deploy at least two connectors per site to support rolling upgrades and failover.

## Connector Hardening checklist

* Run as non-root process where possible.
* Limit outbound destinations to management/data plane addresses.
* Enable automatic updates or orchestrate rolling upgrades.
* Configure local firewall (iptables/nftables) to restrict inbound ports (most connectors require only local management).
* Use monitoring/alerting: disk, CPU, memory, connection counts.

---

# Full Installation – Data Plane & Gateway configuration (exhaustive)

If you host your own data plane/gateway cluster (instead of a vendor cloud), follow these steps:

## Data plane cluster (example Kubernetes deployment)

1. Provision a Kubernetes cluster (EKS/GKE/AKS or on-prem K8s).
2. Deploy gateway pods (stateless) behind an internal/edge load balancer.
3. Configure TLS certificates and key rotation using cert-manager.
4. Configure routing rules for connectors; create virtual services / ingress rules.
5. Set up persistent Redis/Cache if gateways require session state (prefer external managed caches).
6. Scale gateway replicas based on expected connections (see capacity planning).

## Gateway configuration items

* Worker pool sizing (socket concurrency)
* TLS cipher suite configuration (modern, FIPS if required)
* Session timeout defaults and max session lifetimes
* Rate-limiting and DoS protection policies
* Authentication adapter configuration to forward tokens/assertions to connector

---

# Client Installation & Configuration (Windows/macOS/Linux) — exhaustive

## What the client does

* Intercepts DNS/hosts for configured internal hostnames (loopback)
* Opens local loopback interface for intercepted hostnames
* Establishes TLS/WebSocket tunnel to data plane, with mutual auth
* Routes local traffic to the connector via tunnel

## Windows installation (detailed)

1. Download MSI installer (signed).
2. Run as Administrator:

   * Accept EULA
   * Choose default installation directory
3. After install, client runs as service `eaa-client`.
4. First launch: user is redirected to browser IdP for authentication or uses embedded browser for SSO.
5. Client caches short-lived tokens securely (per OS secure storage).
6. Test with `nslookup` against intercepted hostname and `netstat -an` to confirm local listener.

## macOS installation

1. Download signed PKG.
2. Run installer (requires admin).
3. Grant network extension / kernel extension permissions if required.
4. Authenticate via browser-based SSO flow.
5. Confirm using `lsof -i` and `scutil --dns`.

## Linux installation (Deb/RPM)

1. Install package:

```bash
sudo dpkg -i eaa-client_1.0.0_amd64.deb    # Debian/Ubuntu
sudo rpm -Uvh eaa-client-1.0.0.x86_64.rpm  # RHEL/CentOS
```

2. Start and enable service:

```bash
sudo systemctl enable --now eaa-client
sudo journalctl -u eaa-client -f
```

3. Authenticate (CLI or browser redirection) and confirm local loopback listeners.

## Client configuration options

* Auto-start on boot.
* Local DNS interception strategy:

  * Hosts file injection (simple)
  * DNS proxy / redirector (advanced)
  * TUN/TAP virtual interface (for specific protocol forwarding)
* Logging levels and diagnostic mode for troubleshooting.

---

# Application Onboarding: Web / SaaS / SSH / RDP / Custom TCP/UDP

## 1. Web App onboarding (exhaustive)

* **Minimum fields**: Name, internal hostname/IP, internal port, connector/pool, external alias (optional), authentication method (redirect to IdP), session policy.
* **Optional fields**: URL rewrite rules, header transforms, cookie rewrite, path-based routing, HTTP to HTTPS redirect, HSTS policy, compression.
* **Steps**:

  1. Create application entry in management UI or via API.
  2. Map internal host to connector (or connector pool).
  3. Configure external alias/CNAME if you want branded URL.
  4. Upload TLS cert (if using custom domain) and activate.
  5. Apply access policy (user groups/device posture).
  6. Publish and test.

### Example: path rewriting

* Rule: `/oldapp/(.*)` → `/newapp/$1` on internal host. Configure rewrite in app settings.

## 2. SaaS (SAML/OIDC)

* Configure SAML metadata on IdP with assertion consumer URL pointing to management plane SSO endpoint.
* Map SAML attributes to user properties (email, groups, displayName).
* Optionally enable SCIM for provisioning.

## 3. SSH/RDP onboarding

* For SSH:

  * Upload or reference host public key for verification (optional).
  * Choose user authorization model:

    * Passthrough (end-user credentials used against the host)
    * Jump user mapping (connector uses service account and maps to target users)
* For RDP:

  * Configure credential handling and clipboard/drive redirection policies.
  * Optionally enable login recording or session replay (if legal/allowed).
* Test using client agent and confirm session establishment.

## 4. Custom TCP/UDP

* Define protocol and port mapping.
* If UDP-based, configure session timers and NAT behaviors.
* Assign to connector pools and test under expected load patterns.

---

# Access Policies & Device Posture — examples & templates

## Policy components

* **Subject**: user or group (directory identity)
* **Resource**: application entry
* **Conditions**: device posture, location, time window, network source, MFA status
* **Action**: allow/deny, session transform (disable clipboard), logging level

## Example policy templates

### Template A — Corporate Laptop Full Access

```
If user.group == "employees" AND device.posture == "corporate-managed" THEN allow access to web-apps, ssh-apps with clipboard-disabled=false.
```

### Template B — Contractor Restricted Access

```
If user.group == "contractors" AND MFA == true THEN allow access to 'contractor-app-1' only, disallow RDP, require device.posture == "clean".
```

### Device posture examples

* `OS >= Ubuntu 20.04`
* `AV running == true`
* `FullDiskEncryption == true`
* `last_patch_days <= 30`

## Policy example JSON (for API)

```json
{
  "name": "contractor_restricted",
  "subjects": ["group:contractors"],
  "conditions": {
    "mfa_required": true,
    "device_posture": {
      "antivirus": true,
      "disk_encrypted": true
    },
    "time_windows": [
      {"start": "09:00", "end": "18:00", "tz": "UTC"}
    ]
  },
  "actions": {
    "allow": ["app:contractor-portal"],
    "deny": ["app:admin-console"]
  }
}
```

---

# TLS / Certificate Management & DNS setup

## TLS best practices

* Use strong TLS configuration (TLS1.2+ or TLS1.3 only if supported).
* Prefer ECDHE key exchange and modern ciphers.
* Enforce HSTS for web applications when appropriate.
* Regularly rotate certificates before expiration.

## Certificate storage and rotation

* Central certificate store (Vault/HashiCorp/KeyVault) integration recommended.
* Automate renewals with ACME where applicable.
* Secure private keys with strong permissions and HSM where needed.

## DNS setup

* Use CNAME to management/data plane external endpoints if you want branded URLs.
* For internal app names, maintain split-horizon DNS if needed (internal vs external resolution).
* Ensure reverse DNS and PTR records for connectors if auditing requires them.

---

# Firewall & Network Rules (explicit)

## Minimal firewall rules (connector host)

* Allow outbound:

  * TCP 443 → management/data-plane FQDNs/IP ranges (allow to required endpoints)
  * (Optional) UDP 123 → NTP servers
* Block inbound except:

  * SSH/WinRM for admin (restrict to jumpbox/specific IPs)
  * Local management ports (if required) from admin subnet only

## Example iptables (connector)

```bash
# allow outbound HTTPS
iptables -A OUTPUT -p tcp --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT
# allow NTP outbound
iptables -A OUTPUT -p udp --dport 123 -j ACCEPT
# allow loopback
iptables -A INPUT -i lo -j ACCEPT
# allow admin SSH from management network
iptables -A INPUT -p tcp -s 10.10.0.0/24 --dport 22 -j ACCEPT
# drop everything else inbound
iptables -P INPUT DROP
iptables -P FORWARD DROP
```

## Network segmentation recommendations

* Keep connectors in a management network/subnet with restricted egress to only the necessary platform endpoints.
* Use security groups / NSGs on cloud to limit traffic flows.

---

# High Availability, Scaling & Capacity Planning

## Connector scaling

* **Horizontal scaling**: add more connector instances; assign to connector pools.
* **Scale triggers**: CPU > 70% sustained, latency > threshold, connection count > threshold.
* **Rolling upgrades**: drain sessions from a connector before replacing.

## Data plane scaling

* Use stateless gateways with sticky session support if session state is needed (or externalize session store).

## Capacity planning guidelines

* Estimate concurrent sessions per connector (based on application mix).
* Keep a buffer (30–50%) for peak load.
* For RDP/SSH heavy workloads provision more CPU and memory per connector.

---

# Logging, Monitoring, Metrics & SIEM Integration (schema & examples)

## Log types

* **Access logs**: timestamp, user, app, source IP, session duration, bytes transferred.
* **Audit logs**: admin actions (create/update/delete) with user and timestamp.
* **Connector logs**: connectivity, errors, connection counts.
* **Client logs**: client errors, token refresh events.
* **System logs**: OS and service-level logs.

## Sample access log format (JSON)

```json
{
  "timestamp": "2025-12-01T12:34:56Z",
  "user": "alice@example.com",
  "user_id": "u-1234",
  "app": "internal-portal",
  "app_id": "app-5678",
  "action": "connect",
  "source_ip": "203.0.113.45",
  "connector": "conn-nyc-1",
  "duration_seconds": 312,
  "bytes_in": 123456,
  "bytes_out": 654321,
  "device_posture": {"av": true, "disk_encrypted": true}
}
```

## Metrics to monitor

* Connector uptime & restart counts
* Active sessions per connector
* Authentication failures rate
* Average auth latency (IdP)
* Errors per minute (HTTP 5xx, TLS errors)
* Log shipping success/failure

## SIEM integration

* Forward logs via syslog/Fluentd/Filebeat to central SIEM.
* Create alerts for:

  * Repeated auth failures from single IP (possible brute force)
  * Connector offline events
  * Policy changes by non-admin user

---

# Automation: REST API examples & CLI scripts (practical snippets)

## Example: Create application via REST API (curl)

```bash
API_URL="https://eaa-mgmt.example.com/api/v1"
TOKEN="eyJhbGciOi..."

curl -X POST "$API_URL/apps" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"internal-portal",
    "type":"web",
    "internal_host":"10.10.20.5",
    "internal_port":443,
    "connector_pool":"nyc-pool",
    "auth":"saml"
  }'
```

## Example: Register connector with CLI

```bash
eaa-cli connector register --url https://eaa-mgmt.example.com --token <REG_TOKEN> --name conn-nyc-1
```

## Example: Backup configuration

```bash
curl -X POST "$API_URL/admin/backup" -H "Authorization: Bearer $TOKEN" -o eaa-backup-2025-12-01.tar.gz
```

## Example: Script to add user group and assign policy (pseudo)

```bash
#!/bin/bash
TOKEN="..."
GROUP_NAME="contractors"
curl -X POST "$API_URL/groups" -H "Authorization: Bearer $TOKEN" -d "{\"name\":\"$GROUP_NAME\"}"
# assign policy
curl -X POST "$API_URL/policies" -H "Authorization: Bearer $TOKEN" -d '{"name":"contractor_policy", "..."}'
```

---

# Backup, Restore & Disaster Recovery Procedures

## Backup scope

* Management configuration (apps, policies, connectors)
* Database backups (Postgres)
* TLS private keys (secure vault)
* Logs (if retention required), or pointer to centralized log store

## Backup schedule & retention

* Daily configuration snapshot (keep 30 days)
* Weekly full DB backup (keep 90 days)
* Offsite storage for critical backups (S3/Blob with versioning)

## Restore steps (high level)

1. Restore database to new management node.
2. Restore config snapshots.
3. Re-register or re-point connectors (if management FQDN changes).
4. Validate connector health and app reachability.

## DR test checklist

* Simulate management plane failure and recover on standby node.
* Confirm connectors reconnect to new management endpoint.
* Test critical application access after failover.

---

# Troubleshooting — common scenarios, diagnostics & fixes

## Scenario 1: Connector shows offline in management UI

**Checks**

* From connector, `curl -v https://eaa-mgmt.example.com/health`
* Confirm DNS resolution and outbound 443 connectivity (`telnet eaa-mgmt.example.com 443`)
* Check connector logs (`journalctl -u eaa-connector -l`)

**Fixes**

* Open outbound firewall rules for platform IPs
* Ensure registration token not expired — re-register connector

## Scenario 2: User cannot authenticate (SSO fails)

**Checks**

* Check IdP logs for SAML assertions
* Confirm SAML metadata / entity ID match
* Ensure system times are in sync (NTP)

**Fixes**

* Reload SAML metadata; confirm attribute mapping (email, uid)
* Reconfigure time sync on management and connector nodes

## Scenario 3: Web app returns certificate error to user

**Checks**

* Confirm certificate chain on management plane (full chain present)
* Verify external alias CNAME points to correct gateway IP
* Inspect browser error (expired cert / mismatched CN)

**Fixes**

* Upload correct certificate and intermediate bundle
* Reissue CNAME or update DNS records; clear caches

## Scenario 4: Client app can’t resolve internal hostnames

**Checks**

* On client, inspect hosts override (client loopback or DNS proxy)
* Confirm app mapping exists and client policy permits the app

**Fixes**

* Restart client service, re-login, confirm app list synced
* Check management UI that app is published and assigned to user group

---

# Security Hardening Checklist

* Enforce MFA for all admin accounts and sensitive user groups.
* Use RBAC for admin tasks; separate duties between ops and security teams.
* Hardening OS images and containers; use CIS benchmarks.
* Rotate secrets and certificates on a schedule.
* Use encrypted backups and key management (HSM or Vault).
* Regularly audit logs and set SIEM alerts for anomalous activity.
* Limit connector outbound destinations; employ egress filtering.
* Encrypt internal components (DB at rest, TLS for API & internal traffic).
* Conduct periodic penetration testing and vulnerability scanning.

---

# Operational Best Practices & Runbook Ideas

* Maintain runbooks for: connector registration, emergency decommission, user lockouts, certificate renewal, and failover.
* Create a “known-good” baseline and CI tests for configuration changes (validate via API).
* Use canary deployments for app/policy updates and monitor metrics before rolling out.
* Train a small on-call team with escalation matrix and relevant contacts.

---

# Release Notes / Change Log (how to maintain)

* Keep a `CHANGELOG.md` in the docs repo capturing: date, author, change summary, impacted systems, rollback steps.
* Version policy changes and app configs as Git commits or tagged releases.
* Example changelog entry:

```
2025-12-01 - v1.4.2 - Added connector pool feature; updated policy templates; rolling upgrade instructions added - Author: jayant
```

---

# FAQ

**Q: Will this expose my internal servers to the Internet?**
A: No — connectors initiate outbound TLS only; no inbound firewall openings are required.

**Q: Can we use existing IdP (Okta/Azure/AzureAD/ADFS)?**
A: Yes — EAA integrates with SAML/OIDC and LDAP/AD for user and group sync.

**Q: Is the client required for web apps?**
A: No — browser-based access works without client. Client is required for non-web, protocol-level apps.

**Q: How to perform a hotfix/rolling update of a connector?**
A: Drain existing sessions from a connector, update the node, re-register if needed, and verify connectivity. Use connector pools so other connectors take traffic.

---

# Appendices & Reference Snippets

## Appendix A — Sample Nginx reverse proxy for management plane

```nginx
server {
  listen 443 ssl;
  server_name eaa-mgmt.example.com;

  ssl_certificate /etc/ssl/certs/eaa.crt;
  ssl_certificate_key /etc/ssl/private/eaa.key;
  ssl_protocols TLSv1.2 TLSv1.3;
  ssl_ciphers HIGH:!aNULL:!MD5;

  location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header Host $host;
  }
}
```

## Appendix B — Example Postgres backup (cron)

```bash
0 2 * * * /usr/bin/pg_dump -U eaa -F c eaa_db | gzip > /backups/eaa_db_$(date +\%F).sql.gz
```

## Appendix C — Sample connector health-check query

```bash
curl -sS --cacert /etc/ssl/certs/ca.pem https://eaa-mgmt.example.com/api/v1/connectors/health | jq
```

---

# Glossary

* **Connector** — internal agent/appliance that opens outbound connection to the platform and routes traffic to internal apps.
* **Management Plane** — UI/API used to administer the system (apps, policies, connectors, certificates).
* **Data Plane** — runtime traffic handling infrastructure which applies policies and proxies sessions.
* **Client/Agent** — endpoint software used for non-web apps to enable tunneling and DNS interception.
* **Policy** — set of rules that determines access (subjects, conditions, actions).
* **Device Posture** — security/compliance checks performed on endpoints (AV, encryption, OS version).

---
