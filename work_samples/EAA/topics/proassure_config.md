# Customizing ProAssure Configuration {#topic_qqz_5k4_h2b}

This section describes the changes that you may need to make to the YAML files corresponding to ProAssure components. See [Configuring Environment Variables](configuring_proassure.md) for the procedure to customize environment variables in a template. The customizable variables for ProAssure are described in the table below:

|Variable Name|Description|Example/ Default Value|
|-------------|-----------|----------------------|
|**CMDB Bridge Variables**|
|CMDB\_ES\_INDEX\_NAME|CMDB Elastic index name|cmdb|
|CMDB\_ES\_QUERY\_LIMIT|CMDB Elastic query limit|10000|
|VENDOR\_NAME|Vendor name|MYCOMOSI|
|MOI\_VENDOR\_ATTR\_NAME|MOI vendor attribute name|-|
|**Service Designer Variables**|
|SD\_CL\_CRON\_SCHEDULE|CRON expression for collection schedule|0 0/2 \* \* \* ?|
|SD\_ES\_INDEX\_NAME|Service Designer Elastic index name|servicedesigner|
|**PM Bridge**|
|FILE\_POLLING\_RETRY\_TIME|File polling retry duration in case of failure in seconds|60|
| MEASUREMENTJOB\_MAX\_  
 RECOVERY\_HOURS

 |Maximum number of hours for which a particular system job would be attempted to run|16|
| MEASUREMENTJOB  
 \_LATE\_ARRIVAL\_  
 RETRY\_HOURS

 |Number of hours before a retry in case of failure|4|
| MEASUREMENTJOB  
 \_FILE\_POLLING\_  
 INTERAL

 |Polling interval in second|300|
|**FM Bridge**|
| FM\_MSMT\_LATE\_ARRIVAL  
 \_RETRY\_HOURS

 |Number of hours before a retry in case of failure|4|
| FM\_MSMT\_MAX\_  
 RECOVERY\_HOURS

 |Maximum number of hours for which a particular system job would be attempted to run|1|
|**TT Bridge**|
| TT\_MSMT\_LATE\_ARRIVAL  
 \_RETRY\_HOURS

 |Number of hours before a retry in case of failure|4|
| TT\_MSMT\_MAX\_  
 RECOVERY\_HOURS

 |Maximum number of hours for which a particular system job would be attempted to run|1|
|**PA-SPM**|
|PROBLEM\_MANAGER\_APPLICATION\_MODE|Set as HA if high availability is configured.|HA|
|PROBLEM\_MANAGER\_REPLICAS|The number of replicas required for eaa-pa-problem-manager pod. It must be set to '2' or higher for HA, and '1' for STANDALONE.|2|

## Customizing PA-SPM Configuration File { .section}

Perform the following steps to modify configuration file for PA-SPM UI:

-   Go to ProAssure PVC NFS location. It is as follows:

    ```
    <nfs location>/<oc project location>/proassure
    ```

-   Create a new location under /proassure:

    ```
    spm/problem-manager/config
    ```

-   Create config.jsonwith following content under /config directory:

    ```
    {  
       "ttOriginatorDisplayConfig":{  
          "values":[  
             "Service Assurance"
          ],
          "displayValue":"Proassure",
          "defaultDisplayValue":"Non Proassure"
       }
    }
    ```


**Note:** You can add values only in the `"values"` array.

**Parent topic:** [Configuring Environment Variables](../topics/configuring_proassure.md)

