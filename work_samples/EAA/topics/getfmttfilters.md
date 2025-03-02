# Getting FM/TT Filters in Service Designer {#topic_zsv_41n_v2b}

Get FM/ TT filters in Service Designer UI as follows:

-   Open Service Designer UI, and check if Alarm Filters are present.
-   If Alarm Filters are not present, open KIbana, and go to "Dev Tools.'
-   Execute following Script in elastic.

    ```
    POST servicedesigner/alarmfilter/_update_by_query
    {
    "script": {
    "lang": "painless",
    "inline": "if (ctx._source.sourceType == null){ ctx._source.put('sourceType', 'FM'); ctx._source.pto.put('sourceType', 'FM'); }"
    }
    }
     
    5. Now re-check AlarmFilters in Elastic
    ```


