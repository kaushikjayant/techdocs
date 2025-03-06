# Configuring Environment Variables 

After installing a component template, you may need to modify environment variables to ensure proper functionality in the target environment. The configuration is stored in template (YAML) files deployed in the environment. To update configuration settings for a component, you must modify the corresponding YAML file and redeploy it.

## Generic Procedure for Configuration Changes

1. **Open the Relevant YAML File**  
   - Navigate to the corresponding deployment repository and open the required YAML file.  
   - For example, to modify the CMDB Bridge configuration, open the `top-ncp-pa-cmdb-bridge.yaml` file from the `ncp-pulseassure` repository.

2. **Locate the Environment Variable**  
   - In the YAML file, find the `env:` section.  
   - Identify the variable to be modified. For instance, updating the following entry changes the `VENDOR_NAME` setting:
     
     ```yaml
     name: VENDOR_NAME
     value: BRIDGON
     ```

3. **Save and Close the File**

4. **Redeploy the Template**

