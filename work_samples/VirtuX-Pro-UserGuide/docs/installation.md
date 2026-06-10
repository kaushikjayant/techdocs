# VirtuX Pro Installation Guide

## Overview

VirtuX Pro is a Type-2 hypervisor with nested virtualization support, container runtime
integration (Docker/Podman), and a unified management interface for heterogeneous
infrastructure. It runs on Windows, Linux, and macOS, supporting both Intel VT-x/AMD-V
and Apple Hypervisor frameworks.

This guide covers fresh installation, upgrade from previous versions, silent/unattended
deployment, and post-installation validation.

## System Requirements

### Minimum (Development / Evaluation)

| Component | Windows | Linux | macOS |
|:----------|:--------|:------|:------|
| CPU | Intel i5-8500 / AMD Ryzen 5 3600 (4 cores) | Intel i5-8500 / AMD Ryzen 5 3600 (4 cores) | Apple M1/M2/M3 or Intel i7 (4 cores) |
| RAM | 8 GB (16 GB if running guest VMs) | 8 GB (16 GB if running guest VMs) | 8 GB (16 GB if running guest VMs) |
| Disk | 40 GB free (SSD recommended) | 40 GB free (SSD recommended) | 40 GB free (SSD recommended) |
| Hypervisor | Hyper-V enabled (Windows Pro/Enterprise) | KVM (kernel module loaded) | Apple Hypervisor (built-in) |
| GPU | DirectX 12 / Vulkan 1.2 (for GPU passthrough) | Vulkan 1.2 / OpenGL 4.5 | Metal 2 |

### Recommended (Production / Lab Environments)

| Component | Specification |
|:----------|:--------------|
| CPU | Intel Xeon E-2300 / AMD EPYC 7003 (8+ cores, 16+ threads) |
| RAM | 64 GB ECC (scales with guest count: ~2 GB base + guest allocations) |
| Disk | 500 GB NVMe SSD (separate volumes for OS, guest images, and snapshots) |
| Network | 2 × Gigabit or 1 × 10 GbE (separate NIC for management and guest traffic) |
| Hypervisor | KVM on Linux (production); Hyper-V on Windows Server for enterprise deployments |

## Pre-Installation Checklist

Before installing, verify:

- [ ] BIOS/UEFI virtualization extensions enabled (VT-x, AMD-V, or SVM)
- [ ] Hyper-V role installed (Windows) or KVM modules loaded (Linux: `lsmod | grep kvm`)
- [ ] Network: outbound HTTPS (443) reachable for license activation and update checks
- [ ] Administrator/root access on the target system
- [ ] 50 GB free disk space for the VirtuX Pro cache directory and initial guest images
- [ ] NTP time synchronization enabled (required for TLS certificate validation)

---

## Windows Installation

### Standard Installation

1. **Download:** Obtain `VirtuXPro_Setup_2.5.0_x64.msi` from the [VirtuX Pro download portal](https://www.virtuxpro.com/download). Verify the SHA-256 checksum against the published value.

2. **Run the installer** as Administrator:
   - Right-click the `.msi` file → **Run as administrator**
   - If prompted by Windows SmartScreen, click **More info → Run anyway**

3. **Installation Wizard:**
   - **License Agreement:** Review and accept the EULA
   - **Installation Directory:** Default is `C:\Program Files\VirtuXPro`. For production deployments on a dedicated drive, use `D:\VirtuXPro`
   - **Components:** Select options:
     - ☑ VirtuX Pro Core (required)
     - ☑ Management Console (web UI, served on `https://localhost:8443`)
     - ☑ CLI Tools (`virtux.exe` added to PATH)
     - ☐ Nested Virtualization Support (enable only if running VMs inside VMs)
     - ☐ GPU Passthrough Support (requires compatible GPU and drivers)
   - **Data Directory:** Default is `C:\ProgramData\VirtuXPro`. This stores VM configurations, snapshots, and logs. Choose a drive with sufficient space.
   - Click **Install**.

4. **Post-Installation:**
   - The installer adds `virtux.exe` to the system PATH
   - The VirtuX Pro service (`VirtuXService`) starts automatically
   - A desktop shortcut and Start Menu entry are created

### Silent / Unattended Installation

For automated deployment (SCCM, Group Policy, or scripted environments):

```powershell
# Download and verify
$msi = "VirtuXPro_Setup_2.5.0_x64.msi"
$hash = (Get-FileHash $msi -Algorithm SHA256).Hash
if ($hash -ne "EXPECTED_HASH") { throw "Checksum mismatch" }

# Silent install with custom data directory
msiexec /i $msi /qn /norestart `
  INSTALLDIR="D:\VirtuXPro" `
  DATADIR="E:\VirtuXProData" `
  ADDLOCAL="Core,Console,CLI" `
  /L*V "C:\Temp\virtux_install.log"
```

### Adding to System PATH

If the CLI tools weren't added to PATH during installation:

```powershell
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\Program Files\VirtuXPro\bin",
    "Machine"
)
```

---

## Linux Installation

### Package-Based Installation (Recommended)

**Ubuntu / Debian (22.04+, 24.04):**

```bash
# Add the VirtuX Pro repository
curl -fsSL https://apt.virtuxpro.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/virtuxpro-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/virtuxpro-archive-keyring.gpg] https://apt.virtuxpro.com stable main" | sudo tee /etc/apt/sources.list.d/virtuxpro.list

# Install
sudo apt update
sudo apt install -y virtuxpro virtuxpro-console virtuxpro-cli qemu-kvm libvirt-daemon-system

# Start and enable
sudo systemctl enable --now virtuxpro virtuxpro-web
```

**RHEL / CentOS / Rocky Linux (8+, 9+):**

```bash
# Add the VirtuX Pro repository
sudo dnf install -y https://rpm.virtuxpro.com/virtuxpro-release-latest.el$(rpm -E %rhel).noarch.rpm

# Install
sudo dnf install -y virtuxpro virtuxpro-console virtuxpro-cli qemu-kvm libvirt

# Enable KVM module
sudo modprobe kvm-intel  # or kvm-amd for AMD
echo "kvm-intel" | sudo tee /etc/modules-load.d/kvm.conf

# Start and enable
sudo systemctl enable --now virtuxpro virtuxpro-web libvirtd
```

### Tarball Installation (Offline / Air-Gapped)

For environments without package manager access:

```bash
# Download and verify
wget https://www.virtuxpro.com/download/virtuxpro-2.5.0-linux-amd64.tar.gz
wget https://www.virtuxpro.com/download/virtuxpro-2.5.0-linux-amd64.tar.gz.sha256
sha256sum -c virtuxpro-2.5.0-linux-amd64.tar.gz.sha256

# Extract and install
tar -xzf virtuxpro-2.5.0-linux-amd64.tar.gz
cd virtuxpro-2.5.0-linux-amd64

# The install script handles:
# - Binary placement in /opt/virtuxpro/
# - Systemd service unit creation
# - Firewall rules (firewalld/ufw)
# - /usr/local/bin symlinks
sudo ./install.sh --prefix=/opt/virtuxpro --data-dir=/var/lib/virtuxpro

# Verify
virtuxpro version
virtuxpro doctor   # Runs comprehensive system checks
```

### Kernel Module Verification

```bash
# Verify KVM is available
lsmod | grep kvm
# Expected output: kvm_intel or kvm_amd, plus kvm

# Check permissions on /dev/kvm
ls -la /dev/kvm
# Expected: crw-rw---- 1 root kvm

# Add your user to the kvm and libvirt groups
sudo usermod -aG kvm,libvirt $USER
# Log out and back in for group changes to take effect
```

### Firewall Configuration

VirtuX Pro's web console listens on port 8443. Allow access from management workstations:

```bash
# firewalld (RHEL/CentOS/Fedora)
sudo firewall-cmd --permanent --add-port=8443/tcp
sudo firewall-cmd --reload

# ufw (Ubuntu/Debian)
sudo ufw allow from 10.0.0.0/8 to any port 8443 proto tcp
sudo ufw reload

# iptables (generic)
sudo iptables -A INPUT -p tcp --dport 8443 -s 10.0.0.0/8 -j ACCEPT
sudo iptables-save > /etc/iptables/rules.v4
```

---

## macOS Installation

### Standard Installation

1. **Download:** Get `VirtuXPro-2.5.0.dmg` from the [download portal](https://www.virtuxpro.com/download).

2. **Verify the disk image** (optional but recommended):
   ```bash
   shasum -a 256 VirtuXPro-2.5.0.dmg
   # Compare output with published checksum
   ```

3. **Open the DMG** and drag `VirtuX Pro.app` to the `/Applications` folder.

4. **First Launch:**
   - macOS Gatekeeper may block the unsigned extension. Open **System Preferences → Privacy & Security** and click **Allow** for "VirtuX Pro Kernel Extension."
   - If using Apple Silicon (M1/M2/M3), the app runs natively via the Apple Hypervisor framework — no additional kernel extensions needed.
   - For Intel Macs, Hypervisor.framework is used automatically.

5. **Allow execution** if prompted:
   ```bash
   sudo spctl --add /Applications/VirtuX\ Pro.app
   sudo xattr -dr com.apple.quarantine /Applications/VirtuX\ Pro.app
   ```

### Adding CLI Tools to PATH

```bash
# Add to ~/.zshrc (macOS default shell)
echo 'export PATH="/Applications/VirtuX Pro.app/Contents/MacOS:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
virtux version
```

---

## Post-Installation Validation

After installation, run these checks to confirm everything is working:

### Check 1: Service Status

```bash
# Linux
sudo systemctl status virtuxpro virtuxpro-web

# macOS
sudo launchctl list | grep virtuxpro

# Windows
Get-Service VirtuXService
```

### Check 2: CLI Functionality

```bash
virtux version
# Expected: VirtuX Pro v2.5.0 (build 20250601)

virtux doctor
# Checks: hypervisor availability, disk space, network connectivity,
#         port availability, permission levels, NTP sync

virtux info
# Shows: host resources, active VMs, license status, storage pools
```

### Check 3: Web Console Accessibility

Open `https://localhost:8443` in a browser. On first access, accept the self-signed
certificate (production deployments should replace this with a CA-signed certificate).
Log in with the default credentials:
- Username: `admin`
- Password: `admin` (change immediately on first login)

### Check 4: Create a Test VM

```bash
# Download a minimal cloud image for testing
wget https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img

# Create and start a test VM
virtux vm create --name test-vm \
  --cpu 2 --memory 2048 --disk jammy-server-cloudimg-amd64.img \
  --network bridge=virbr0 \
  --start

# Verify it's running
virtux vm list
virtux vm console test-vm
```

---

## Upgrading from Previous Versions

### Linux (Package-Based)

```bash
sudo apt update && sudo apt upgrade virtuxpro virtuxpro-cli   # Debian/Ubuntu
sudo dnf update virtuxpro virtuxpro-cli                       # RHEL/CentOS
sudo systemctl restart virtuxpro virtuxpro-web
virtuxpro db migrate   # Run database migrations if prompted
```

### Windows

Download the latest MSI and run the installer. It will detect the existing installation
and offer an upgrade option. VM configurations and snapshots are preserved.

### macOS

Download the latest DMG and replace the existing `/Applications/VirtuX Pro.app`.
Configuration and VM data (stored in `~/Library/Application Support/VirtuXPro/`) is preserved.

### Pre-Upgrade Checklist

- [ ] Take snapshots of all running VMs
- [ ] Backup `/var/lib/virtuxpro/config.yml` (Linux) or `C:\ProgramData\VirtuXPro\config.yml` (Windows)
- [ ] Review the [release notes](https://www.virtuxpro.com/releases/2.5.0) for breaking changes
- [ ] Schedule a maintenance window if upgrading a production cluster

---

## Uninstallation

### Linux

```bash
# Stop services
sudo systemctl stop virtuxpro virtuxpro-web

# Remove packages
sudo apt purge virtuxpro virtuxpro-cli virtuxpro-console   # Debian/Ubuntu
sudo dnf remove virtuxpro virtuxpro-cli virtuxpro-console   # RHEL/CentOS

# Remove data (careful — this deletes all VMs and snapshots)
sudo rm -rf /var/lib/virtuxpro /etc/virtuxpro /opt/virtuxpro
sudo rm -f /usr/local/bin/virtux

# Remove repository
sudo rm /etc/apt/sources.list.d/virtuxpro.list              # Debian/Ubuntu
sudo rm /etc/yum.repos.d/virtuxpro*.repo                    # RHEL/CentOS
```

### Windows

- Open **Control Panel → Programs and Features** → select VirtuX Pro → **Uninstall**
- Or silently: `msiexec /x {PRODUCT_CODE} /qn`
- Delete data directory manually: `C:\ProgramData\VirtuXPro`

### macOS

```bash
sudo rm -rf /Applications/VirtuX\ Pro.app
rm -rf ~/Library/Application\ Support/VirtuXPro
rm -rf ~/Library/Preferences/com.virtuxpro.plist
```

---

## Support

- **Documentation:** [https://docs.virtuxpro.com](https://docs.virtuxpro.com)
- **Community Forum:** [https://community.virtuxpro.com](https://community.virtuxpro.com)
- **Enterprise Support:** support@virtuxpro.com (SLA: 4-hour response for Sev-1)
- **GitHub:** [https://github.com/virtuxpro](https://github.com/virtuxpro)