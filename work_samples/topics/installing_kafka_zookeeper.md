# Installing Big Data Framework {#topic_rny_2gx_kcb}

**Content**

The following procedure will deploy the following frameworks:

-   Zookeeper
-   Kafka
-   Spark \(spark master, spark workers, spark-ui proxy\)
-   Redis

**Procedure**

**PV**

The following PVs will have to be created.

For zookeeper

For each of your zookeeper replicas \(by default 3\), a PV has to be created.

It has to be "associated" to the storage class "*eaa-platform-zookeeper-data*" and to the gid "1000" through the following annotations:

```
metadata:
 annotations:
 [pv.beta.kubernetes.io/gid](http://pv.beta.kubernetes.io/gid): "1000"
 [volume.beta.kubernetes.io/storage-class](http://volume.beta.kubernetes.io/storage-class): eaa-platform-zookeeper-data
```

Example of a "Zookeeper" Amazon EBS PV:

```
- apiVersion: v1
 kind: PersistentVolume
 metadata:
 annotations:
 [pv.beta.kubernetes.io/gid](http://pv.beta.kubernetes.io/gid): "1000"
 [volume.beta.kubernetes.io/storage-class](http://volume.beta.kubernetes.io/storage-class): eaa-platform-zookeeper-data
 labels:
 [failure-domain.beta.kubernetes.io/region](http://failure-domain.beta.kubernetes.io/region): eu-west-1
 [failure-domain.beta.kubernetes.io/zone](http://failure-domain.beta.kubernetes.io/zone): eu-west-1a
 name:<your namespace>-eaa-platform-zookeeper-data-1
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

For Kafka

For each of your kafka replicas \(by default 3\), a PV has to be created.

It has to be "associated" to the storage class "*eaa-platform-kafka-data*" and to the gid "1000" through the following annotations:

```
 metadata:
 annotations:
 [pv.beta.kubernetes.io/gid](http://pv.beta.kubernetes.io/gid): "1000"
 [volume.beta.kubernetes.io/storage-class](http://volume.beta.kubernetes.io/storage-class): eaa-platform-kafka-data
```

Example of a "Kafka" Amazon EBS PV:

```
- apiVersion: v1
 kind: PersistentVolume
 metadata:
 annotations:
 [pv.beta.kubernetes.io/gid](http://pv.beta.kubernetes.io/gid): "1000"
 [volume.beta.kubernetes.io/storage-class](http://volume.beta.kubernetes.io/storage-class): eaa-platform-kafka-data
 labels:
 [failure-domain.beta.kubernetes.io/region](http://failure-domain.beta.kubernetes.io/region): eu-west-1
 [failure-domain.beta.kubernetes.io/zone](http://failure-domain.beta.kubernetes.io/zone): eu-west-1a
 name: <your namespace>-eaa-platform-kafka-data-0
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

For Spark workers

Two "global" PVs have to be created.

One for sharing spark application jars between the spark workers, the other to checkpoint the internal states of your running spark applications.

Those 2 PVs have to be named respectively:

-   spark-app-jars-<your namespace\>-volume
-   spark-app-checkcp-<your namespace\>-volume

Those 2 PVs have to be read-write many PV \(for example, NFS PVs will work\).

For Redis:

Create a PV for Redis and name it as pv-redis.

```
metadata:
name: eaa-platform-redis-eaa-staging-21-pv-1
```

Example of a "Redis" Amazon EBS PV:

```
apiVersion: v1
kind: List
items:
- apiVersion: v1
kind: PersistentVolume
metadata:
name: eaa-platform-redis-eaa-staging-21-pv-1
spec:
accessModes:
- ReadWriteMany
capacity:
storage: 128Mi
nfs:
path: /srv/nfs/volumes_eaa_staging_2_1/redis/redis-1
server: [nfs01.ocp.mycom-osi.com](http://nfs01.ocp.mycom-osi.com)
persistentVolumeReclaimPolicy: Retain
```

**Deploy**

Go to <root\_git\_dir\> directory in terminal and execute:

```
./eaa-deploy/shell/deploy-big-data-platform.sh --freshinstall
```

Deploy Redis:

```
./eaa-deploy/shell/deploy-redis.sh --dryrun
./eaa-deploy/shell/deploy-redis.sh --proceed
```

**Checks**

Wait for all deployments finish :

```
./eaa-deploy/shell/waitEndOfDeployment.sh
```

When finished, check status:

```
python ./eaa-deploy/shell/check-deployment-status.py
```

