[Home](index.md)

# Installing Big Data Framework

## Content

The following procedure will deploy the following frameworks:

- Zookeeper
- Kafka
- Spark (Spark Master, Spark Workers, Spark-UI Proxy)
- Redis

## Procedure

### Persistent Volumes (PV)

#### Zookeeper
For each Zookeeper replica (default: 3), a PV must be created. It should be associated with the storage class `netpulse-platform-zookeeper-data` and the GID `1000` using the following annotations:

```yaml
metadata:
  annotations:
    pv.beta.kubernetes.io/gid: "1000"
    volume.beta.kubernetes.io/storage-class: netpulse-platform-zookeeper-data
```

Example of a Zookeeper Amazon EBS PV:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  annotations:
    pv.beta.kubernetes.io/gid: "1000"
    volume.beta.kubernetes.io/storage-class: netpulse-platform-zookeeper-data
  labels:
    failure-domain.beta.kubernetes.io/region: eu-west-1
    failure-domain.beta.kubernetes.io/zone: eu-west-1a
  name: <your-namespace>-netpulse-platform-zookeeper-data-1
spec:
  accessModes:
    - ReadWriteOnce
  awsElasticBlockStore:
    fsType: xfs
    volumeID: vol-033000a44c3e24548
  capacity:
    storage: 10Gi
  persistentVolumeReclaimPolicy: Retain
```

#### Kafka
For each Kafka replica (default: 3), a PV must be created. It should be associated with the storage class `netpulse-platform-kafka-data` and the GID `1000` using the following annotations:

```yaml
metadata:
  annotations:
    pv.beta.kubernetes.io/gid: "1000"
    volume.beta.kubernetes.io/storage-class: netpulse-platform-kafka-data
```

Example of a Kafka Amazon EBS PV:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  annotations:
    pv.beta.kubernetes.io/gid: "1000"
    volume.beta.kubernetes.io/storage-class: netpulse-platform-kafka-data
  labels:
    failure-domain.beta.kubernetes.io/region: eu-west-1
    failure-domain.beta.kubernetes.io/zone: eu-west-1a
  name: <your-namespace>-netpulse-platform-kafka-data-0
spec:
  accessModes:
    - ReadWriteOnce
  awsElasticBlockStore:
    fsType: xfs
    volumeID: vol-0a2d7f88dec0548ec
  capacity:
    storage: 10Gi
  persistentVolumeReclaimPolicy: Retain
```

#### Spark Workers
Two global PVs must be created:

- One for sharing Spark application JARs between workers.
- One for checkpointing the internal states of running Spark applications.

These PVs should be named as follows:

- `spark-app-jars-<your-namespace>-volume`
- `spark-app-checkcp-<your-namespace>-volume`

These PVs should support ReadWriteMany mode (e.g., NFS PVs).

#### Redis
Create a PV for Redis named `pv-redis`.

```yaml
metadata:
  name: netpulse-platform-redis-netpulse-staging-21-pv-1
```

Example of a Redis Amazon EBS PV:

```yaml
apiVersion: v1
kind: List
items:
  - apiVersion: v1
    kind: PersistentVolume
    metadata:
      name: netpulse-platform-redis-netpulse-staging-21-pv-1
    spec:
      accessModes:
        - ReadWriteMany
      capacity:
        storage: 128Mi
      nfs:
        path: /srv/nfs/volumes_netpulse_staging_2_1/redis/redis-1
        server: nfs01.ocp.bridgon.com
      persistentVolumeReclaimPolicy: Retain
```

## Deployment

Navigate to `<root_git_dir>` in the terminal and execute:

```sh
./netpulse-deploy/shell/deploy-big-data-platform.sh --freshinstall
```

### Deploy Redis

```sh
./netpulse-deploy/shell/deploy-redis.sh --dryrun
./netpulse-deploy/shell/deploy-redis.sh --proceed
```

## Checks

Wait for all deployments to finish:

```sh
./netpulse-deploy/shell/waitEndOfDeployment.sh
```

Check deployment status:

```sh
python ./netpulse-deploy/shell/check-deployment-status.py
```

[Home](index.md)

