import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
from anthropic import Anthropic
from supabase import create_client, Client

load_dotenv()

app = FastAPI(title="Finpilot Backend API")

# Setup API clients
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

supabase_url = os.getenv("SUPABASE_URL", "https://xyz.supabase.co")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "dummykey")
supabase: Client = create_client(supabase_url, supabase_key)

class LedgerRequest(BaseModel):
    account_id: str
    ledger_text: str

@app.get("/")
def home():
    return {"message": "Finpilot Backend is Running!"}

@app.post("/api/process-financials")
async def process_financials(data: LedgerRequest):
    try:
        # Phase 1: Gemini parses raw text into structured JSON data
        gemini_model = genai.GenerativeModel("gemini-1.5-pro")
        gemini_prompt = f"Parse this financial data into clean JSON format containing list of transactions, total income, and total expense:\n{data.ledger_text}"
        
        gemini_res = gemini_model.generate_content(
            gemini_prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        parsed_json = json.loads(gemini_res.text)

        # Phase 2: Claude runs deep anomaly detection & forecasting
        claude_prompt = f"""
        Analyze the following financial metrics.
        Identify unusual spending patterns (anomalies) and give a 1-sentence forecast.
        JSON output format:
        {{"anomalies": [{"item": "...", "reason": "...", "severity": "HIGH/MED/LOW"}], "forecast": "..."}}
        
        Data: {json.dumps(parsed_json)}
        """
        
        claude_res = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{"role": "user", "content": claude_prompt}]
        )
        analysis_result = json.loads(claude_res.content[0].text)

        # Phase 3: Push results to Supabase
        db_record = {
            "account_id": data.account_id,
            "raw_metrics": parsed_json,
            "anomalies": analysis_result.get("anomalies", []),
            "forecast": analysis_result.get("forecast", "")
        }
        db_response = supabase.table("finpilot_reports").insert(db_record).execute()

        return {"status": "success", "data": db_response.data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))