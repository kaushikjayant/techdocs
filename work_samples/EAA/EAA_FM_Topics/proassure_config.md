# Customizing NetExpert Configuration {#topic_qqz_5k4_h2b}

This section describes the changes that you may need to make to the YAML files corresponding to NetExpert components. See [Configuring Environment Variables](configuring_proassure.md) for the procedure to customize environment variables in a template. The customizable variables for NetExpert are described in the table below:

|Variable Name|Description|Example/ Default Value|
|-------------|-----------|----------------------|
|**Alert-History-Viewer Variables**| | |
|EAA\_NX\_HISTORY\_VIEWER\_RELEASE\_VERSION|NetExpert Release Version|12.0|
|ELASTIC\_RESPONSE\_LIMIT|Elastic response limit|500|
|ALERT\_SOURCE|Alert source name|NX-FM|
|FM\_QUERY\_CLIENT\_KEY|FM Query client key|f//TqTXsS6NK9ZiRm8coUg==|
|OAUTH\_ROOT\_PATH|Oauth root path|http://oauth2-pm-eaa-staging.apps.ocp.mycom-osi.com/eaanims- oauth2|
|**Alert-Manager Variables**| | |
|EAA\_NX\_VERSION|NetExpert Release Version|12.0|
|EAA\_RELEASE\_VERSION|EAA Release Version|1.5-eaa-12|
|EAA\_AM\_VERSION|EAA Alert Manager Version|12.1.5|

**Note:** Before you start alert manager deployment, you need to update the value of the variable \(EAA\_AM\_VERSION\) to the alert manager version which you want to deploy.

If you want to deploy Alert Manager 12.1.5 the value of the variable must be

```
EAA_AM_VERSION=12.1.5
```

**Parent topic:** [Configuring Environment Variables](../EAA_FM_Topics/configuring_proassure.md)

