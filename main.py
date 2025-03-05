import os
from dotenv import load_dotenv
import pandas as pd
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from allora_sdk.v2.api_client import AlloraAPIClient as AlloraClient, PriceInferenceToken, PriceInferenceTimeframe

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Allora Strategy API",
    description="AI Strategy signals using Allora Network predictions",
    version="1.0.0"
)

# Input data model
class MarketData(BaseModel):
    market_volatility: float
    trading_volume: float
    timestamp: str

class AIAgent:
    def __init__(self, chain=None, api_key=None):
        # Get configuration from environment variables
        self.chain = chain or os.getenv("ALLORA_CHAIN", "testnet")
        self.api_key = api_key or os.getenv("ALLORA_API_KEY")
        
        if not self.api_key:
            raise ValueError("ALLORA_API_KEY must be set in environment variables")

        self.client = AlloraClient(
            chain_slug=self.chain,
            api_key=self.api_key
        )
        self.scaler = StandardScaler()

    async def predict_yield(self):
        btc_inference = await self.client.get_price_inference(
            asset=PriceInferenceToken.BTC,
            timeframe=PriceInferenceTimeframe.EIGHT_HOURS
        )
        eth_inference = await self.client.get_price_inference(
            asset=PriceInferenceToken.ETH,
            timeframe=PriceInferenceTimeframe.EIGHT_HOURS
        )
        
        # Access the normalized values using proper object attributes
        btc_norm = float(btc_inference.inference_data.network_inference_normalized)
        eth_norm = float(eth_inference.inference_data.network_inference_normalized)
        
        return {
            "btc_prediction": {
                "price": btc_inference.inference_data.network_inference,
                "normalized": btc_inference.inference_data.network_inference_normalized,
                "confidence": btc_inference.inference_data.confidence_interval_percentiles
            },
            "eth_prediction": {
                "price": eth_inference.inference_data.network_inference,
                "normalized": eth_inference.inference_data.network_inference_normalized,
                "confidence": eth_inference.inference_data.confidence_interval_percentiles
            },
            "yield_score": (btc_norm + eth_norm) / 200000  # Normalized to 0-1 range
        }

    async def analyze_risk(self):
        try:
            topics = await self.client.get_all_topics()
            risk_factors = []
            
            for topic in topics:
                # Access AlloraTopic properties directly
                if hasattr(topic, 'topic_name') and 'risk' in topic.topic_name.lower():
                    inference = await self.client.get_inference_by_topic_id(topic.topic_id)
                    risk_factors.append(inference)
            
            # Calculate risk score based on available data
            risk_score = 0.5  # Default risk score
            if risk_factors:
                # Adjust this calculation based on the actual inference data structure
                risk_score = len(risk_factors) / 10  # Simple example
            
            return {
                "risk_factors": risk_factors,
                "risk_score": risk_score
            }
        except Exception as e:
            print(f"Error in risk analysis: {e}")
            return {"error": str(e), "risk_score": 1}

    async def get_strategy_signals(self):
        try:
            # Get predictions and risk analysis in parallel
            yield_data, risk_data = await asyncio.gather(
                self.predict_yield(),
                self.analyze_risk()
            )

            return {
                "timestamp": datetime.now(),
                "yield_data": yield_data,
                "risk_data": risk_data,
                "signals": {
                    "high_yield": yield_data["yield_score"] > 0.1,
                    "low_risk": risk_data["risk_score"] < 0.5
                }
            }
        except Exception as e:
            print(f"Strategy signal error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

# Initialize the agent using environment variables
try:
    agent = AIAgent()
except ValueError as e:
    print(f"Error initializing AIAgent: {e}")
    raise

@app.get("/")
async def root():
    return {
        "status": "online", 
        "service": "Allora Strategy API",
        "chain": agent.chain
    }

@app.post("/strategy/signals")
async def get_signals():
    try:
        signals = await agent.get_strategy_signals()
        return signals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    try:
        # Simple health check of Allora connection
        topics = agent.client.get_all_topics()
        return {"status": "healthy", "allora_connected": True}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
