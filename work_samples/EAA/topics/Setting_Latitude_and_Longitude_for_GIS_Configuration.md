[Home](../index.md)
# Setting the Latitude and Longitude for GIS Configuration

Please note that ICM is not being used in NetPulseAssure, and the configuration is slightly different.

- The LAT-LON information for the NEs needs to be inserted using CMDB Generic Connector as a part of Inventory/Topology data. (There is no enrichment, this is just an attribute.)
- Map these attributes with the following Environment Variables in Deployment Config:
  - The Attribute ID of LONGITUDE → `GIS_LOCATION_X_PI_ID`
  - The Attribute ID of LATITUDE → `GIS_LOCATION_Y_PI_ID`
  - Ensure that the LAT and LON attributes are mapped in the mapped attributes table:

To check the PI ID of latitude and longitude:
```sql
SELECT * FROM moc_attribute_def WHERE name IN ('LONGITUDE', 'LATITUDE');
```

Confirm if the PIDs are mapped:
```sql
SELECT * FROM moc_attribute_def WHERE idf_mapped_attribute IN (SELECT id FROM mapped_attribute WHERE name LIKE 'Location%');
```

You should see the PI ID of latitude and longitude. For example:

```
103  4  0  2  PositionY
102  3  0  2  PositionX
100000015  4  0  3  LATITUDE  Created by Admin-Rest
100000016  3  0  3  LONGITUDE  Created by Admin-Rest
```

If not, update the table:
```sql
UPDATE moc_attribute_def SET idf_mapped_attribute = 3 WHERE id = 100000016;
UPDATE moc_attribute_def SET idf_mapped_attribute = 4 WHERE id = 100000015;
```

- Add the Anchored MOC to the site config file.

**Note:** The KPIs used for LATITUDE and LONGITUDE were of TEXT data type (STRING), causing conversion issues. Since GIS coordinates are always numeric, a new KPI was created to convert TEXT to NUMBER, ensuring valid GIS coordinates.

**Existing KPI Names:**
- LATITUDE and LONGITUDE (TEXT data type)

**New KPI Names:**
- PositionX and PositionY (NUMBER data type)

These new KPIs were created using the following formula:
```text
positionX = Str2Float(!LONGITUDE![NE,Time])
positionY = Str2Float(!LATITUDE![NE,Time])
```

The new KPI IDs have been used in the gis-netpulseassure DC for the below environment parameters. The web-reporter environment file has also been updated:

```
GIS_LOCATION_X_PI_ID = 100001282
GIS_LOCATION_Y_PI_ID = 100001283
```

### Handling Multiple Values in site.yaml

Properties with multiple values in the **site.yaml** file, separated by a comma, should be formatted using `\,`.

**Example:**
```yaml
gis-wms-servers:
- OSM;http://129.206.228.72/cached/hillshade\,World;http://www2.demis.nl/wms/wms.asp

fm-sources: NetCool\,TMF524
tt-sources: BMC
```

**Parent Topic:** [Configuring PulseOptima](../topics/Configuring_PrOptima.md)

[Home](../index.md)

