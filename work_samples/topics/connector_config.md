# Customizing Connectors Configuration {#topic_gc1_xk4_h2b}

This section describes the changes that you may need to make to the YAML files corresponding to ProAssure connectors. See [Configuring Environment Variables](configuring_proassure.md) for the procedure to customize environment variables in a template. The customizable variables for ProAssure are described in the table below:

|Variable Name|Description|Example/ Default Value|
|-------------|-----------|----------------------|
|**FM Netcool Connector**|
| FMINGESTION\_ALARM  
 \_BATCH\_SIZE

 |Alarm batch size to be ingested|1|
|JSON\_PATH|Configuration file default path|/opt/mycomosi/var/db/fm-netcool-connector|
|**CMDB Generic Connector**|
|CMDB\_ES\_QUERY\_LIMIT|CMDB Elastic query limit|10000|
|CGC\_ES\_INDEX\_NAME|CMDB Elastic index name|cgc|
|JSON\_ROOTPATH|Location of the configuration JSON file|/opt/mycomosi/data/web/var/db/cmdb-generic-connector|
|**BMC TT Connector**|
|BMC\_USERNAME|BMC account user name|sasmintuser|
|BMC\_PASSWORD|BMC account password|password|
|BMC\_INCIDENT\_WSDL|BMC incident WSDL file path| /opt/mycomosi/var/  
 db/bmc-tt-connector/  
 WSDL-path/H3G\_SA\_  
 SM\_HPD\_IncidentInterface  
 \_Staging\_WS.xml

 |
|BMC\_PROBLEM\_WSDL|BMC problem WSDL file path| /opt/mycomosi/var/db/  
 bmc-tt-connector/  
 WSDL-path/H3G\_PBM  
 \_ProblemInterface\_  
 Staging\_WS.xml

 |
|BMC\_INCIDENT\_QUERY\_WSDL|BMC incident query WSDL file path| /opt/mycomosi/var/db/  
 bmc-tt-connector/  
 WSDL-path/H3G\_  
 HPD\_IncidentInterface  
 \_WS.xml

 |
|VALUE\_MAPPING\_PATH|Value mapping JSON file path|/opt/mycomosi/var/db/bmc-tt-connector/value-mapping/BMC\_TT\_ENUM\_MAPPING.json|
|SEVERITY\_MAPPING\_PATH|Severity mapping JSON file path|/opt/mycomosi/var/db/bmc-tt-connector/value-mapping/PRIORITY\_TT\_SEVERITY.json|

**Parent topic:** [Configuring Environment Variables](../topics/configuring_proassure.md)

