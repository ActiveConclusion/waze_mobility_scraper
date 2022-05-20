import requests
import jmespath
import json
import pandas as pd

cookies = {
    "HSID": "Ax9j2Mbtm0o6B1Cr0",
    "SSID": "AeUwDKmTG0J0vrZCR",
    "SID": "IQgoIZ6czs_U8MalNh_DNNqNSg45aKmIBBIeQnva2ai49gJTmwH7k_yktzCY24QI-qrqGw.",
}
headers = {
    "x-rap-xsrf-token": "AH-ilETkIoHWLxqOVT0kw75awEBvx-AZyQ:1649521468702",
}

json_data = {
    "dataRequest": [
        {
            "requestContext": {
                "reportContext": {
                    "reportId": "fe8a3c7d-9303-4e70-8acb-4e042714fa76",
                    "pageId": "18291825",
                    "mode": 1,
                    "componentId": "cd-0hdhhii97b",
                    "displayType": "simple-table",
                },
            },
            "datasetSpec": {
                "dataset": [
                    {
                        "datasourceId": "aba71524-948e-4c23-a04c-3fd49961f785",
                        "revisionNumber": 0,
                        "parameterOverrides": [],
                    },
                ],
                "queryFields": [
                    {
                        "name": "qt_1hdhhii97b",
                        "datasetNs": "d0",
                        "tableNs": "t0",
                        "dataTransformation": {
                            "sourceFieldName": "_Date_",
                        },
                    },
                    {
                        "name": "qt_3hdhhii97b",
                        "datasetNs": "d0",
                        "tableNs": "t0",
                        "dataTransformation": {
                            "sourceFieldName": "_Geo_",
                        },
                    },
                    {
                        "name": "qt_2hdhhii97b",
                        "datasetNs": "d0",
                        "tableNs": "t0",
                        "dataTransformation": {
                            "sourceFieldName": "_dkm_percent_change_",
                            "aggregation": 1,
                            "outputGeoType": 0,
                        },
                    },
                ],
                "sortData": [
                    {
                        "sortColumn": {
                            "name": "qt_1hdhhii97b",
                            "datasetNs": "d0",
                            "tableNs": "t0",
                            "dataTransformation": {
                                "sourceFieldName": "_Date_",
                            },
                        },
                        "sortDir": 1,
                    },
                    {
                        "sortColumn": {
                            "name": "qt_2hdhhii97b",
                            "datasetNs": "d0",
                            "tableNs": "t0",
                            "dataTransformation": {
                                "sourceFieldName": "_dkm_percent_change_",
                                "aggregation": 1,
                            },
                        },
                        "sortDir": 0,
                    },
                ],
                "includeRowsCount": True,
                "relatedDimensionMask": {
                    "addDisplay": False,
                    "addUniqueId": False,
                    "addLatLong": False,
                },
                "paginateInfo": {
                    "startRow": 1,
                    "rowsCount": 100000,
                },
                "filters": [
                    {
                        "filterDefinition": {
                            "filterExpression": {
                                "include": True,
                                "conceptType": 0,
                                "concept": {
                                    "ns": "t0",
                                    "name": "qt_7dt8nli97b",
                                },
                                "filterConditionType": "GTE",
                                "stringValues": [
                                    "20200301",
                                ],
                                "numberValues": [],
                                "queryTimeTransformation": {
                                    "dataTransformation": {
                                        "sourceFieldName": "_Date_",
                                    },
                                },
                            },
                        },
                        "dataSubsetNs": {
                            "datasetNs": "d0",
                            "tableNs": "t0",
                            "contextNs": "c0",
                        },
                        "version": 3,
                    },
                    {
                        "filterDefinition": {
                            "filterExpression": {
                                "include": True,
                                "conceptType": 0,
                                "concept": {
                                    "ns": "t0",
                                    "name": "qt_cwkdcli97b",
                                },
                                "filterConditionType": "EQ",
                                "stringValues": [
                                    "Country",
                                ],
                                "numberValues": [],
                                "queryTimeTransformation": {
                                    "dataTransformation": {
                                        "sourceFieldName": "_geo_level_",
                                    },
                                },
                            },
                        },
                        "dataSubsetNs": {
                            "datasetNs": "d0",
                            "tableNs": "t0",
                            "contextNs": "c0",
                        },
                        "version": 3,
                    },
                ],
                "features": [],
                "dateRanges": [
                    {
                        "startDate": 20200301,
                        "endDate": 20300101,
                        "dataSubsetNs": {
                            "datasetNs": "d0",
                            "tableNs": "t0",
                            "contextNs": "c0",
                        },
                    },
                ],
                "contextNsCount": 1,
                "dateRangeDimensions": [
                    {
                        "name": "qt_1mv384bjnc",
                        "datasetNs": "d0",
                        "tableNs": "t0",
                        "dataTransformation": {
                            "sourceFieldName": "_Date_",
                        },
                    },
                ],
                "calculatedField": [],
                "needGeocoding": False,
                "geoFieldMask": [],
                "geoVertices": 100000,
            },
        },
    ],
}
dashboard_response = requests.get(
    "https://datastudio.google.com/u/0/reporting/fe8a3c7d-9303-4e70-8acb-4e042714fa76/page/bhuOB",
)
print(dashboard_response.headers)

response = requests.post(
    "https://datastudio.google.com/u/0/batchedDataV2",
    headers=headers,
    json=json_data,
    cookies=cookies,
)
body = response.text
body = body[4:]
json_data = json.loads(body)
j = "dataResponse[0].dataSubset[0].dataset.tableDataset.[column[0].stringColumn.values[], column[1].stringColumn.values[], column[2].doubleColumn.values[]]"
table = jmespath.search(j, json_data)
columns = ["Date", "Country", "% Change In Waze Driven Miles/KMs"]
data = {column: table[i] for i, column in enumerate(columns)}
df = pd.DataFrame(data)
df.to_excel("Waze_test.xlsx")
