# VirtuX Pro API & Automation Guide

## Overview

VirtuX Pro exposes a REST API and a command-line interface (CLI) for programmatic
VM lifecycle management. This guide covers authentication, API endpoints with curl
examples, CLI scripting patterns, Infrastructure-as-Code integration (Terraform,
Ansible), and CI/CD pipeline integration.

## Authentication

### API Token Generation

1. Log into the VirtuX Pro web console at `https://<host>:8443`
2. Navigate to **Settings → API Tokens**
3. Click **Generate Token**, provide a label (e.g., `jenkins-ci`), and select the
   appropriate scope:
   - `vm:read` — list and inspect VMs
   - `vm:write` — create, modify, and delete VMs
   - `vm:admin` — full VM control including snapshots and migrations
   - `admin:read` — read-only access to cluster configuration
   - `admin:write` — full administrative access
4. Copy the generated token. It appears only once.

### Token Usage

All API requests require the token in an `Authorization` header:

```bash
curl -H "Authorization: Bearer <TOKEN>" https://<host>:8443/api/v1/vms
```

Tokens expire after 90 days by default. Renew before expiry to avoid automation
failures. For CI/CD pipelines, store the token as a secret in your pipeline
configuration (GitHub Secrets, GitLab CI Variables, Jenkins Credentials).

## REST API Reference

### Base URL

```
https://<virtux-host>:8443/api/v1
```

All endpoints return JSON. Responses include standard HTTP status codes:

| Code | Meaning |
|:----:|:--------|
| 200 | Success — GET or successful operation |
| 201 | Created — VM or resource created successfully |
| 400 | Bad Request — Invalid parameters |
| 401 | Unauthorized — Missing or invalid token |
| 404 | Not Found — VM or resource does not exist |
| 409 | Conflict — Operation conflicts with current VM state |
| 500 | Internal Server Error |

### Virtual Machines

**List All VMs:**

```bash
curl -X GET "https://virtux.internal:8443/api/v1/vms" \
  -H "Authorization: Bearer $VIRTUX_TOKEN"
```

Response:
```json
{
  "vms": [
    {
      "id": "vm-abc123",
      "name": "web-server-01",
      "state": "running",
      "cpu": 4,
      "memory_mb": 8192,
      "disk_gb": 50,
      "os": "Ubuntu 22.04",
      "ip_address": "192.168.122.45",
      "host": "node-01",
      "created": "2025-06-01T10:30:00Z"
    }
  ],
  "total": 1
}
```

**Get a Specific VM:**

```bash
curl -X GET "https://virtux.internal:8443/api/v1/vms/vm-abc123" \
  -H "Authorization: Bearer $VIRTUX_TOKEN"
```

**Create a VM:**

```bash
curl -X POST "https://virtux.internal:8443/api/v1/vms" \
  -H "Authorization: Bearer $VIRTUX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "web-server-02",
    "cpu": 4,
    "memory_mb": 8192,
    "disk_gb": 50,
    "os": "ubuntu-22.04",
    "network": "bridge=virbr0",
    "start": true
  }'
```

Required fields: `name`, `cpu`, `memory_mb`, `disk_gb`, `os`.
Optional fields: `network` (default: NAT), `start` (default: false), `storage_pool`
(default: `default`), `cloud_init` (path to cloud-init YAML), `tags` (array of strings).

**Delete a VM:**

```bash
curl -X DELETE "https://virtux.internal:8443/api/v1/vms/vm-abc123" \
  -H "Authorization: Bearer $VIRTUX_TOKEN"
```

Add `?force=true` to forcefully power off and delete without confirmation.

**VM Power Operations:**

```bash
# Start
curl -X POST "https://virtux.internal:8443/api/v1/vms/vm-abc123/start" \
  -H "Authorization: Bearer $VIRTUX_TOKEN"

# Graceful shutdown (ACPI signal)
curl -X POST "https://virtux.internal:8443/api/v1/vms/vm-abc123/shutdown" \
  -H "Authorization: Bearer $VIRTUX_TOKEN"

# Force power off
curl -X POST "https://virtux.internal:8443/api/v1/vms/vm-abc123/poweroff" \
  -H "Authorization: Bearer $VIRTUX_TOKEN"

# Reboot
curl -X POST "https://virtux.internal:8443/api/v1/vms/vm-abc123/reboot" \
  -H "Authorization: Bearer $VIRTUX_TOKEN"
```

**VM Snapshots:**

```bash
# Create snapshot
curl -X POST "https://virtux.internal:8443/api/v1/vms/vm-abc123/snapshots" \
  -H "Authorization: Bearer $VIRTUX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "pre-upgrade-20250601", "description": "Before kernel upgrade"}'

# List snapshots
curl -X GET "https://virtux.internal:8443/api/v1/vms/vm-abc123/snapshots" \
  -H "Authorization: Bearer $VIRTUX_TOKEN"

# Restore snapshot
curl -X POST "https://virtux.internal:8443/api/v1/vms/vm-abc123/snapshots/pre-upgrade-20250601/restore" \
  -H "Authorization: Bearer $VIRTUX_TOKEN"
```

**VM Migration:**

```bash
curl -X POST "https://virtux.internal:8443/api/v1/vms/vm-abc123/migrate" \
  -H "Authorization: Bearer $VIRTUX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"target_host": "node-02", "live": true}'
```

### Hosts and Clusters

**List Hosts:**

```bash
curl -X GET "https://virtux.internal:8443/api/v1/hosts" \
  -H "Authorization: Bearer $VIRTUX_TOKEN"
```

**Host Resource Usage:**

```bash
curl -X GET "https://virtux.internal:8443/api/v1/hosts/node-01/resources" \
  -H "Authorization: Bearer $VIRTUX_TOKEN"
```

Response:
```json
{
  "host": "node-01",
  "cpu": {"total": 16, "used": 8, "available": 8, "percent": 50.0},
  "memory_mb": {"total": 65536, "used": 32768, "available": 32768},
  "disk_gb": {"total": 500, "used": 200, "available": 300},
  "running_vms": 5
}
```

### Storage Pools

**List Storage Pools:**

```bash
curl -X GET "https://virtux.internal:8443/api/v1/storage" \
  -H "Authorization: Bearer $VIRTUX_TOKEN"
```

**Create Storage Pool:**

```bash
curl -X POST "https://virtux.internal:8443/api/v1/storage" \
  -H "Authorization: Bearer $VIRTUX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "nvme-pool", "path": "/mnt/nvme/virtux", "type": "dir"}'
```

---

## CLI Usage

### Installation

```bash
pip install virtux-cli
```

Authenticate:

```bash
virtux login --url https://virtux.internal:8443 --token $VIRTUX_TOKEN
# Credentials stored in ~/.virtux/config (permissions: 0600)
```

### VM Management Commands

```bash
# List VMs with filtering
virtux vm list
virtux vm list --state running --tag production

# Create VM
virtux vm create --name web-01 --cpu 4 --memory 8192 --disk 50 \
  --os ubuntu-22.04 --network bridge=virbr0 --start

# VM details (JSON output available)
virtux vm show vm-abc123
virtux vm show vm-abc123 --json

# VM power control
virtux vm start vm-abc123
virtux vm shutdown vm-abc123
virtux vm reboot vm-abc123

# VM console (web-based, opens browser)
virtux vm console vm-abc123

# Delete VM
virtux vm delete vm-abc123
virtux vm delete vm-abc123 --force   # Skip confirmation
```

### Snapshot Management

```bash
virtux snapshot create vm-abc123 --name pre-patch
virtux snapshot list vm-abc123
virtux snapshot restore vm-abc123 --name pre-patch
virtux snapshot delete vm-abc123 --name old-snapshot
```

### Host and Cluster Management

```bash
virtux host list
virtux host show node-01
virtux host resources node-01
virtux cluster status
```

---

## Automation Examples

### Bulk VM Deployment (Shell)

```bash
#!/bin/bash
# deploy-web-cluster.sh — Deploy N identical web servers

VIRTUX_URL="https://virtux.internal:8443"
TOKEN="${VIRTUX_TOKEN:?Set VIRTUX_TOKEN environment variable}"
COUNT=${1:-3}
PREFIX=${2:-web}

for i in $(seq 1 $COUNT); do
  VM_NAME="${PREFIX}-$(printf '%02d' $i)"
  echo "Creating $VM_NAME..."

  curl -s -X POST "$VIRTUX_URL/api/v1/vms" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"name\": \"$VM_NAME\",
      \"cpu\": 2,
      \"memory_mb\": 4096,
      \"disk_gb\": 30,
      \"os\": \"ubuntu-22.04\",
      \"network\": \"bridge=virbr0\",
      \"tags\": [\"$PREFIX\", \"auto-deployed\"],
      \"start\": true
    }" | jq -r '.id + " " + .name'

  # Short delay between creations to avoid API rate limiting
  sleep 2
done

echo "Deployment complete. $(virtux vm list --tag auto-deployed | wc -l) VMs running."
```

### Python VM Deployment Script

```python
#!/usr/bin/env python3
"""deploy-vm.py — Deploy and configure VMs using the VirtuX Pro REST API."""

import os
import sys
import time
import requests
import json

VIRTUX_URL = os.environ.get("VIRTUX_URL", "https://virtux.internal:8443")
VIRTUX_TOKEN = os.environ.get("VIRTUX_TOKEN")

if not VIRTUX_TOKEN:
    print("Error: VIRTUX_TOKEN environment variable not set", file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {VIRTUX_TOKEN}",
    "Content-Type": "application/json",
}

def create_vm(name, cpu, memory_mb, disk_gb, os_name, network="bridge=virbr0", start=True):
    """Create a virtual machine and wait for it to be ready."""
    payload = {
        "name": name,
        "cpu": cpu,
        "memory_mb": memory_mb,
        "disk_gb": disk_gb,
        "os": os_name,
        "network": network,
        "start": start,
    }

    resp = requests.post(
        f"{VIRTUX_URL}/api/v1/vms",
        headers=HEADERS,
        json=payload,
        verify=True,
    )

    if resp.status_code != 201:
        print(f"Failed to create VM: {resp.status_code} — {resp.text}")
        return None

    vm = resp.json()
    vm_id = vm["id"]
    print(f"Created VM: {vm_id} ({name})")

    # Wait for VM to reach 'running' state
    for _ in range(30):  # 60-second timeout
        status = get_vm_status(vm_id)
        if status == "running":
            print(f"  VM {name} is running")
            return vm_id
        time.sleep(2)

    print(f"  Warning: VM {name} did not start within timeout")
    return vm_id


def get_vm_status(vm_id):
    """Get the current state of a VM."""
    resp = requests.get(
        f"{VIRTUX_URL}/api/v1/vms/{vm_id}",
        headers=HEADERS,
        verify=True,
    )
    if resp.status_code == 200:
        return resp.json()["state"]
    return "unknown"


def get_vm_ip(vm_id):
    """Retrieve the IP address of a running VM."""
    resp = requests.get(
        f"{VIRTUX_URL}/api/v1/vms/{vm_id}",
        headers=HEADERS,
        verify=True,
    )
    if resp.status_code == 200:
        return resp.json().get("ip_address")
    return None


if __name__ == "__main__":
    # Example: deploy 3 web servers
    configs = [
        {"name": "web-01", "cpu": 2, "memory_mb": 4096, "disk_gb": 30, "os": "ubuntu-22.04"},
        {"name": "web-02", "cpu": 2, "memory_mb": 4096, "disk_gb": 30, "os": "ubuntu-22.04"},
        {"name": "db-01",  "cpu": 4, "memory_mb": 8192, "disk_gb": 100, "os": "ubuntu-22.04"},
    ]

    for cfg in configs:
        vm_id = create_vm(**cfg)
        if vm_id:
            ip = get_vm_ip(vm_id)
            print(f"  {cfg['name']} → IP: {ip}\n")
```

### Cloud-Init Automation

VirtuX Pro supports cloud-init for automated VM provisioning:

```bash
# cloud-init.yaml
#cloud-config
hostname: web-server-01
fqdn: web-server-01.example.com
users:
  - name: deploy
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh_authorized_keys:
      - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ...
packages:
  - nginx
  - python3
  - git
write_files:
  - path: /etc/nginx/sites-available/default
    content: |
      server {
        listen 80;
        server_name _;
        location / { return 200 "Hello from web-server-01\n"; }
      }
runcmd:
  - systemctl enable --now nginx
  - echo "Provisioning complete" >> /var/log/cloud-init.log
```

Deploy with cloud-init:

```bash
virtux vm create --name web-01 --cpu 2 --memory 4096 --disk 30 \
  --os ubuntu-22.04 --cloud-init cloud-init.yaml --start
```

---

## Infrastructure as Code

### Terraform Provider

```hcl
# main.tf
terraform {
  required_providers {
    virtux = {
      source  = "virtuxpro/virtux"
      version = "~> 1.2.0"
    }
  }
}

provider "virtux" {
  url   = "https://virtux.internal:8443"
  token = var.virtux_token
}

resource "virtux_vm" "web_server" {
  count      = 3
  name       = "web-${format("%02d", count.index + 1)}"
  cpu        = 2
  memory_mb  = 4096
  disk_gb    = 30
  os         = "ubuntu-22.04"
  network    = "bridge=virbr0"
  cloud_init = file("${path.module}/cloud-init.yaml")
  tags       = ["web", "terraform"]

  lifecycle {
    ignore_changes = [cloud_init]  # Don't recreate on cloud-init changes
  }
}

output "vm_ips" {
  value = virtux_vm.web_server[*].ip_address
}
```

```bash
terraform init
terraform plan
terraform apply -auto-approve
```

### Ansible Integration

```yaml
# inventory/virtux.yml
plugin: virtuxpro.virtux.virtux_inventory
url: "https://virtux.internal:8443"
token: "{{ lookup('env', 'VIRTUX_TOKEN') }}"
groups:
  web: "'web' in tags"
  database: "'db' in tags"
```

```yaml
# playbooks/deploy-web.yml
- hosts: web
  become: yes
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Start nginx
      systemd:
        name: nginx
        state: started
        enabled: yes

    - name: Deploy application
      copy:
        src: ../app/
        dest: /var/www/html/
```

```bash
ansible-playbook -i inventory/virtux.yml playbooks/deploy-web.yml
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/deploy-vm.yml
name: Deploy Test VM
on:
  pull_request:
    paths:
      - 'src/**'

jobs:
  deploy-test-vm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy test VM
        env:
          VIRTUX_TOKEN: ${{ secrets.VIRTUX_TOKEN }}
        run: |
          curl -X POST "https://virtux.internal:8443/api/v1/vms" \
            -H "Authorization: Bearer $VIRTUX_TOKEN" \
            -H "Content-Type: application/json" \
            -d '{
              "name": "pr-test-${{ github.event.pull_request.number }}",
              "cpu": 2, "memory_mb": 4096, "disk_gb": 20,
              "os": "ubuntu-22.04", "start": true,
              "tags": ["ci", "pr-${{ github.event.pull_request.number }}"]
            }'

      - name: Cleanup test VM
        if: always()
        env:
          VIRTUX_TOKEN: ${{ secrets.VIRTUX_TOKEN }}
        run: |
          VM_ID=$(curl -s "https://virtux.internal:8443/api/v1/vms?tag=pr-${{ github.event.pull_request.number }}" \
            -H "Authorization: Bearer $VIRTUX_TOKEN" | jq -r '.vms[0].id')
          if [ -n "$VM_ID" ]; then
            curl -X DELETE "https://virtux.internal:8443/api/v1/vms/$VM_ID?force=true" \
              -H "Authorization: Bearer $VIRTUX_TOKEN"
          fi
```

---

## Rate Limiting

The API enforces the following limits per token:

| Endpoint | Limit |
|:---------|:------|
| `GET /api/v1/*` | 300 requests/minute |
| `POST /api/v1/vms` | 30 requests/minute |
| `DELETE /api/v1/vms/*` | 30 requests/minute |
| All other mutations | 60 requests/minute |

Rate limit headers are included in every response:
```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 27
X-RateLimit-Reset: 1717200000
```

Automation scripts should check `X-RateLimit-Remaining` and back off with
exponential delay if approaching the limit.

---

## API Documentation

Full OpenAPI 3.1 specification: `https://virtux.internal:8443/api/v1/openapi.json`

Interactive Swagger UI: `https://virtux.internal:8443/api/v1/docs`