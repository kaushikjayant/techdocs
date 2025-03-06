[Home](../index.md)

# Adding a New MOC to the GIS View in Web Client 

You can add a new MOC to the GIS view in the web client as follows:

- **Enrichment via CMDB Generic Connector**:  
  Enrich the MOC data along with its x, y coordinates.  
  
- **Verify Enrichment in NetPulseAssure Desktop Client**:  
  Ensure that the enrichment for the new MOC is complete and populates data correctly.  
  
- **Check MOC Availability in Database**:  
  Confirm that the new MOC is available in the `moc_def` table and note the ID.  
  
- **Update `GisCommon.site.properties`**:  
  Append the MOC ID in the GIS configuration file:  
  
  ```shell
  [bridgon@ncp-pulseoptima-nbi-mdds-netpulseassure-37-zks3x properties-site]$ cat GisCommon.site.properties

  NodeClass=100000199,100000225
  pulseoptima.EnableGIS=true
  NodeLayer.CoordSysId=4326
  #AnchoredNodeClass=5002;5001,2002;2001,12000021,16175003;16175024,90;91;100000199;100000225

  [bridgon@ncp-pulseoptima-nbi-mdds-netpulseassure-37-zks3x properties-site]
  ```

  **Note:** `AnchoredNodeClass` is used when a parent-child relationship exists. Separate values using a semicolon (`<child>;<parent>`).  


- **Restart Required Pods**:  
  Restart the following pods for changes to take effect:  
  - `gis-netpulseassure`
  - `interactive-mdds-netpulseassure`
  - `nbi-mdds-netpulseassure`

**Parent topic:** [Configuring PulseOptima](../topics/Configuring_PulseOptima.md)

[Home](../index.md)

