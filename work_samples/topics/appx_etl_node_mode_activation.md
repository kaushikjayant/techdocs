# EAA ETL NODE mode activation {#topic_jsc_2qp_rdb}

**Upgrade Preparation**

**Mediation Persistent Data**

-   You will need to select a specific OCP app node to be THE node dedicated to ETL pods: Extract, Transform, Load, Write and PreAggrFormula.

    To enable this behavior, identify node and label it for deployment :


```
oc label node <ETL_NODE_NAME>
        nodetype=<NAMESPACE>-etl
```

-   Create a Service Account as follows which will be used by the ETL pods:

```
oc create serviceaccount
        <ETL_SERVICE_ACCOUNT>
```

```
oc adm policy
        add-scc-to-user hostmount-anyuid -z 
<ETL_SERVICE_ACCOUNT>
```

-   3 PrOptima Mediation Storages identified as RAWDATA, ETL, FLATFILES will be mounted directly on this node.

    → Ensure latest ceph-common package is installed on the etl node to allow access to the Ceph cluster storage with the appropriate access rights setup.

    → Ideally test local mount \(of an anused CephRBD\) to secure the duration of the downtime phase.


-   Setup NFS server on etl node :

    → Install nfs server

    → Allow access from other nodes :


```
sudo iptables -I INPUT -m state --state NEW -p tcp -m
        multiport --dport 111,20048,2049,32803 -s 0.0.0.0/0 -j ACCEPT

```

```
sudo iptables -I INPUT -m state --state NEW -p udp -m
        multiport --dport 111,20048,2049,32803 -s 0.0.0.0/0 -j ACCEPT
sudo /sbin/service
        iptables save
```

**Site configuration**

-   Get latest deployment files

cd <GIT REPO\>

git pull

git checkout 1.5.12

-   Activate ETL Node mode:

> mv <root\_git\_dir\>/eaa-deploy-site-<customer-namespace\>/config/eaa-proptima-mediation.env <root\_git\_dir\>/eaa-deploy-site-<customer-namespace\>/config/eaa-proptima-mediation-etlnode.env

-   Site preparation

    → type :


> <root\_git\_dir\>/eaa-deploy/shell/check-params.sh <customer-namespace\>

Ensure all env files properties are set

→ To check all the PVs that you will have to create. type :

> <root\_git\_dir\>/eaa-deploy/shell/check-pvs.sh <customer-project\>

It should return empty as no new pv has been added.

**Upgrade**

Downtime starts at this step.

**Shutdown Service**

Due to migration of data storages, it is required to shutdown service while operating the upgrade.

oc project <namespace\>

for i in \`oc get dc | grep proptima | sed -s 's/ .\*//'\` ; do

```
oc
          scale *dc* *$i* 
```

```
--replicas=*0 ; done*
```

**Migrate Storage**

**Free RBD Storages to migrate.**

WARNING : Do not delete data inside storages or it will not be recoverable.

→ Delete pvs :

oc delete pv <NAMESPACE\>-proptima-rawdata-pm-volume

oc delete pv <NAMESPACE\>-proptima-etl-pm-volume

oc delete pv <NAMESPACE\>-proptima-flatfiles-pm-volume

→ Free nfs shares : on nfs server,

\* delete the exports for the 3 above pvs \*

\* reload nfs :

service nfs reload

→ Free Ceph mount on nfs server:

\* Umount the 3 folders \(rawdata, etl, flatfiles\): umount /dev/rbd/<pool\_name\>/<image\_name\>

\* Umap the 3 images: rbd unmap /dev/rbd/<pool\_name\>/<image\_name\>

**Enable access from etl node**

-   List the rbd pools
    -   > Example: sudo ceph osd lspools --name client.rbd --keyring /etc/ceph/rbd.keyring


-   List the rbd images of a specific pool
    -   > Example: sudo rbd ls <poolname\> --name client.rbd --keyring /etc/ceph/rbd.keyring

-   Create the images on the Ceph cluster and disabled the not supported features
    -   > Example: sudo rbd create <NAMESPACE\>-proptima-etl-pm --size 320G --pool rbd --name client.rbd --keyring /etc/ceph/rbd.keyring sudo rbd feature disable <NAMESPACE\>-proptima-etl-pm object-map deep-flatten fast-diff exclusive-lock

-   Map the Ceph RBD images on the node manually
    -   It shall be done for RBD images previously referenced in :

        -   <NAMESPACE\>-proptima-rawdata-pm-volume
        -   <NAMESPACE\>-proptima-etl-pm-volume
        -   <NAMESPACE\>-proptima-flatfiles-pm-volume
    -   > Example: sudo rbd map <NAMESPACE\>-proptima-etl-pm --pool rbd --name client.rbd --keyring /etc/ceph/rbd.keyring

-   In case of new image, format it
    -   > Example: sudo mkfs.xfs /dev/rbd/rbd/<NAMESPACE\>-proptima-etl-pm

    -   Example: sudo mkfs.ext4 /dev/rbd/rbd/<NAMESPACE\>-proptima-etl-pm
-   Mount those images on directories defined by the 3 tpl-eaa-proptima-mediation.yaml template parameters, respectively:
    -   RAWDATA\_HOSTPATH
    -   ETL\_HOSTPATH
    -   FLATFILES\_HOSTPATH
    -   > Example: sudo mount /dev/rbd/rbd/<NAMESPACE\>-proptima-etl-pm /srv/rbd/volumes\_eaa\_staging/proptima-data-etl

-   On each mount point run the commands:
    -   sudo chcon -R -u system\_u -r object\_r -t svirt\_sandbox\_file\_t -l s0 <mount-point\>
    -   sudo chown -R mycom:mycom <mount-point\>

-   NFS-export the volumes from the node:

Start an ssh session to the node.

Edit the file

```
/etc/exports
```

and add the following line for each mount point:

```
<mount-point>
        *(rw,no_root_squash)
```

-   Enable NFS to start at boot on the node:

```
sudo systemctl enable nfs-server
```

-   Start the NFS service on the node:

```
sudo systemctl start nfs
```

-   Export the volumes using command:

```
sudo exportfs -a
```

-   Create a NFS PV to mount from this node:

In the template below, replace these 2 parameters :

NAMESPACE: Openshift project name

PRODUCT: "pm" for PrOptima or "proassure" for "ProAssure" NFS\_SHARE\_PATH: path as defined in the /etc/exports file.

```
vi flatfiles-pv.yaml

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

Then create :

```
oc create -f flatfiles-pv.yaml
```

**Deploy Sprint 12**

-   Update Platform :

```
export EAA_PROJECT=<NAMESPACE>
./eaa-deploy/shell/deploy-platform.sh
```

-   Update PrOptima :

```
oc process -f eaa-deploy/template/tpl-eaa-proptima-mediation-etlnode.yaml --param-file eaa-deploy-site-<customer-project>/config/eaa-proptima-mediation-etlnode.env | oc apply -f -
oc process -f eaa-deploy/template/tpl-eaa-proptima-reporting.yaml --param-file eaa-deploy-site-<customer-project>/config/eaa-proptima-reporting.env | oc apply -f -
oc process -f eaa-deploy/template/tpl-eaa-proptima-web-reporting.yaml --param-file eaa-deploy-site-<customer-project>/config/eaa-proptima-web-reporting.env | oc apply -f -
oc process -f eaa-deploy/template/tpl-eaa-proptima-admin.yaml --param-file eaa-deploy-site-<customer-project>/config/eaa-proptima-admin.env | oc apply -f -
oc process -f eaa-deploy/template/tpl-eaa-proptima-ip-management.yaml --param-file eaa-deploy-site-<customer-project>/config/eaa-proptima-ip-management.env | oc apply -f -
```

