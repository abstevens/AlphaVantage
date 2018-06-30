# AlphaVantage
Created a Python program to graph stock data from Alpha Vantage

## Steps for use

1.	To be compatible with this projects service, you will need to have Python version 3.6 onwards and to also install two third-party packages; Matplotlib (2.2.2) and Pandas (0.23.1). The project will need the Python version and packages accessible within its environment.
2.	Install an integrated development environment (IDE) that is compatible with Python such as PyCharm or Spyder.
3.	Open the project in an IDE and run the interactive interpreter on the StockTimeSeriesData.py file.
4.	The program will display a user input option stating, “Enter stock symbols (comma separation)”. The user should input a stock symbol separated by commas such as AMZN (for Amazon), AAPL (for Apple), F (for Ford) etc. To be able to compare two stocks, a simple example would be for the user to input GE, F. Its recommended to input stocks that have relative pricings (can be selected on http://money.cnn.com/data/hotstocks/index.html) to be able to notice more detail. Once finished entering stock, hit the enter key to move onto the next step.
5.	The program then display which data set should be picked for graphing. By default, the first data set will be chosen unless specified. Once the users answer is typed, press enter to continue.
6.	A user input will display stating which time series to pick for graphing. By default, the program will pick the first option being within today’s trading. Once the answer is typed, press enter to continue. Any option picked apart from the first (within today’s trading), skip step 7.
7.	If the user selects within today’s trading as the time series to be graphed, the program will ask for an interval in minutes to be mentioned between two consecutive data points. Pick either of the options (1, 5, 15, 30 or 60) by typing the number directly and press enter to continue. The default is 1-minute interval.
8.	Once completed all above user inputs needed, the program will inform which stock has loaded and when the graph has been plotted. Depending on the IDE, a graph will be displayed showing the stock data specified from the user input.
9.	Another user input will be displayed asking “Would you like to search more stocks (y/n)?”, which there will be an expected user input of either “y” (yes) or “n” (no). If the user selects “y”, steps 4-8 will be repeated. If the user selects “n”, the service will terminate.
