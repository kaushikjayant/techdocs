# Customizing PulseAssure Configuration

This section describes the changes that you may need to make to the YAML files corresponding to PulseAssure components. The customizable variables for PulseAssure are described in the table below:

| Variable Name | Description | Example/Default Value |
|--------------|-------------|----------------------|
| **CMDB Bridge Variables** |
| CMDB_ES_INDEX_NAME | CMDB Elastic index name | cmdb |
| CMDB_ES_QUERY_LIMIT | CMDB Elastic query limit | 10000 |
| VENDOR_NAME | Vendor name | bridgon |
| MOI_VENDOR_ATTR_NAME | MOI vendor attribute name | - |
| **Service Designer Variables** |
| SD_CL_CRON_SCHEDULE | CRON expression for collection schedule | 0 0/2 * * * ? |
| SD_ES_INDEX_NAME | Service Designer Elastic index name | servicedesigner |
| **PulseOptima Bridge** |
| FILE_POLLING_RETRY_TIME | File polling retry duration in case of failure (seconds) | 60 |
| MEASUREMENTJOB_MAX_RECOVERY_HOURS | Maximum number of hours for a system job retry | 16 |
| MEASUREMENTJOB_LATE_ARRIVAL_RETRY_HOURS | Hours before a retry in case of failure | 4 |
| MEASUREMENTJOB_FILE_POLLING_INTERVAL | Polling interval in seconds | 300 |
| **FaultShield Bridge** |
| FM_MSMT_LATE_ARRIVAL_RETRY_HOURS | Hours before a retry in case of failure | 4 |
| FM_MSMT_MAX_RECOVERY_HOURS | Maximum number of hours for a system job retry | 1 |
| **TT Bridge** |
| TT_MSMT_LATE_ARRIVAL_RETRY_HOURS | Hours before a retry in case of failure | 4 |
| TT_MSMT_MAX_RECOVERY_HOURS | Maximum number of hours for a system job retry | 1 |
| **PulseAssure-SPM** |
| PROBLEM_MANAGER_APPLICATION_MODE | Set as HA if high availability is configured | HA |
| PROBLEM_MANAGER_REPLICAS | Number of replicas required for PulseAssure-problem-manager pod. Must be '2' or higher for HA, '1' for standalone | 2 |

## Customizing PulseAssure-SPM Configuration File { .section }

Perform the following steps to modify the configuration file for PulseAssure-SPM UI:

1. Navigate to the PulseAssure PVC NFS location:
   ```
   <nfs location>/<oc project location>/PulseAssure
   ```
2. Create a new directory under `/PulseAssure`:
   ```
   spm/problem-manager/config
   ```
3. Create a `config.json` file with the following content under the `/config` directory:
   ```json
   {  
      "ttOriginatorDisplayConfig": {  
         "values": [  
            "Service Assurance"
         ],
         "displayValue": "PulseAssure",
         "defaultDisplayValue": "Non PulseAssure"
      }
   }
   ```

**Note:** You can add values only in the `"values"` array.

**Parent topic:** [Configuring Environment Variables](../topics/configuring_PulseAssure.md)

