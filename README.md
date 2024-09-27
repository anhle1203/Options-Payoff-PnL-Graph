# Options Payoff Visualizer

## Overview
The Options Payoff Visualizer is a Python-based tool developed with Streamlit that provides a graphical representation of various options trading strategies and their potential outcomes. This application is designed to help traders and investors understand the potential payoffs and risks associated with different options strategies in a clear and interactive manner.

## Features
- **Visual Representation**: See the payoff diagrams for various options strategies.
- **Strategy Insights**: Access detailed information about each strategy including risks, rewards, and breakeven points.
- **Interactive Interface**: Adjust parameters like strike price, premium, and spot price to see how the payoffs change.

## Installation

To set up the Options Payoff Visualizer, follow these steps:

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/anhle1203/Payoff-Diagram-Visualizer.git 
   ```
2. Navigate to the project directory:
   ```bash
   cd options-payoff-visualizer
   ```
3. Install the required Python packages
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command in the project's root directory 

   ```bash
   streamlit run app/app.py
   ```

## Supported Strategies

This tool supports a wide array of option strategies ranging form Basic to Advanced, including but not limited to: 

- Long/Short Calls
- Long/Short Puts
- Straddles
- Butterflies
- Strangles
- Condors

For each strategy, you can adjust various parameters and view the resulting payoff diagram to undersatnd potential outcomes.

## Project Structure
```bash
options-payoff-visualizer/
│
├── app/               
│   ├── app.py         # Streamlit app
│   └── media/         
│
├── src/           
│   ├── option_strategies.py  # Logic implementation
│   └── strategies_info.json  # Metadata and description of options strategies
│
├── README.md          # Project documentation
├── requirements.txt   # Required dependencies
└── .gitignore         
```


## Contributing

Contributions are absolutely welcome! If you have improvements or new features in mind, feel free to fork the repository, make your changes, and submit a pull request.



## ___Disclaimer___:

This tool is intended for educational and informational purposes __only__ and should not be considered as financial advice.

