# =============================================================================
# Original credit to Bernard Brenyah @ Medium 
# Edited by Ann-Marie Thompson
# 
# =============================================================================
# import needed modules
import quandl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# get adjusted closing prices of x-amount of selected companies with Quandl
# currently limited by demo API
quandl.ApiConfig.api_key = 'DxVkJosWFu3XYgo1sCso'
selected = ['AAPL', 'WMT', 'GE', 'TSLA', 'ATVI','AMD','NVDA', 'LMT','INTC','KR','CBS','WFC','PNC','DUK','BLK']
data = quandl.get_table('WIKI/PRICES', ticker = selected,
                        qopts = { 'columns': ['date', 'ticker', 'adj_close'] },
                        date = { 'gte': '2014-01-01', 'lte': '2018-09-09' }, paginate=True)

# reorganise data pulled by setting date as index with
# columns of tickers and their corresponding adjusted prices
clean = data.set_index('date')
table = clean.pivot(columns='ticker')

# calculate daily and annual returns of the stocks
returns_daily = table.pct_change()
returns_annual = returns_daily.mean() * 250

# get daily and covariance of returns of the stock
cov_daily = returns_daily.cov()
cov_annual = cov_daily * 250

# empty lists to store returns, volatility and weights of imiginary portfolios
port_returns = []
port_volatility = []
sharpe_ratio = []
stock_weights = []

# set the number of combinations for imaginary portfolios
num_assets = len(selected)
num_portfolios = 50000

#set random seed for reproduction's sake
np.random.seed(101)

# populate the empty lists with each portfolio's wieghts, returns and risks
for single_portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = np.dot(weights, returns_annual)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
    sharpe = returns / volatility
    sharpe_ratio.append(sharpe)
    port_returns.append(returns)
    port_volatility.append(volatility)
    stock_weights.append(weights)

# a dictionary for Returns and Risk values of each portfolio
portfolio = {'Returns': port_returns,
             'Volatility': port_volatility,
             'Sharpe Ratio': sharpe_ratio}

# extend original dictionary to accomodate each ticker and weight in the portfolio
for counter,symbol in enumerate(selected):
    portfolio[symbol+' Weight'] = [Weight[counter] for Weight in stock_weights]

# make a nice dataframe of the extended dictionary
df = pd.DataFrame(portfolio)

# get better labels for desired arrangement of columns
column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' Weight' for stock in selected]

# reorder dataframe columns
df = df[column_order]        

# plot frontier, max sharpe & min Volatility values with a scatterplot
plt.style.use('seaborn-dark')
df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
plt.show()

# =============================================================================
# Extra stuff
# =============================================================================

# find min Volatility & max sharpe values in the dataframe (df)
min_volatility = df['Volatility'].min()
max_sharpe = df['Sharpe Ratio'].max()
max_return = df['Returns'].max()
min_return = df['Returns'].min()

# use the min, max values to locate and create the two special portfolios
print("Optimal Portfolio")
sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
print(sharpe_portfolio.T)
print("\nMinimum Variance Portfolio")
min_variance_port = df.loc[df['Volatility'] == min_volatility]
print(min_variance_port.T)
print("\nMaximum Return Portfolio")
max_return_port = df.loc[df['Returns'] == max_return]
print(max_return_port.T)
print("\nMinimum Return Portfolio")
min_return_port = df.loc[df['Returns'] == min_return]
print(min_return_port.T)

# plot frontier, max sharpe & min Volatility values with a scatterplot
plt.style.use('seaborn-dark')
df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', marker='D', s=200)
plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='blue', marker='D', s=200 )
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
plt.show()

# initialize counters and new lists
# =============================================================================
# port_return_test = []
# port_sharpe_test = []
# count1 = -1 
# count2 = -1
# =============================================================================

# Comb through port_returns and sharpe_ratio lists looking for specific portfolios
# =============================================================================
# for i in port_returns:
#     count1 += 1
#     if i > .25: # Finds all portfolios with a return greater than variable
#         port_return_test.append(i)
# for i in sharpe_ratio:
#     count2 += 1
#     if i > 1.0: # Finds all portfolios with a sharpe ratio greater than variable
#         port_sharpe_test.append(i) 
# =============================================================================