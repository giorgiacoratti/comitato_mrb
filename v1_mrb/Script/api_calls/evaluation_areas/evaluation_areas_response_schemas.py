import sys
sys.path.insert(0, "../lib")
## Importo la posizione della libreria schema perché non la trova più in automatico... capire perché!
#sys.path.append(r"./Python311/Lib")
sys.path.append(r"C:\Program Files (x86)\SmartBear\TestComplete 15\Bin\Extensions\Python\Python311\Lib")

from schema import Schema, Or, Optional


"""
  Schema atteso gli interfaccia PATCH /v1/mrb/quarterly-reports/{reportId}/quarterly-details/{quarterlyDetailId}/areas/{areaId}/evaluate (TC0016)
  response body: EvaluationActionUpdateDto
"""
EvaluationActionUpdateDto = Schema(
  {
    "actionType": str,
    "status": str,
    "evaluated": bool,
    Optional("motivation"): str
  }
)


"""
  Schema atteso gli interfaccia GET /v1/mrb/quarterly-reports/{reportId}/quarterly-details/{quarterlyDetailId}/areas (TC0017)
  response body: ListResultEvaluationAreaDto
"""
ListResultEvaluationAreaDto = Schema(
  {
    Optional("data"): [
      {
        "id": int,
        "area": str,
        "areaName": str
      }
    ],
    Optional("total"): int
  }
)


"""
  Schema atteso gli interfaccia GET /v1/mrb/quarterly-reports/{reportId}/quarterly-details/{quarterlyDetailId}/areas/{areaId} (TC0018)
  response body: EvaluationAreaDetailDto
"""
EvaluationAreaDetailDto = Schema(
  {
    "id": int,
    "quarterlyDetailId": int,
    "area": {
      "id": int,
      "area": str,
      "areaName": str
    },
    "actions": [
      {
        "actionType": str,
        "requested": bool,
        "description": Or(None, str),
        Optional("status"): Or(None, str),
        Optional("evaluation"): Or(None, str, bool),
        Optional("motivation"): Or(None, str)
      }
    ],
    "elements": [
      {
        "id": int,
        "areaId": int,
        "name": str,
        "status": Or(None, str),
        Optional("motivation"): Or(None, str),
        "previousQuarterFields": [
          {
            "id": int,
            "name": Or(None, str),      
            "type": str,
            Optional("value"): Or(dict, None, str),
            Optional("selectOptions"): [
              {
                "value": Or(dict, str),
                "label": str
              }
            ]
          }
        ],
        "currentQuarterFields": [
          {
            "id": int,
            "name": Or(None, str),
            "type": str,
            Optional("value"): Or(dict, None, str),
            Optional("selectOptions"): [
              {
                "value": str,
                "label": str
              }
            ]
          }
        ]
      }
    ]
  }
)
