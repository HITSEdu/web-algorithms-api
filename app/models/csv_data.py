from pydantic import BaseModel


class CSVData(BaseModel):
    csv_text: str
    session_id: str
