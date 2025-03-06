[Home](../index.md)
# Customizing Connectors Configuration 

This section describes the changes that you may need to make to the YAML files corresponding to PulseAssure connectors. See [Configuring Environment Variables](../topics/configuring_proassure.md) for the procedure to customize environment variables in a template. The customizable variables for PulseAssure are described in the table below:

| Variable Name | Description | Example/ Default Value |
|--------------|-------------|----------------------|
| **FM Netcool Connector** |
| FMINGESTION_ALARM_BATCH_SIZE | Alarm batch size to be ingested | 1 |
| JSON_PATH | Configuration file default path | /opt/bridgon/var/db/fm-netcool-connector |
| **CMDB Generic Connector** |
| CMDB_ES_QUERY_LIMIT | CMDB Elastic query limit | 10000 |
| CGC_ES_INDEX_NAME | CMDB Elastic index name | cgc |
| JSON_ROOTPATH | Location of the configuration JSON file | /opt/bridgon/data/web/var/db/cmdb-generic-connector |
| **BMC TT Connector** |
| BMC_USERNAME | BMC account user name | sasmintuser |
| BMC_PASSWORD | BMC account password | password |
| BMC_INCIDENT_WSDL | BMC incident WSDL file path | /opt/bridgon/var/db/bmc-tt-connector/WSDL-path/H3G_SA_SM_HPD_IncidentInterface_Staging_WS.xml |
| BMC_PROBLEM_WSDL | BMC problem WSDL file path | /opt/bridgon/var/db/bmc-tt-connector/WSDL-path/H3G_PBM_ProblemInterface_Staging_WS.xml |
| BMC_INCIDENT_QUERY_WSDL | BMC incident query WSDL file path | /opt/bridgon/var/db/bmc-tt-connector/WSDL-path/H3G_HPD_IncidentInterface_WS.xml |
| VALUE_MAPPING_PATH | Value mapping JSON file path | /opt/bridgon/var/db/bmc-tt-connector/value-mapping/BMC_TT_ENUM_MAPPING.json |
| SEVERITY_MAPPING_PATH | Severity mapping JSON file path | /opt/bridgon/var/db/bmc-tt-connector/value-mapping/PRIORITY_TT_SEVERITY.json |

**Parent topic:** [Configuring Environment Variables](../topics/configuring_proassure.md)

[Home](../index.md)
