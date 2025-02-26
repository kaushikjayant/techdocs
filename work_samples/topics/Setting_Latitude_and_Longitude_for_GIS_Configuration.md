# Setting the Latitude and Longitude for GIS Configuration {#topic_gis_configuration}

Please note that ICM is not being used in ProAssure and the configuration is bit different.

-   The LAT-LON information for the NEs needs to be inserted using CMDB Generic Connector as a part of Inventory/Topology data. \(There is no enrichment, this is just an attribute\).
-   Map these attributes with the following Environment Variables in Deployment Config:
    -   The Attribute ID of LONGITUDE → GIS\_LOCATION\_X\_PI\_ID
    -   The Attribute ID of LATITUDE → GIS\_LOCATION\_Y\_PI\_ID
    -   Make sure that the LAT and LON attributes are mapped in mapped attributes table:

To check the PI ID of lat and long: *select \* from moc\_attribute\_def where name in \('LONGITUDE\(change this accordingly\)', 'LATITUDE\(change this accordingly\)'\);*

Confirm if the PIDs are mapped: select *\* from moc\_attribute\_def where idf\_mapped\_attribute in \(select id from mapped\_attribute where name like 'Location%'\);*

*--you should see the PI ID of latitude and longitude, in our case *100000015 and *100000016 were the PI IDs.***

*103 4 0 2 PositionY*

*102 3 0 2 PositionX*

*100000015 4 0 3 LATITUDE Created by Admin-Rest*

*100000016 3 0 3 LONGITUDE Created by Admin-Rest*

If not update the table:

Update moc\_attribute\_def set idf\_mapped\_attribute = 3 where id = 100000016;

Update moc\_attribute\_def set idf\_mapped\_attribute = 4 where id = 100000015;

-   Add the Anchored MOC to the site config file.

    **Note:** The KPI that are used for the LATITUDE and LONGITUDE were of TEXT data type \(STRING\) hence getting some issues while converting into NUMBER since GIS coordinates are always in numeric.

    ![](Display_attribute_lognitude.png "Display Attribute Longitude")


We created one more KPI on top of it to convert TEXT to NUMBER and now we are getting valid GIS coordinates.

**Note:** If we can correct the data type of existing KPI then there is no need for new ones.

**Existing KPI names**:

LATITUDE and LONGITUDE \(TEXT data type\)

**New KPI names**:

PositionX and PositionY \(NUMBER data type\)

![](calculations.png "New KPI Names")

These new KPI are created by below formula:

positionX = Str2Float\(!LONGITUDE!\[NE,Time\]\)

positionY = Str2Float\(!LATITUDE!\[NE,Time\]\)

![](Metric_Position.png "Metric Position")

![](Metric_Position1.png "Metric Position")

The new KPI IDs has been used in gis-proassure DC for the below env parameters. web-reporter env file has been also updated with the below details:

GIS\_LOCATION\_X\_PI\_ID = 100001282

GIS\_LOCATION\_Y\_PI\_ID = 100001283

![](Metric_Position_Format.png "Metric Position Format")

![](Metric_Position_Y.png "Metric Position Y")

![](POD.png "POD")

**Note:** The properties which have more than one value in **site.yaml** file and separated by comma, should be separated as **\\,**. For example,

```
gis-wms-servers:
- OSM;http://129.206.228.72/cached/hillshade\,World;http://www2.demis.nl/wms/wms.asp
```

```
fm-sources: NetCool\,TMF524
```

```
tt-sources: BMC
```

**Parent topic:** [Configuring PrOptima](../topics/Configuring_PrOptima.md)

