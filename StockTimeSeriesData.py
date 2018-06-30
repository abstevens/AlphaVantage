from matplotlib import pyplot as plt
import pandas as pd
import re


class StockTimeSeriesData:

    def __init__(self):
        # API from AlphaVantage: https://www.alphavantage.co/documentation/
        self.API_URL = 'https://www.alphavantage.co/query?'

        # Data sets returned from API into CSV
        self.columns_from_csv = {0: 'timestamp', 1: 'close', 2: 'open', 3: 'high', 4: 'low', 5: 'volume'}

        # Dictionary of standard API parameters used in all time series requests
        self.api_parameters = {'apikey': '6N29U4IWMPL7D8T8', 'datatype': 'csv'}

        # Create variable for stock symbols
        self.api_symbols = []

    def main(self) -> None:
        # Make stock symbols upper case and store
        symbols = input('Enter stock symbols (comma separation): ').upper()

        # Remove whitespaces from symbols and separate them into a list
        input_symbols = self.multiple_answers(symbols)

        data_set = '''\nData set options:\n
(1) Close - the last traded price for the period
(2) Open - the first traded price for the period
(3) High - the highest traded price for the period
(4) Low - the lowest traded price for the period
(5) Volume - the number of shares or contracts for the period\n
Enter a number corresponding to the data set (default is 1): '''

        # Options correlating to data set
        data_set_options = ['1', '2', '3', '4', '5']

        # Check if data set result match options
        data_set = self.multiple_choice_questions(data_set, data_set_options)

        # Store value of data sets
        x_axis_name = self.columns_from_csv.get(0)
        y_axis_name = self.columns_from_csv.get(int(data_set))

        time_series = '''\nTime series options:\n
(1) Within today's trading
(2) Daily trading
(3) Last trading day of each week
(4) Last trading day of each month\n
Enter a number corresponding to the time series (default is 1): '''

        # Options correlated to time series
        time_series_options = ['1', '2', '3', '4']

        # Check if time series result match options
        time_series = self.multiple_choice_questions(time_series, time_series_options)

        # Check what time series was selected and pass particular API parameters
        if time_series == '1':
            self.api_parameters.update(self.__set_parameters_for_intraday())
        elif time_series == '2':
            self.api_parameters.update(self.__set_parameters_for_daily())
        elif time_series == '3':
            self.api_parameters.update(self.__set_parameters_for_weekly())
        else:
            self.api_parameters.update(self.__set_parameters_for_monthly())

        # Get stock prices for particular time series and data set
        stock_data = self.__gather_stock_prices(input_symbols, x_axis_name, y_axis_name)

        if stock_data.empty:
            print('\nProgram failed to plot', ', '.join(input_symbols), '\n')
        else:
            # Graph the stock prices
            self.graph_and_show(stock_data, x_axis_name, y_axis_name)

        iterate_options = ['y', 'n']
        iterate = 'Would you like to search more stocks (y/n)? '

        # Check if iteration result matches options
        iterate = self.multiple_choice_questions(iterate, iterate_options)

        # Iterate again if user wants to
        if iterate == 'y':
            print()
            self.api_symbols = []
            self.main()
        else:
            print('\nThank you for using this service, trade responsibly!')

    def __set_parameters_for_intraday(self) -> dict:
        message_options = ['1', '5', '15', '30', '60']
        message = '\nEnter an interval in minutes (1, 5, 15, 30, 60) between two consecutive data points' \
                  ' (default is 1): '

        # Check if interval result matches options and add 'min' at end for API convention
        input_interval = self.multiple_choice_questions(message, message_options).__add__('min')

        # Extra parameters needed for intraday call
        extra_parameters = {'function': 'TIME_SERIES_INTRADAY', 'outputsize': 'compact', 'interval': input_interval}

        return extra_parameters

    @staticmethod
    def __set_parameters_for_daily() -> dict:
        # Extra parameters needed for daily call
        extra_parameters = {'function': 'TIME_SERIES_DAILY', 'outputsize': 'compact'}

        return extra_parameters

    @staticmethod
    def __set_parameters_for_weekly() -> dict:
        # Extra parameters needed for weekly call
        extra_parameters = {'function': 'TIME_SERIES_WEEKLY'}

        return extra_parameters

    @staticmethod
    def __set_parameters_for_monthly() -> dict:
        # Extra parameters needed for monthly call
        extra_parameters = {'function': 'TIME_SERIES_MONTHLY'}

        return extra_parameters

    def __gather_stock_prices(self, input_symbols: list, x_axis_name: str, y_axis_name: str) -> pd.DataFrame:
        # Columns to graph - timestamp on x axis and data_set chosen on y axis
        columns_to_graph = [x_axis_name, y_axis_name]

        gathered_data = []

        print('\nGathering stock information:\n')

        # For each stock chosen to graph
        for stock in input_symbols:
            # Add stock API parameter
            self.api_parameters.update({'symbol': stock})

            print(stock, 'STOCK LOADING...')

            # Make  URL query from constructed API parameters
            csv_download = self.make_api_url_query()

            # Read API return from Pandas module (third party) into DataFrame
            csv_data = pd.read_csv(csv_download)

            # try:
            # Filter DataFrame to only columns_to_graph
            data = csv_data.filter(items=columns_to_graph)

            # Convert timestamp column to datetime and replace as index for x axis
            if 'timestamp' in data:
                data.index = pd.to_datetime(data['timestamp'])
            else:
                print(stock, 'STOCK FAILED...')
                continue

            # Remove initial timestamp column
            del data['timestamp']

            """
            print('Data to be graphed for', stock + ':\n', data)
            """

            # Add stock data to list for graphing
            gathered_data.append(data)

            # Add stock symbol to instance variable
            self.api_symbols.append(stock)

        if len(gathered_data) == 0:
            # Return empty DataFrame
            return pd.DataFrame()
        else:
            # Merge with an inner join on columns of DataFrame(s) from stocks gathered
            return pd.concat(gathered_data, axis=1, join='inner')

    def graph_and_show(self, stock_data: pd.DataFrame, x_axis_name: str, y_axis_name: str) -> None:
        # Plot stock data using matplotlib and set legend to stocks chosen
        stock_data.plot().legend(self.api_symbols)

        # Set title of graph to readable time series function
        readable_title = self.api_parameters['function'].replace('_', ' ')

        # Configure matplotlib information and show
        plt.title(readable_title)
        plt.xlabel(x_axis_name.capitalize())
        plt.ylabel(y_axis_name.capitalize())
        plt.show()

        print('\nPlotted ' + readable_title.lower() + ' graph!\n')

    def make_api_url_query(self) -> str:
        # Construct URI query for request with API parameter keys and values
        api_uri_query = '&'.join("{!s}={!r}".format(key, val) for (key, val) in self.api_parameters.items())

        # Remove single quotes from URI
        api_uri_query = api_uri_query.replace('\'', '')

        # Return full URL to perform request
        return self.API_URL + api_uri_query

    @staticmethod
    def multiple_choice_questions(question: str, options: list, default_answer='1') -> str:
        string = None

        # Iterate message until answer matches options
        while string not in options:
            input_return = input(question)

            # If string is empty return default answer
            if not input_return:
                return default_answer

            # Regex pattern
            pattern = re.compile("\s+$")

            # Remove regex from string
            string = re.sub(pattern, '', input_return.replace(' ', ''))

        return string

    @staticmethod
    def multiple_answers(string: str) -> list:
        # Regex pattern
        pattern = re.compile("^\s+|\s*,\s*|\s+$")

        # Return removal of regex on string and split results by comma
        return [x for x in pattern.split(string.replace(' ', '')) if x]


# condition to only execute as script and not from use within other modules
if __name__ == "__main__":
    instance = StockTimeSeriesData()
    instance.main()
