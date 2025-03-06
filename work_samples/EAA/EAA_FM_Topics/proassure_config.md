[Home](../index.md)
# Customizing FaultShield Configuration

This section outlines the necessary modifications to the YAML files for FaultShield components. For details on customizing environment variables in a template, refer to [Configuring Environment Variables](configuring_proassure.md). The table below lists the customizable variables for FaultShield:

| Variable Name | Description | Example/ Default Value |
|--------------|-------------|----------------------|
| **Alert-History-Viewer Variables** |  |  |
| EAA_NX_HISTORY_VIEWER_RELEASE_VERSION | FaultShield Release Version | 12.0 |
| ELASTIC_RESPONSE_LIMIT | Elastic response limit | 500 |
| ALERT_SOURCE | Alert source name | FS |
| FS_QUERY_CLIENT_KEY | FS Query client key | f//TqTXsS6NK9ZiRm8coUg== |
| OAUTH_ROOT_PATH | OAuth root path | http://oauth2-pm-netpulse-staging.apps.ocp.mycom.com/eaanims-oauth2 |
| **Alert-Manager Variables** |  |  |
| EAA_NX_VERSION | FaultShield Release Version | 12.0 |
| EAA_RELEASE_VERSION | EAA Release Version | 1.5-eaa-12 |
| EAA_AM_VERSION | EAA Alert Manager Version | 12.1.5 |

**Note:** Before deploying Alert Manager, update the value of `EAA_AM_VERSION` to the desired Alert Manager version.

For example, to deploy Alert Manager version 12.1.5, set:

```
EAA_AM_VERSION=12.1.5
```

**Parent topic:** [Configuring Environment Variables](../EAA_FM_Topics/configuring_proassure.md)

[Home](../index.md)
