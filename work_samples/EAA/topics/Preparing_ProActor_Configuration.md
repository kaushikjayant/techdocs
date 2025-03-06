[Home](../index.md)
# Preparing Configuration 

## Target  
For a given product, ensure all customization is entered into configuration files and that all expected PVs are created.

## Steps  

### 1. Populate Configuration  
Run iterations of the deployment script in dry-run mode. Each time it fails due to a missing parameter, ensure that the parameter is added. For example:  

```sh
./deploy-synaptifix.sh --dryrun
```

### 2. Create PVs  
Once the deployment has successfully completed in dry-run mode, execute the following command to verify and create the required PVs:  

```sh
./ncp/shell/check-pvs.sh
```

[Home](../index.md)
