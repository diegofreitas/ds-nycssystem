
__author__ = 'diego.freitas'
import numpy as np
import pandas
import ggplot as gp
from datetime import datetime

import itertools

def compute_r_squared(data, predictions):
    mean = np.mean(data)
    r_squared = 1 - (np.sum(np.square(data-predictions)) /np.sum(np.square(data-mean)))

    return r_squared

def get_day_week(date):
    return datetime.strptime(date,'%Y-%m-%d').date().isoweekday()

def add_polynomial_features(df, degree, add_sqrt):
    for i in range(2, degree + 1):
        for combination in itertools.combinations_with_replacement(df.columns, i):
            name = " ".join(combination)
            value = np.prod(df[list(combination)], axis=1)
            df[name] = value
    if add_sqrt:
        for column in df.columns:
            df["%s_sqrt" % column] = np.sqrt(df[column])

def normalize_features(array):
   """
   Normalize the features in the data set.
   """
   array_normalized = (array-array.mean())/array.std()
   mu = array.mean()
   sigma = array.std()

   return array_normalized, mu, sigma

def compute_cost(features, values, theta):


    m = len(values)
    sum_of_square_errors = np.square(np.dot(features, theta) - values).sum()
    cost = sum_of_square_errors / (2*m)

    return cost

def gradient_descent(features, values, theta, alpha, num_iterations):


    m = len(values)
    cost_history = []

    for i in range(num_iterations):
       theta = theta - (alpha/m) * np.dot(np.dot(features,theta) - values ,features)
       cost_history.append(compute_cost(features, values, theta))
    return theta, pandas.Series(cost_history)

def predictions(dataframe):

    dataframe['weekday'] = dataframe.DATEn.apply(get_day_week)
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    #features = dataframe[['rain', 'Hour', 'weekday']].join(dummy_units)#   ''', 'Hour', 'meantempi' '''
    features = dataframe[[ 'Hour', 'meantempi', 'weekday']]
    #add_polynomial_features(features, 3, add_sqrt=False)
    features = features.join(dummy_units)

    values = dataframe[['ENTRIESn_hourly']]
    m = len(values)

    features, mu, sigma = normalize_features(features)
    features['ones'] = np.ones(m)

    features_array = np.array(features)
    values_array = np.array(values).flatten()

    #Set values for alpha, number of iterations.
    alpha = 0.1# please feel free to change this value
    num_iterations = 200 # please feel free to change this value

    print "Gradient descent"
    #Initialize theta, perform gradient descent
    theta_gradient_descent = np.zeros(len(features.columns))
    theta_gradient_descent, cost_history = gradient_descent(features_array,
                                                            values_array,
                                                            theta_gradient_descent,
                                                            alpha,
                                                            num_iterations)
    predictions = np.dot(features_array, theta_gradient_descent)
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

   cost_df = pandas.DataFrame({
      'Cost_History': cost_history,
      'Iteration': range(len(cost_history))
   })
   return gp.ggplot(cost_df, gp.aes('Iteration', 'Cost_History')) +\
          gp.geom_point() + gp.geom_line() + gp.ggtitle('Cost History for alpha = %.3f' % alpha )


real_results, predictions, plot, theta_gradient_descent = predictions(pandas.read_csv('turnstile_data_master_with_weather_part.csv', low_memory=False))


print(theta_gradient_descent[0:4])
print(compute_r_squared(real_results, predictions))


