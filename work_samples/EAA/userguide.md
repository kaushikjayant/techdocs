
---

# **Enterprise Application Access (EAA) — Comprehensive User Guide**


---

## **Table of Contents**

* [What is EAA — Overview & Purpose](#what-is-eaa--overview--purpose)
* [EAA Architecture & Components](#eaa-architecture--components)
* [Key Features](#key-features)
* [Supported Application Types & Use Cases](#supported-application-types--use-cases)
* [Getting Started — Initial Setup](#getting-started--initial-setup)
* [Managing Applications, Identity & Access](#managing-applications-identity--access)
* [Client Access, EAA Client & Device Posture](#client-access-eaa-client--device-posture)
* [Connectors — Deployment & Configuration](#connectors--deployment--configuration)
* [Security & Zero Trust](#security--zero-trust)
* [Audit, Logging, Monitoring & SIEM](#audit-logging-monitoring--siem)
* [Administration & Maintenance](#administration--maintenance)
* [REST API, CLI & Automation](#rest-api-cli--automation)

---

# **What is EAA — Overview & Purpose**

Enterprise Application Access (EAA) is a **Zero Trust Network Access (ZTNA)** solution that provides secure, identity-based, application-specific access to internal enterprise applications **without VPNs or network exposure**.

### **Why EAA?**

* Eliminates traditional VPN attack surface
* Prevents lateral movement inside the network
* Gives application-only access instead of network tunnels
* Integrates with enterprise identity providers
* Enforces device posture before granting access
* Works smoothly for hybrid/remote workforce

EAA follows **Zero Trust**:

> *Never Trust, Always Verify.*

---

# **EAA Architecture & Components**

EAA has three primary architectural units:

## **1. Data Edge (Traffic Plane)**

Handles user traffic securely and efficiently between users → EAA Cloud → Enterprise Connector → Application.

## **2. Management Edge (Control Plane)**

Where admins configure:

* Applications
* Directories
* Identity providers (IdPs)
* Access policies
* Device posture rules
* Connector management

## **3. Enterprise Connector**

A secure outbound-only appliance/VM/container that connects internal applications to EAA Cloud **without opening inbound firewall ports**.

### **Connector Characteristics**

* Outbound TLS (443) only
* No inbound firewall rules
* No direct exposure of internal apps
* Highly available using connector pools

---

# **Key Features**

### ✔ **Clientless access for web apps**

Access via browser without VPN.

### ✔ **Client-based access for non-web apps**

For RDP, SSH, VNC, legacy TCP/UDP, thick clients.

### ✔ **SAML 2.0 SSO for SaaS**

EAA can act as IdP for:

* Office 365
* Salesforce
* ServiceNow
* Atlassian Suite
* GitHub
  …and more.

### ✔ **Advanced Device Posture Checks**

Validate:

* OS version
* Firewall status
* Antivirus status
* Disk encryption
* Patch compliance
* Security products

### ✔ **Granular Access Policies**

Conditions based on:

* Identity
* Groups
* Device posture
* Time windows
* Geo/location
* Risk score

### ✔ **Zero Trust Visibility**

Complete access/usage logs.

### ✔ **Scalability**

Easily add connectors, applications, and user groups.

---

# **Supported Application Types & Use Cases**

## **Application Types**

* **Web/HTTP(S)**
* **SaaS via SAML**
* **Remote protocols**: RDP, SSH, VNC
* **Custom TCP/UDP**
* **Thick client apps**
* **Bookmark apps (URL shortcuts)**

## **Use Cases**

* Secure remote workforce access
* Contractor/third-party isolated access
* Replacement for traditional VPNs
* Secure legacy private apps
* Zero Trust transformation initiatives
* Secure access to cloud workloads

---

# **Getting Started — Initial Setup**

## **1. Prerequisites**

* Akamai Control Center admin access
* Deployment plan for at least one Connector
* Identity provider (IdP) available to integrate

---

## **2. Directory & Identity Setup**

### Supported directory types:

* Cloud Directory
* Active Directory
* LDAP
* AD-LDS
* Azure AD / Okta / Ping (via SAML)

### Setup Steps:

1. Add directory
2. Define attribute mappings
3. Synchronize users/groups
4. Configure access roles
5. Enable MFA (optional but recommended)

---

## **3. Deploy a Connector**

### Deployment Targets:

* VMware ESXi
* Hyper-V
* KVM / OpenStack
* AWS EC2
* Azure VM
* GCP
* Docker container

### Requirements:

* Outbound HTTPS (port 443)
* Static or DHCP IP
* DNS reachable

---

## **4. Configure Applications**

### For Web Apps:

* Define internal hostname
* Assign connector
* Configure TLS (optional)
* Create access policy
* Deploy

### For SaaS Apps:

* Configure SAML metadata
* Upload certificates
* Map attributes
* Test SSO flow

### For RDP/SSH/Custom TCP Apps:

* Create Client Access Application
* Map internal port/hostname
* Publish via EAA Client

---

## **5. Configure Access Policies**

Access rules can include conditions such as:

* User / Group
* Device posture profile
* Geo-location
* Time of day
* MFA requirement
* Risk score

EAA supports **logical AND/OR policy chaining** for fine-grained control.

---

## **6. User Onboarding**

### For web access:

Users log in through browser portal.

### For client-based apps:

Users install **EAA Client**:

* Windows
* macOS
* Linux

Client creates a secure tunnel for TCP/UDP apps.

---

# **Managing Applications, Identity & Access**

## **Application Management Includes:**

* App definitions
* URL rewriting
* Header injection
* Load balancing
* Path mapping
* Internal host routing
* TLS certificates
* Health status
* Deployment versions & rollback

---

## **Identity & Directory Management**

* Multiple IdPs supported
* Flexible attribute mapping
* Directory overlays
* Role-based administrative access
* Policy-based group assignment

---

# **Client Access, EAA Client & Device Posture**

## **EAA Client Features**

* Intercepts DNS requests to protected app
* Creates loopback mapping
* Routes traffic through secure tunnel
* Supports TCP/UDP legacy apps

## **Device Posture Checks**

* Antivirus installed?
* Firewall active?
* OS version minimum?
* Disk encryption?
* USB blocked?
* Custom scripts for posture?

Access is allowed only if posture meets policy.

---

# **Connectors — Deployment & Configuration**

## **Connector Responsibilities**

* Resolve internal hostnames
* Route traffic to app servers
* Encrypt outbound flow
* Load balance between multiple connectors

## **High Availability**

* Connector pools
* Automatic failover
* Pool-based assignment

## **Best Practices**

* Deploy minimum two connectors per location
* Separate web and client access connectors if needed
* Enable monitoring via portal

---

# **Security & Zero Trust**

EAA implements Zero Trust in four layers:

1. **Identity verification**
2. **Device posture verification**
3. **Context verification (location, time, risk)**
4. **Application-specific least-privilege access**

### **Zero Trust Benefits**

* Apps hidden from internet
* No inbound firewall ports
* No lateral movement
* No network-level access
* Reduced credential misuse risk
* Strong compliance & audit trails

---

# **Audit, Logging, Monitoring & SIEM**

## **Logs Available**

* Access logs
* Admin logs
* Connector logs
* Authentication logs
* Device posture logs
* Application event logs

## **SIEM Integration**

Export logs via API to:

* Splunk
* QRadar
* Azure Sentinel
* Elastic
* ArcSight
* Chronicle

---

# **Administration & Maintenance**

### Tasks:

* Update connectors
* Rotate certificates
* Monitor health
* Review audit logs
* Manage user access
* Tune policies
* Enable MFA or strengthen posture rules

### Backup:

* Export configuration
* Maintain version history
* Rollback to safe version

---

# **REST API, CLI & Automation**

EAA supports:

### **1. REST APIs**

To automate:

* App creation
* Policy updates
* Directory sync
* Connector monitoring

### **2. CLI Tool (Akamai CLI EAA Plugin)**

* Manage apps
* Pull logs
* Automate deployments

### **3. IaC**

Can integrate with:

* Terraform
* Ansible
* CI/CD pipelines

---



