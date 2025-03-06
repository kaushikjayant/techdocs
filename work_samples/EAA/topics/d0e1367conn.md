[Home](../index.md)
# Installing Connectors

This script deploys the following connectors:

- *CMDB Granite Connector*
- *CMDB Granite SOAP C1 Connector*
- *CT-Remedy SOAP Connector*
- *CMDB Generic Connector*
- *TT Connector*
- *TMF 524 Connector*
- *FM Netcool Connector*
- *BMC Inventory Connector*
- *BMC TT SOAP NBI Connector*
- *BMC TT Remedy Kafka Connector*
- *CMDB Granite SOAP Connector*

## Preparing for Installation

1. Clone the required repositories for installing connectors:

    ```sh
    git clone git@gitlab.bridgon.com:ncp/ncp-deploy.git
    git clone git@gitlab.bridgon.com:ncp/netpulseassure-connector.git
    ```

2. Verify the connector versions to be installed:

    ```sh
    cat netpulseassure-connector/release-version.txt
    ```

3. Ensure the required templates exist:

    ```sh
    ls -la netpulseassure-connector/template
    ```

## Installing Connectors

### Dry Run Installation

1. Perform a dry run installation to validate deployment:

    ```sh
    deploy-connector.sh --dryrun ncp-<connector-name>
    ```

    Example:

    ```sh
    cd ~/netpulseassure-connector
    ./shell/deploy-connector.sh --dryrun ncp-cmdb-granite-connector
    ```

2. Replace `<connector-name>` with the appropriate connector name:

    - `ncp-cmdb-granite-soap-c1-connector` – CMDB Granite SOAP C1 Connector
    - `ncp-fm-netcool-kafka-c1-connector` – FM Netcool Kafka C1 Connector
    - `ncp-bmc-inventory-connector` – BMC Inventory Connector
    - `ncp-bmc-tt-connector` – TT Connector
    - `ncp-cmdb-generic-connector` – CMDB Generic Connector
    - `ncp-ct-remedy-soap-c1-connector` – CT Remedy SOAP Connector
    - `ncp-fm-netcool-connector` – FM Netcool Connector
    - `ncp-tmf524-connector` – TMF 524 Connector
    - `ncp-tt-remedy-soap-c2s-connector` – FaultShield BMC TT SOAP SBI Connector
    - `ncp-tt-remedy-soap-c2n-connector` – BMC TT SOAP NBI Connector
    - `ncp-tt-remedy-kafka-c1-connector` – BMC TT Remedy Kafka Connector
    - `ncp-cmdb-granite-soap-c1-connector` – CMDB Granite SOAP Connector

    Sample output:

    ```sh
    /home/bridgon/ncp-deploy-site-<$NCP_PROJECT>
    Changing to project 'connector'
    Reading connector template file by ncp-cmdb-granite-connector
    Installing ncp-cmdb-granite-connector:2.2.6.0
    [INFO] Processing template tpl-ncp-cmdb-granite-connector.yaml ...
    [INFO]    ... Injected 3 dimensioning parameters
    All done
    ```

### Proceed with Installation

1. Run the installation script in `--proceed` mode to complete the deployment:

    ```sh
    deploy-connector.sh --proceed ncp-<connector-name>
    ```

    Example:

    ```sh
    cd ~/netpulseassure-connector
    ./shell/deploy-connector.sh --proceed ncp-cmdb-granite-connector
    ```

2. Replace `<connector-name>` as in the dry run step above.

    Sample output:

    ```sh
    /home/bridgon/ncp-deploy-site-<$NCP_PROJECT>
    Changing to project 'connector'
    Reading connector template file by ncp-cmdb-granite-connector
    Installing ncp-cmdb-granite-connector:2.4.6.0
    [INFO] Processing template tpl-ncp-cmdb-granite-connector.yaml ...
    [INFO]    ... Injected 3 dimensioning parameters
    imagestream "ncp-cmdb-granite-connector" configured
    deploymentconfig "ncp-cmdb-granite-connector" configured
    service "ncp-cmdb-granite-connector" configured
    route "ncp-cmdb-granite-connector" configured
    Importing ncp-cmdb-granite-connector:2.4.6.0 image...
    All done
    ```

The connectors are now installed successfully.
[Home](../index.md)
