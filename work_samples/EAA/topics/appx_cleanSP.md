[Home](../index.md)
# Cleaning Service Problems

Clean service problems from Elastic by following these steps:

1. **Stop Spark Apps**
   - Run the `Kill_running_drivers.sh` script from the `spark-app-gateway` pod.

2. **Verify Persistent Volume (PV) Path**
   - Run the following command:
     ```
     oc describe pv spark-app-checkp-<site>-volume
     ```
   - Look for the line:
     ```
     Path: /<xxxx>/spark/checkpoints
     ```
   - Remove the content of this directory from NFS.

3. **Fetch Redis Master Node Service IP**
   - Run the following command:
     ```
     oc get svc | grep -i redis
     ```
     Example output:
     ```
     eaa-platform-redis 172.30.253.116 <none> 6379/TCP  
     ```
   - Access the Redis Sentinel pod:
     ```
     oc rsh redis-sentinel pod
     ```

4. **Clear Redis Keys**
   - Run the following commands to delete relevant keys:
     ```
     redis-cli -h 172.30.253.116 -p 6379 --raw keys spm* | xargs redis-cli -h 172.30.253.116 -p 6379 del
     redis-cli -h 172.30.253.116 -p 6379 --raw keys sie* | xargs redis-cli -h 172.30.253.116 -p 6379 del
     ```

5. **Delete SPM Elastic Indexes**
   - Run the following commands:
     ```
     curl -XDELETE <elastic-host-url-in-openshift>/spmingestion
     curl -XDELETE <elastic-host-url-in-openshift>/problem-tracking-records
     ```

6. **Restart Required Pods**
   - Restart the `eaa-pa-spm-ingestion` pod.
   - Restart the `eaa-pa-problem-manager` pod.

[Home](../index.md)
