from fastapi import FastAPI, HTTPException
from services import prediction_service
from datetime import datetime, timedelta
from pydantic import BaseModel
from datetime import date
from typing import List

#
class PredictionRequest(BaseModel):
    symbols: List[str]
    start_date: date
    end_date: date

app = FastAPI()


@app.post("/get-bias")
def read_predictions(request_data: PredictionRequest):
    """
    Fetches and returns predictions for a list of symbols within a specified date range.

    This endpoint accepts POST requests with a JSON body containing a list of symbol names
    ('symbols'), a start date ('start_date'), and an end date ('end_date'). It queries the
    prediction service for predictions of these symbols within the given date range. If predictions
    are found, they are returned in a specified format; if no predictions are found, a 404 HTTP
    exception is raised with a message indicating that predictions were not found.

    Parameters:
    - request_data (PredictionRequest): A Pydantic model that includes 'symbols' (List[str]),
      'start_date' (date), and 'end_date' (date).

    Returns:
    - dict: Predictions for the specified symbols and date range in the requested format.

    Raises:
    - HTTPException: If no predictions are found for the specified symbols within the date range.
    """
    predictions = prediction_service.get_predictions_by_symbol_and_date(
        symbols=request_data.symbols,
        start_date=request_data.start_date.isoformat(),
        end_date=request_data.end_date.isoformat()
    )
    if predictions:
        return predictions
    raise HTTPException(status_code=404, detail="Predictions not found")


@app.get("/get-daily-bias")
def read_predictions():
    """
    Fetches and returns predictions for the current day, or the most recent trading day if today
    is a weekend (Saturday or Sunday). This endpoint does not require any input parameters and
    automatically determines the appropriate date to query predictions for: today's date, or
    the date of the last Friday if today is Saturday or Sunday.

    The function queries the prediction service for predictions of all available symbols for
    the determined date. If predictions are found, they are returned in JSON format; if no
    predictions are found, a 404 HTTP exception is raised with a message indicating that
    predictions were not found.

    Returns:
    - dict: Predictions for the determined date in JSON format.

    Raises:
    - HTTPException: If no predictions are found for the determined date.
    """
    predictions = prediction_service.get_latest_predictions(result_format="json")

    if predictions:
        return predictions
    raise HTTPException(status_code=404, detail="Predictions not found")


@app.get("/")
def hello_world():
    return "Hello World!"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)