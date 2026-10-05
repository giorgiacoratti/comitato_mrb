import sys
sys.path.insert(0, "../lib")
## Importo la posizione della libreria schema perché non la trova più in automatico... capire perché!
#sys.path.append(r"./Python311/Lib")
sys.path.append(r"C:\Program Files (x86)\SmartBear\TestComplete 15\Bin\Extensions\Python\Python311\Lib")

from schema import Schema, Or, Optional


"""
  Schema atteso gli interfaccia GET /v1/mrb/evaluation-areas-config/areas (TC0001)
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