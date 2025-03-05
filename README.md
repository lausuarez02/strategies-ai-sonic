# Cult of Ronin: AI Agent Repo (strategies-ai)

This repository is responsible for optimizing strategy execution dynamically using AI, predicting the best yield farming moves, performing risk analysis, and utilizing ZK (Zero-Knowledge) computations for privacy. The AI agent leverages [Allora Network](https://allora.network) for decentralized AI predictions and other techniques to automate and improve the decision-making process for DeFi strategies.

## Overview

Key functionalities of this repo include:
- **Dynamic strategy optimization**: AI optimizes strategy execution based on market conditions using Allora Network's price predictions.
- **Yield farming prediction**: AI-based prediction for identifying the best yield farming opportunities.
- **Risk analysis & alerts**: Using Allora's topic-based inferences to assess risks such as impermanent loss, liquidation risks, and more.
- **ZK computations**: Implementing ZK-proof logic for privacy-sensitive strategies (e.g., Noir/Aztec).

## Folder Structure

```plaintext
📂 strategies-ai/
├── 📂 notebooks/
│ ├── strategy_backtesting.ipynb  # Tests AI strategies on past data
├── 📂 zk/                        # If using Noir/Aztec for ZK privacy
│ ├── private_farming.noir        # ZK-proof logic for strategy privacy
├── main.py                   # Main AI execution agent using Allora Network
├── README.md                     # Project documentation
```

### `notebooks/`

- **strategy_backtesting.ipynb**: A Jupyter notebook to backtest the AI strategies on historical data.

### `zk/`

- **private_farming.noir**: ZK-proof logic to ensure privacy during strategy execution.

### `ai_agent.py`

- This is the main AI execution agent that dynamically optimizes strategy execution using Allora Network's predictions and risk analysis capabilities, along with Zero-Knowledge computations for privacy when needed.

## Installation

Clone this repository and install dependencies using the following commands:

```bash
git clone https://github.com/lausuarez02/strategies-ai-sonic.git
cd strategies-ai-sonic
pip install -r requirements.txt
```

## Configuration

You'll need to set up your Allora Network API key. Create a `.env` file with:

```env
ALLORA_API_KEY=your_api_key_here
ALLORA_CHAIN=testnet  # or mainnet for production
```

## Usage

### Running the AI Agent

To run the AI execution agent:

```bash
python ai_agent.py
```

This will trigger the AI agent to start optimizing strategies using Allora Network's predictions.

### Backtesting AI Strategies

To backtest the strategies on historical data, run:

```bash
jupyter notebook notebooks/strategy_backtesting.ipynb
```

### Privacy-Preserving Strategy

To utilize the ZK-based private farming strategy, run:

```bash
python zk/private_farming.noir
```

## Dependencies

Make sure to install all required libraries:

```bash
pip install -r requirements.txt
```

Key dependencies include:
- `allora-sdk`: For accessing Allora Network's AI predictions and insights
- `pandas`: For data handling
- `python-dotenv`: For environment variable management
- `asyncio`: For asynchronous operations
- `pycryptodome`: For Zero-Knowledge computations

## Contributing

Feel free to fork this repository and submit pull requests. If you find a bug or want to suggest a feature, open an issue, and I'll review it.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
