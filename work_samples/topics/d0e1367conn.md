# Installing Connectors {#d0e1367}

This script will deploy the following connectors:

-   *CMDB Granite Connector*
-   *CMDB Granite Soap C1 Connector*
-   *CT-Remedy SOAP Connector*
-   *CMDB Generic Connector*
-   *TT Connector*
-   *TMF 524 Connector*
-   *FM Netcool Connector*
-   *BMC Inventory Connector*
-   BMC TT SOAP NBI Connector
-   BMC TT Remedy Kafka Connector
-   CMDB Granite SOAP Connector

## Preparing Installation { .section}

-   Clone the required repositories for installing connectors:

    ```
    git clone git@gitlab.mycom-osi.com:eaa/eaa-deploy.git
    git clone git@gitlab.mycom-osi.com:eaa/eaa-proassure-connector.git
    ```

-   Check the connectors versions to be installed by running the following command.

    ```
    cat eaa-proassure-connector/release-version.txt
    ```

-   Ensure that the templates required for installation exist by running the following command:

    ```
    ls -la eaa-proassure-connector/template
    ```


## Installing Connectors { .section}

Install connectors by performing the following steps:

-   Perform a dryrun installation by running the following command:

    ```
    deploy-connector.sh --dryrun eaa-<connector-name>
    ```

    For example:

    ```
    cd ~/eaa-proassure-connector
    ./shell/deploy-connector.sh --dryrun eaa-cmdb-granite-connector
    ```

    **Note:** The above example demonstrates the deployment of the eaa-cmdb-granite-connector template. You must separately run the command by replacing the connector name for each template that needs to be deployed. You must additionally run the command after replacing eaa-<connector-name\> with:

    -   eaa-cmdb-granite-soap-c1-connector to deploy CMDB Granite Soap C1 Connector.
    -   eaa-fm-netcool-kafka-c1-connector to deploy FM Netcool Kafka C1 Connector.
    -   eaa-bmc-inventory-connector to deploy BMC Inventory Connector.
    -   eaa-bmc-tt-connector to deploy TT Connector.
    -   eaa-cmdb-generic-connector to deploy CMDB Generic Connector.
    -   eaa-ct-remedy-soap-c1-connector to deploy CT Remedy SOAP Connector.
    -   eaa-fm-netcool-connector to deploy FM Netcool Connector.
    -   eaa-tmf524-connector to deploy TMF524 Connector.
    -   eaa-tt-remedy-soap-c2s-connector to deploy ProAssure BMC TT SOAP SBI Connector
    -   eaa-tt-remedy-soap-c2n-connector to deploy BMC TT SOAP NBI Connector
    -   eaa-tt-remedy-kafka-c1-connector to deploy BMC TT Remedy Kafka Connector
    -   eaa-cmdb-granite-soap-c1-connector to deploy CMDB Granite SOAP Connector
    An output similar to the following is displayed:

    ```
    /home/mycom/eaa-deploy-site-<$EAA_PROJECT>
    Changing to project 'connector' 
    Reading connector template file by eaa-cmdb-granite-connector
    Installing eaa-cmdb-granite-connector:2.2.6.0
    [20180614-10:49:52] [INFO] Processing template tpl-eaa-cmdb-granite-connector.yaml ...
    [20180614-10:49:55] [INFO]    ... Injected 3 dimensioning parameters
    All done
    ```

-   Run the installation script in --proceed mode to complete the installation:

    ```
    deploy-connector.sh --proceed eaa-<connector-name>
    ```

    For example:

    ```
    cd ~/eaa-proassure-connector
    ./shell/deploy-connector.sh --proceed eaa-cmdb-granite-connector
    ```

    **Note:** The above example demonstrates the deployment of the eaa-cmdb-granite-connector template. You must separately run the command by replacing the connector name for each template that needs to be deployed. You must additionally run the command after replacing eaa-<connector-name\> with:

    -   eaa-bmc-inventory-connector to deploy BMC Inventory Connector.
    -   eaa-cmdb-granite-soap-c1-connector to deploy CMDB Granite Soap C1 Connector.
    -   eaa-fm-netcool-kafka-c1-connector to deploy FM Netcool Kafka C1 Connector.
    -   eaa-bmc-tt-connector to deploy TT Connector.
    -   eaa-cmdb-generic-connector to deploy CMDB Generic Connector.
    -   eaa-ct-remedy-soap-c1-connector to deploy CT Remedy SOAP Connector.
    -   eaa-fm-netcool-connector to deploy FM Netcool Connector.
    -   eaa-tmf524-connector to deploy TMF524 Connector.
    -   eaa-tt-remedy-soap-c2s-connector to deploy ProAssure BMC TT SOAP SBI Connector
    -   eaa-tt-remedy-soap-c2n-connector to deploy BMC TT SOAP NBI Connector
    -   eaa-tt-remedy-kafka-c1-connector to deploy BMC TT Remedy Kafka Connector
    -   eaa-cmdb-granite-soap-c1-connector to deploy CMDB Granite SOAP Connector
    An output similar to the following is displayed:

    ```
    /home/mycom/eaa-deploy-site-<$EAA_PROJECT>
    Changing to project 'connector'
    Reading connector template file by eaa-cmdb-granite-connector
    Installing eaa-cmdb-granite-connector:2.4.6.0
    [20180614-10:53:27] [INFO] Processing template tpl-eaa-cmdb-granite-connector.yaml ...
    [20180614-10:53:29] [INFO]    ... Injected 3 dimensioning parameters
    imagestream "eaa-cmdb-granite-connector" configured
    deploymentconfig "eaa-cmdb-granite-connector" configured
    service "eaa-cmdb-granite-connector" configured
    route "eaa-cmdb-granite-connector" configured
    Importing eaa-cmdb-granite-connector:2.4.6.0 image...
    All done
    ```

    The connectors are installed.


