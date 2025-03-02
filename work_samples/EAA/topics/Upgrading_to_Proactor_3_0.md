# Upgrading ProActor {#d0e2070}

If you are an existing customer of proactor, you can upgrade to the latest version. There are two scenarios in upgrading from an older version to the latest version.

1.  Upgrading from 2.0 VM to 3.0 Cloud
2.  Upgrading from 2.0 Cloud to 3.0 Cloud

    There will be some data lose from History and Actions tab if you move to a newer version.


**If you are upgrading from 2.0 VM to 3.0 Cloud, perform the following steps:**

-   Take backup of json file store.
-   Copy JSON file store from VM to cloud NFS in ProActor volume.
-   Install proactor 3.0 deployment script as:

    ```
    ./eaa-deploy/shell/deploy-proactor.sh --freshinstall
    ```

-   Now, run the migration script as:

    ```
    ./eaa-deploy/shell/deploy-proactor.sh --proceed
    ```


**If you are upgrading from 2.0 Cloud to 3.0 Cloud, perform the following steps:**

-   Take backup of json file store from proactor NFS volume.
-   Install proactor 3.0 deployment script as:

    ```
    ./eaa-deploy/shell/deploy-proactor.sh --freshinstall
    ```

-   Now, run the migration script as:

    ```
    ./eaa-deploy/shell/deploy-proactor.sh --proceed
    ```


**Note:** When you upgrading from an older version, start creating the autoflows only after migration script is run successfully.

