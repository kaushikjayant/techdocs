# Configuring NBI for PrOptima {#NBI_versioning}

You can control the version of EAA PrOptima Web Reporter and EAA PrOptima NBI from backend as follows:

-   Open the **eaa-proptima-web-reporting-v6-proassure.env** file.
-   Mention the NBI version and PrOptima Web Reporter version.
-   Similarly, open the **eaa-proptima-web-reporting-v6.env** file.
-   Mention the NBI version and PrOptima Web Reporter version.

    **Note:** If EAA\_PROPTIMA\_WEB\_REPORTING\_VERSION is greater than **6.1.0**, then EAA\_PROPTIMA\_NBI\_VERSION is **6.0**, else EAA\_PROPTIMA\_NBI\_VERSION is **1.5-eaa-12**.

    **Note:** If these properties are missing from the property file then default value for EAA\_PROPTIMA\_NBI\_VERSION will be **1.5-eaa-12** and EAA\_PROPTIMA\_WEB\_REPORTING\_VERSION will be **6.0**.


**Parent topic:** [Configuring PrOptima](../topics/Configuring_PrOptima.md)

