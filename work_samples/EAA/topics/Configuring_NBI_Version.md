[Home](../index.md)
# Configuring NBI for PulseOptima

You can control the version of NetPulse PulseOptima Web Reporter and NetPulse PulseOptima NBI from the backend as follows:

1. Open the **ncp-pulseoptima-web-reporting-v6-netpulseassure.env** file.
2. Specify the NBI version and PulseOptima Web Reporter version.
3. Similarly, open the **ncp-pulseoptima-web-reporting-v6.env** file.
4. Specify the NBI version and PulseOptima Web Reporter version.

### Important Notes:
- If `NCP_PULSEOPTIMA_WEB_REPORTING_VERSION` is greater than **6.1.0**, then `NCP_PULSEOPTIMA_NBI_VERSION` should be **6.0**.
- Otherwise, `NCP_PULSEOPTIMA_NBI_VERSION` should be **1.5-ncp-12**.
- If these properties are missing from the property file, the default values will be:
  - `NCP_PULSEOPTIMA_NBI_VERSION = 1.5-ncp-12`
  - `NCP_PULSEOPTIMA_WEB_REPORTING_VERSION = 6.0`

**Parent topic:** [Configuring PulseOptima](../topics/Configuring_PulseOptima.md)  

[Home](../index.md)
