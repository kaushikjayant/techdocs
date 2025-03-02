# Adding a New MOC to the GIS View in Web Client {#topic_gis_configuration}

You can add a new MOC to the GIS view in web client as follows:

-   Enrichment to be done via cmdb generic connector for the MOC along with it's x, y co-ordinates.

    ![](Enrichment_Sample.png "Enrichment Sample")

-   Check if the Enrichment for the new MOC is done and is populating data in proassure desktop client.

    ![](Enrichment_of_New_MOC.png "Enrichment of New MOC")

-   Check if the new MOC is available in moc\_def table, also note the ID.

    ![](Moc_Def_Table.png "MOC Definition Table")

-   Append the ID in GisCommon.site.properties:

    \[mycom@eaa-proptima-nbi-mdds-proassure-37-zks3x properties-site\]$ cat GisCommon.site.properties

    NodeClass=100000199,100000225

    Proptima.EnableGIS=true

    NodeLayer.CoordSysId=4326

    \#AnchoredNodeClass=5002;5001,2002;2001,12000021,16175003;16175024,90;91;100000199;100000225

    \[mycom@eaa-proptima-nbi-mdds-proassure-37-zks3x properties-site\]

    **Note:** AnchoredNodeClass is generally used when you have a parent-child relationship present, it should be separated with semicolon in the form <child\>;<parent\>

    Sample GIS image between NodeB and FddCell given below.

    ![](Sample_GIS_Image.png "Sample GIS Image between NodeB and FddCell")

-   Restart gis-proassure, interactive-mdds-proassure and nbi-mdds-proassure pods.

**Parent topic:** [Configuring PrOptima](../topics/Configuring_PrOptima.md)

