# Preparing Configuration {#topic_otj_jtl_3db}

Target: For a given product, ensure all customization is entered into configuration files and that all expected PVs are created.

-   Populate Configuration:

Run iterations of deployment script in dryrun, each time it fails with a missing parameter, ensure it is added eg:

```
./deploy-netexpert.sh --dryrun
```

-   Create PVs :

Once the deployment has been run successfully in dry-run mode, execute:

```
./eaa-deploy/shell/check-pvs.sh
```

