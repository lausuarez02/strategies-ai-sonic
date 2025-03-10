# Shogun: AI Agent Repo (strategies-ai)

This repository is responsible for optimizing strategy execution dynamically using AI, predicting the best yield farming moves, and performing risk analysis. The AI agent leverages [Allora Network](https://allora.network) for decentralized AI predictions to provide signals for DeFi strategies.

## Overview

This repo serves as a prediction and signal provider:
- **Dynamic strategy optimization**: AI optimizes strategy signals based on market conditions using Allora Network's price predictions
- **Yield farming prediction**: AI-based prediction for identifying the best yield farming opportunities
- **Risk analysis & alerts**: Using Allora's topic-based inferences to assess risks such as impermanent loss, liquidation risks, and more

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your configuration:
```env
ALLORA_API_KEY=your_api_key_here
ALLORA_CHAIN=testnet
API_PORT=8000
```

3. Start the API server:
```bash
uvicorn main:app --reload
```

## API Endpoints

- `GET /`: Health check and service info
- `GET /health`: Detailed health status of Allora connection
- `POST /strategy/signals`: Get strategy signals including:
  - Yield predictions for BTC and ETH
  - Risk analysis
  - Trading signals

## Example Usage

```bash
# Get strategy signals
curl -X POST http://localhost:8000/strategy/signals

# Check service health
curl http://localhost:8000/health
```

## Response Format

Strategy signals response example:
```json
{
    "timestamp": "2024-03-20T00:00:00Z",
    "yield_data": {
        "btc_prediction": {
            "price": "...",
            "normalized": "...",
            "confidence": "..."
        },
        "eth_prediction": {
            "price": "...",
            "normalized": "...",
            "confidence": "..."
        },
        "yield_score": 0.75
    },
    "risk_data": {
        "risk_factors": [],
        "risk_score": 0.3
    },
    "signals": {
        "high_yield": true,
        "low_risk": true
    }
}
```

## Architecture

This service acts as a prediction provider that:
1. Connects to Allora Network for AI predictions
2. Processes and normalizes prediction data
3. Calculates risk scores
4. Provides clean signals via API endpoints
5. Can be consumed by other services for strategy execution

## Note

This repository only handles predictions and signals. For actual strategy execution and trading, please refer to the strategy execution repository.
