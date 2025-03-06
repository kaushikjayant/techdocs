# EAA ETL NODE Mode Activation {#topic_jsc_2qp_rdb}

## Upgrade Preparation

### Mediation Persistent Data

- Select a specific OCP app node to be dedicated for ETL pods (Extract, Transform, Load, Write, and PreAggrFormula).
- Label the selected node for deployment:

  ```sh
  oc label node <ETL_NODE_NAME> nodetype=<NAMESPACE>-etl
  ```

- Create a Service Account for ETL pods:

  ```sh
  oc create serviceaccount <ETL_SERVICE_ACCOUNT>
  ```

  ```sh
  oc adm policy add-scc-to-user hostmount-anyuid -z <ETL_SERVICE_ACCOUNT>
  ```

- Mount three PrOptima Mediation Storages (RAWDATA, ETL, FLATFILES) directly on the node.
  - Ensure the latest `ceph-common` package is installed.
  - Test local mount of an unused CephRBD.

### Setup NFS Server on ETL Node

- Install NFS server.
- Allow access from other nodes:

  ```sh
  sudo iptables -I INPUT -m state --state NEW -p tcp -m multiport --dport 111,20048,2049,32803 -s 0.0.0.0/0 -j ACCEPT
  sudo iptables -I INPUT -m state --state NEW -p udp -m multiport --dport 111,20048,2049,32803 -s 0.0.0.0/0 -j ACCEPT
  sudo /sbin/service iptables save
  ```

## Site Configuration

- Get latest deployment files:

  ```sh
  cd <GIT_REPO>
  git pull
  git checkout 1.5.12
  ```

- Activate ETL Node mode:

  ```sh
  mv <root_git_dir>/eaa-deploy-site-<customer-namespace>/config/eaa-proptima-mediation.env \
     <root_git_dir>/eaa-deploy-site-<customer-namespace>/config/eaa-proptima-mediation-etlnode.env
  ```

- Prepare the site:

  ```sh
  <root_git_dir>/eaa-deploy/shell/check-params.sh <customer-namespace>
  ```

- Verify required PVs:

  ```sh
  <root_git_dir>/eaa-deploy/shell/check-pvs.sh <customer-project>
  ```

  It should return empty if no new PVs are added.

## Upgrade

### Shutdown Service

Due to data migration, services must be shut down before upgrade.

```sh
oc project <namespace>
for i in `oc get dc | grep proptima | sed -s 's/ .*//'` ; do
  oc scale dc $i --replicas=0
done
```

### Migrate Storage

#### Free RBD Storages to Migrate

**Warning:** Do not delete data inside storages.

```sh
oc delete pv <NAMESPACE>-proptima-rawdata-pm-volume
oc delete pv <NAMESPACE>-proptima-etl-pm-volume
oc delete pv <NAMESPACE>-proptima-flatfiles-pm-volume
```

- Remove NFS exports and reload NFS:

  ```sh
  service nfs reload
  ```

- Unmount and unmap Ceph volumes:

  ```sh
  umount /dev/rbd/<pool_name>/<image_name>
  rbd unmap /dev/rbd/<pool_name>/<image_name>
  ```

### Enable Access from ETL Node

- List RBD pools:

  ```sh
  sudo ceph osd lspools --name client.rbd --keyring /etc/ceph/rbd.keyring
  ```

- List RBD images of a pool:

  ```sh
  sudo rbd ls <poolname> --name client.rbd --keyring /etc/ceph/rbd.keyring
  ```

- Create Ceph RBD images:

  ```sh
  sudo rbd create <NAMESPACE>-proptima-etl-pm --size 320G --pool rbd --name client.rbd --keyring /etc/ceph/rbd.keyring
  sudo rbd feature disable <NAMESPACE>-proptima-etl-pm object-map deep-flatten fast-diff exclusive-lock
  ```

- Map RBD images on the node:

  ```sh
  sudo rbd map <NAMESPACE>-proptima-etl-pm --pool rbd --name client.rbd --keyring /etc/ceph/rbd.keyring
  ```

- Format and mount images:

  ```sh
  sudo mkfs.xfs /dev/rbd/rbd/<NAMESPACE>-proptima-etl-pm
  sudo mount /dev/rbd/rbd/<NAMESPACE>-proptima-etl-pm /srv/rbd/volumes_eaa_staging/proptima-data-etl
  ```

- Adjust ownership and permissions:

  ```sh
  sudo chcon -R -u system_u -r object_r -t svirt_sandbox_file_t -l s0 <mount-point>
  sudo chown -R mycom:mycom <mount-point>
  ```

- Export NFS volumes:

  ```sh
  echo "<mount-point> *(rw,no_root_squash)" | sudo tee -a /etc/exports
  sudo systemctl enable nfs-server
  sudo systemctl start nfs
  sudo exportfs -a
  ```

### Create NFS PV

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: <NAMESPACE>-proptima-flatfiles-<PRODUCT>-volume
spec:
  accessModes:
  - ReadWriteMany
  capacity:
    storage: 100Gi
  nfs:
    server: <ETL_NODE_NAME>
    path: <NFS_SHARE_PATH>
  persistentVolumeReclaimPolicy: Retain
status: {}
```

```sh
oc create -f flatfiles-pv.yaml
```

### Update Platform

```sh
export EAA_PROJECT=<NAMESPACE>
./eaa-deploy/shell/deploy-platform.sh
```

### Update PrOptima

```sh
oc process -f eaa-deploy/template/tpl-eaa-proptima-mediation-etlnode.yaml --param-file eaa-deploy-site-<customer-project>/config/eaa-proptima-mediation-etlnode.env | oc apply -f -
oc process -f eaa-deploy/template/tpl-eaa-proptima-reporting.yaml --param-file eaa-deploy-site-<customer-project>/config/eaa-proptima-reporting.env | oc apply -f -
oc process -f eaa-deploy/template/tpl-eaa-proptima-web-reporting.yaml --param-file eaa-deploy-site-<customer-project>/config/eaa-proptima-web-reporting.env | oc apply -f -
oc process -f eaa-deploy/template/tpl-eaa-proptima-admin.yaml --param-file eaa-deploy-site-<customer-project>/config/eaa-proptima-admin.env | oc apply -f -
oc process -f eaa-deploy/template/tpl-eaa-proptima-ip-management.yaml --param-file eaa-deploy-site-<customer-project>/config/eaa-proptima-ip-management.env | oc apply -f -
```

