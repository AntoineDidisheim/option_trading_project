# option_trading_project

## Data
* Download and clean option data
* Keep only stock with a large market cap
* Merge option data, with stock data --> we need to compare the option to the stock to measure returns
* Efficient data-loading (pickle)

## Portfolio class
* Cash invested
* Options held
* Trading decisions (buy sell)
* Free cash management 

## Performance measure
* Returns 
* Sharp-ratio 
* alphas <- factor regression and keep the alpha
r = alpha + beta_1*mkt + beta_2 * mom + beta_3 HmL +... 

## Trading strategies
* Define and pre-process/code some features/predictors
* Use some ML model to make prediciton about stock --> trade on those signals
a) signals about the mean direciton fo the stock, b) signals about specific part of the distributions of asset.
b) use ML to define an option-pricing model which is going to price the whole cross section and we buy whatever the algorithm deems underated. 


