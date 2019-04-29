import numpy as np
from sklearn import linear_model

class MarketingCosts:

    # param marketing_expenditure list. Expenditure for each previous campaign.
    # param units_sold list. The number of units sold for each previous campaign.
    # param desired_units_sold int. Target number of units to sell in the new campaign.
    # returns float. Required amount of money to be invested.
    @staticmethod
    def desired_marketing_expenditure(marketing_expenditure, units_sold, desired_units_sold):
        reg=linear_model.LinearRegression()
        X=list(zip(marketing_expenditure[1:],units_sold[1:]))
        print(desired_units_sold)
        reg.fit(units_sold[1:],marketing_expenditure[1:])
        p=reg.predict(desired_units_sold)

        return p

#For example, with the parameters below the function should return 250000.0.
print(MarketingCosts.desired_marketing_expenditure(
    [300000, 200000, 400000, 300000, 100000],
    [60000, 50000, 90000, 80000, 30000],
    60000))
