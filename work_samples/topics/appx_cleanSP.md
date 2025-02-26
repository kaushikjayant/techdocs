# Cleaning Service Problems {#topic_ozs_wzj_bfb}

Clean Service problems from elastic as follows:

-   Stop spark apps by running the `Kill_running_drivers.sh` script from the spark-app-gateway pod.
-   Run the following command:

    ```
    oc describe pv spark-app-checkp-<site>-volume
    ```

-   Look for line:

    ```
    Path: /<xxxx>/spark/checkpoints
    ```

-   Remove the content of this directory from NFS.
-   Fetch the IP of redis master node service:

    ```
    oc get svc | grep -i redis
    eaa-platform-redis 172.30.253.116 <none> 6379/TCP  
    oc rsh redis-sentinel pod
    ```

-   Run following commands:

    ```
    redis-cli -h 172.30.253.116 -p 6379 --raw keys spm* | xargs redis-cli -h 172.30.253.116 -p 6379 del 
    redis-cli -h 172.30.253.116 -p 6379 --raw keys sie* | xargs redis-cli -h 172.30.253.116 -p 6379 del
    ```

-   To delete SPM elastic indexes, run:

    ```
    curl –XDELETE <elastic-host-url-in-openshift>/spmingestion
    curl –XDELETE <elastic-host-url-in-openshift>/problem-tracking-records
    ```

-   After executing above commands, restart eaa-pa-spm-ingestion pod.
-   Restart the eaa-pa-problem-manager pod.

