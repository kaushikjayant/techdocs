# API and Automation

## Overview
VirtuX Pro provides robust automation capabilities through its REST API and Command Line Interface (CLI), allowing users to efficiently deploy, configure, and manage virtual machines (VMs). This guide details how to automate VM deployments using these tools.

---

## 1. REST API

### 1.1 API Authentication
To interact with VirtuX Pro's API, you need to authenticate using an API token.

#### Steps:
1. Obtain an API token from the VirtuX Pro web interface.
2. Use the token in the authorization header for API requests.

Example:
```bash
curl -X GET "https://api.virtuxpro.com/v1/vms" \
     -H "Authorization: Bearer YOUR_API_TOKEN"
```

### 1.2 Deploying a Virtual Machine
You can deploy a VM using the following API request:
```bash
curl -X POST "https://api.virtuxpro.com/v1/vms" \
     -H "Authorization: Bearer YOUR_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "MyVM",
       "cpu": 4,
       "memory": 8192,
       "disk": 50,
       "os": "Ubuntu 22.04"
     }'
```

### 1.3 Managing Virtual Machines
- **Start VM**:
  ```bash
  curl -X POST "https://api.virtuxpro.com/v1/vms/{vm_id}/start" \
       -H "Authorization: Bearer YOUR_API_TOKEN"
  ```
- **Stop VM**:
  ```bash
  curl -X POST "https://api.virtuxpro.com/v1/vms/{vm_id}/stop" \
       -H "Authorization: Bearer YOUR_API_TOKEN"
  ```
- **Delete VM**:
  ```bash
  curl -X DELETE "https://api.virtuxpro.com/v1/vms/{vm_id}" \
       -H "Authorization: Bearer YOUR_API_TOKEN"
  ```

---

## 2. Command Line Interface (CLI)
VirtuX Pro provides a CLI for quick and scriptable interactions.

### 2.1 Installation
Install the VirtuX CLI using:
```bash
pip install virtux-cli
```

### 2.2 CLI Authentication
Authenticate using your API token:
```bash
virtux login --token YOUR_API_TOKEN
```

### 2.3 Deploying a VM via CLI
```bash
virtux vm create --name MyVM --cpu 4 --memory 8192 --disk 50 --os "Ubuntu 22.04"
```

### 2.4 Managing VMs via CLI
- **List VMs**:
  ```bash
  virtux vm list
  ```
- **Start a VM**:
  ```bash
  virtux vm start --id vm_id
  ```
- **Stop a VM**:
  ```bash
  virtux vm stop --id vm_id
  ```
- **Delete a VM**:
  ```bash
  virtux vm delete --id vm_id
  ```

---

## 3. Automating Deployments
### 3.1 Using Scripts
You can use shell scripts to automate bulk deployments. Example:
```bash
#!/bin/bash
for i in {1..5}
do
  virtux vm create --name "VM-$i" --cpu 2 --memory 4096 --disk 20 --os "Ubuntu 22.04"
done
```
Save this as `deploy_vms.sh` and run:
```bash
chmod +x deploy_vms.sh
./deploy_vms.sh
```

### 3.2 Using Infrastructure as Code (IaC)
VirtuX Pro supports integration with Terraform and Ansible.

Example Terraform script:
```hcl
provider "virtux" {
  token = "YOUR_API_TOKEN"
}

resource "virtux_vm" "example" {
  name   = "MyTerraformVM"
  cpu    = 2
  memory = 4096
  disk   = 30
  os     = "Ubuntu 22.04"
}
```
Run:
```bash
terraform init
terraform apply
```

---

## Conclusion
With VirtuX Pro's REST API and CLI, users can efficiently automate VM management, integrate with DevOps tools, and optimize their cloud infrastructure. For further details, refer to the official [VirtuX Pro API Documentation](https://api.virtuxpro.com/docs).
