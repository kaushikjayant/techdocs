[Home](../index.md)
# Getting FaultShield Filters in Service Designer

Get FaultShield filters in the Service Designer UI as follows:

- Open the Service Designer UI and check if Alarm Filters are present.
- If Alarm Filters are not present, open Kibana and go to **Dev Tools**.
- Execute the following script in Elasticsearch:

  ```
  POST servicedesigner/alarmfilter/_update_by_query
  {
    "script": {
      "lang": "painless",
      "inline": "if (ctx._source.sourceType == null){ ctx._source.put('sourceType', 'FM'); ctx._source.pto.put('sourceType', 'FM'); }"
    }
  }
  ```
  
- Now, recheck Alarm Filters in Elasticsearch.

[Home](../index.md)
