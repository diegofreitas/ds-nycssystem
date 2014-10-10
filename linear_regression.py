from r_squared import compute_r_squared

__author__ = 'diego.freitas'
import numpy as np
import pandas
import ggplot as gp
from datetime import datetime
import r_squared

def get_day_week(date):
    return datetime.strptime(date,'%Y-%m-%d').date().isoweekday()

def normalize_features(array):
   """
   Normalize the features in the data set.
   """
   array_normalized = (array-array.mean())/array.std()
   mu = array.mean()
   sigma = array.std()

   return array_normalized, mu, sigma

def compute_cost(features, values, theta):
    """
    Compute the cost function given a set of features / values,
    and the values for our thetas.

    This can be the same code as the compute_cost function in the lesson #3 exercises,
    but feel free to implement your own.
    """

    m = len(values)
    sum_of_square_errors = np.square(np.dot(features, theta) - values).sum()
    cost = sum_of_square_errors / (2*m)

    return cost

def gradient_descent(features, values, theta, alpha, num_iterations):
    """
    Perform gradient descent given a data set with an arbitrary number of features.

    This can be the same gradient descent code as in the lesson #3 exercises,
    but feel free to implement your own.
    """

    m = len(values)
    cost_history = []

    for i in range(num_iterations):
       theta = theta - (alpha/m) * np.dot(np.dot(features,theta) - values ,features)
       cost_history.append(compute_cost(features, values, theta))
    return theta, pandas.Series(cost_history)

def predictions(dataframe):
    '''
    The NYC turnstile data is stored in a pandas dataframe called weather_turnstile.
    Using the information stored in the dataframe, let's predict the ridership of
    the NYC subway using linear regression with gradient descent.

    You can see the information contained in the turnstile weather dataframe here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

    Your prediction should have a R^2 value of 0.40 or better.

    Note: Due to the memory and CPU limitation of our Amazon EC2 instance, we will
    give you a random subet (~15%) of the data contained in
    turnstile_data_master_with_weather.csv

    If you'd like to view a plot of your cost history, uncomment the call to
    plot_cost_history below. The slowdown from plotting is significant, so if you
    are timing out, the first thing to do is to comment out the plot command again.

    If you receive a "server has encountered an error" message, that means you are
    hitting the 30-second limit that's placed on running your program. Try using a
    smaller number for num_iterations if that's the case.

    If you are using your own algorithm/models, see if you can optimize your code so
    that it runs faster.
    '''
    dataframe['weekday'] = dataframe.DATEn.apply(get_day_week)

    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    #features = dataframe[['rain', 'Hour', 'weekday']].join(dummy_units)#   ''', 'Hour', 'meantempi' '''
    features = dataframe[['rain', 'Hour', 'meantempi', 'weekday']].join(dummy_units)

    values = dataframe[['ENTRIESn_hourly']]
    m = len(values)

    features, mu, sigma = normalize_features(features)
    features['ones'] = np.ones(m)

    features_array = np.array(features)
    values_array = np.array(values).flatten()

    #Set values for alpha, number of iterations.
    alpha = 0.1# please feel free to change this value
    num_iterations = 200 # please feel free to change this value

    #Initialize theta, perform gradient descent
    theta_gradient_descent = np.zeros(len(features.columns))
    theta_gradient_descent, cost_history = gradient_descent(features_array,
                                                            values_array,
                                                            theta_gradient_descent,
                                                            alpha,
                                                            num_iterations)
    predictions = np.dot(features_array, theta_gradient_descent)
    plot = None
    # -------------------------------------------------
    # Uncomment the next line to see your cost history
    # -------------------------------------------------
    plot = plot_cost_history(alpha,cost_history)
    #
    # Please note, there is a possibility that plotting
    # this in addition to your calculation will exceed
    # the 30 second limit on the compute servers.


    return values_array, predictions, plot, theta_gradient_descent


def plot_cost_history(alpha, cost_history):
   """This function is for viewing the plot of your cost history.
   You can run it by uncommenting this

       plot_cost_history(alpha, cost_history)

   call in predictions.

   If you want to run this locally, you should print the return value
   from this function.
   """
   cost_df = pandas.DataFrame({
      'Cost_History': cost_history,
      'Iteration': range(len(cost_history))
   })
   return gp.ggplot(cost_df, gp.aes('Iteration', 'Cost_History')) + \
      gp.geom_point() + gp.geom_line() + gp.ggtitle('Cost History for alpha = %.3f' % alpha )


real_results, predictions, plot, theta_gradient_descent = predictions(pandas.read_csv('turnstile_data_master_with_weather_part.csv', low_memory=False))

#print(plot)
print(theta_gradient_descent[0:4])
print(compute_r_squared(real_results, predictions))


