# Configuring Environment Variables {#topic_f3g_lk4_h2b}

After installing a component template, you may need to modify some environment variables to make the different components work in the target environment. The configuration is saved in the template \(YAML\) files deployed in the target environment. For making changes to configuration settings for a component, you must make changes to the corresponding YAML file and redeploy it. The generic procedure to make any configuration change to a template is as follows:

-   Open the specific YAML file from the corresponding deployment repository. For example open the tpl-eaa-nx-history-viewer.yaml file from the eaa-netexpert repository if you need to make configuration changes to Alert History Viewer.
-   In the YAML file, locate the variable name to be changed in the env: section. For example, updating the value for the following property changes the ALERT\_SOURCE setting.

    ```
    name: ALERT_SOURCE
    value: NX-FM
    ```

-   Save and close the file.
-   Redeploy the template.

-   **[Customizing NetExpert Configuration](../EAA_FM_Topics/proassure_config.md)**  


