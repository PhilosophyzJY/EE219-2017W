import math
import csv
import pandas as pd
import pandasql
import numpy as np
from scipy import stats
from matplotlib import pylab
from sklearn import linear_model
from sklearn.datasets import load_boston
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import svm
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline


def LinearRegs(filename): # Linear Regression

	print "LINEAR REGRESSION\n"

	boston = pd.read_csv(filename)

	# Adding headers to the data
	headers = ['crim','zn','indus','chas','nox','rm','age','dis','rad','tax','ptratio','b','lstat','medv']
	boston.columns = headers

	x_vals = boston.drop('medv',axis = 1)
	y_vals = boston.medv

	lin = linear_model.LinearRegression()

	# Performing cross validation
	kf = KFold(n_splits=10)

	sub_rmse = 0

	for train_index, test_index in kf.split(x_vals):
		X_train, X_test = x_vals.values[train_index], x_vals.values[test_index]
		y_train, y_test = y_vals.values[train_index], y_vals.values[test_index]

		lin.fit(X_train,y_train)

		y_pred = lin.predict(X_test)[0:len(y_test)]
		rmse = math.sqrt(mean_squared_error(y_test,y_pred))
		sub_rmse = rmse + sub_rmse

	avg_rmse = sub_rmse / kf.n_splits

	print "Avg RMSE:", avg_rmse

	# Finding total RMSE
	lin2 = linear_model.LinearRegression()	
	lin2.fit(x_vals,y_vals)

	y_vals_total_pred = lin2.predict(x_vals)
	rmse_total = math.sqrt(mean_squared_error(y_vals,y_vals_total_pred))

	print "RMSE total is:",rmse_total

	linear_coeff = pd.DataFrame(zip(headers,lin2.coef_))
	print linear_coeff
		
	
def PolyRegs(filename): # Polynomial Regression

	print "POLYNOMIAL REGRESSION\n"

	boston = pd.read_csv(filename)

	# Adding names to columns
	headers = ['crim','zn','indus','chas','nox','rm','age','dis','rad','tax','ptratio','b','lstat','medv']
	boston.columns = headers

	x_vals = boston.drop('medv',axis = 1)
	y_vals = boston.medv

	for i in range(1,6): # Degree of 6 takes a few minutes to compute

		degree_spec = i # Specifying the polynomial degree

		poly = PolynomialFeatures(degree=degree_spec)

		kf = KFold(n_splits=10)

		sub_rmse_poly = 0

		for train_index, test_index in kf.split(x_vals):
			X_train, X_test = x_vals.values[train_index], x_vals.values[test_index]
			y_train, y_test = y_vals.values[train_index], y_vals.values[test_index]

			X_poly_train = poly.fit_transform(X_train)
			y_poly_pred = poly.fit_transform(X_test)

			polyReg = linear_model.LinearRegression()
			polyReg.fit(X_poly_train, y_train)

			y_pred = polyReg.predict(y_poly_pred)

			rmse_poly = math.sqrt(mean_squared_error(y_test,y_pred))

			sub_rmse_poly = sub_rmse_poly + rmse_poly 

		avg_rmse_poly = sub_rmse_poly / kf.n_splits

		print "Avg RMSE for Poly Regression of degree " + str(poly.degree) + " is " + str(avg_rmse_poly)

		# Finding total RMSE
		poly_tot = PolynomialFeatures(degree=degree_spec)

		x_vals_poly = poly_tot.fit_transform(x_vals)

		polyReg_tot = linear_model.LinearRegression()
		polyReg_tot.fit(x_vals_poly,y_vals)

		y_vals_poly_pred = polyReg_tot.predict(x_vals_poly)

		rmse_poly_tot = math.sqrt(mean_squared_error(y_vals,y_vals_poly_pred))

		print "RMSE total for Poly Regression of degree " + str(poly_tot.degree) + " is " + str(rmse_poly_tot)
		


def RidgeRegs(filename):

	print "RIDGE REGRESSION\n"

	boston = pd.read_csv(filename)

	# Adding names to columns
	headers = ['crim','zn','indus','chas','nox','rm','age','dis','rad','tax','ptratio','b','lstat','medv']
	boston.columns = headers

	x_vals = boston.drop('medv',axis = 1)
	y_vals = boston.medv

	# Used as comparator values solely, picked arbitrily high numbers
	optimal_alpha = 1000
	rmse_comp = 1000

	for p in [1,0.1,0.01,0.001]: 

		alpha_val = p # Selected alpha value for Ridge Regression 

		ridge = linear_model.Ridge(alpha = alpha_val)

		kf = KFold(n_splits=10)

		sub_rmse_ridge = 0

		for train_index, test_index in kf.split(x_vals):
			X_train, X_test = x_vals.values[train_index], x_vals.values[test_index]
			y_train, y_test = y_vals.values[train_index], y_vals.values[test_index]

			ridge.fit(X_train,y_train)

			y_pred = ridge.predict(X_test)
			
			rmse_ridge = math.sqrt(mean_squared_error(y_test,y_pred))
			sub_rmse_ridge = rmse_ridge + sub_rmse_ridge

		avg_rmse_ridge = sub_rmse_ridge / kf.n_splits

		# Finding optimal alpha according to Avg RMSE for 10 fold cross validation
		if avg_rmse_ridge < rmse_comp:
			optimal_alpha = ridge.alpha
			rmse_comp = avg_rmse_ridge

		print "Avg RMSE for Ridge Regression with alpha: " + str(ridge.alpha) + " is " + str(avg_rmse_ridge)

		# Total RMSE for Ridge Regression 

		ridge_tot = linear_model.Ridge(alpha = alpha_val)

		ridge_tot.fit(x_vals,y_vals)
		y_vals_ridge_pred = ridge_tot.predict(x_vals)

		rmse_ridge_tot = math.sqrt(mean_squared_error(y_vals,y_vals_ridge_pred))

		print "Total RMSE for Ride Regression with alpha: " + str(ridge_tot.alpha) + " is " +str(rmse_ridge_tot)
		print ""

	# Generating coefficients with optimal alpha value
	print "Optimal alpha value according to 10-fold cross validation is: " + str(optimal_alpha)
	print ""

	ridge_tot_optimal = linear_model.Ridge(alpha = optimal_alpha)

	ridge_tot_optimal.fit(x_vals,y_vals)
	y_vals_ridge_pred_optimal = ridge_tot_optimal.predict(x_vals)

	rmse_ridge_optimal = math.sqrt(mean_squared_error(y_vals,y_vals_ridge_pred_optimal))

	print "Total RMSE for Ride Regression with optimal alpha: " + str(ridge_tot_optimal.alpha) + " is " +str(rmse_ridge_optimal)
	print ""

	# Prints optimal coefficients 
	ridge_coeff = pd.DataFrame(zip(headers,ridge_tot_optimal.coef_))
	print ridge_coeff

def LassoRegs(filename):

	print "LASSO REGRESSION\n"

	boston = pd.read_csv(filename)

	# Adding names to columns
	headers = ['crim','zn','indus','chas','nox','rm','age','dis','rad','tax','ptratio','b','lstat','medv']
	boston.columns = headers

	x_vals = boston.drop('medv',axis = 1)
	y_vals = boston.medv

	# Used as comparator values solely, picked arbitrily high numbers
	optimal_alpha = 1000
	rmse_comp = 1000

	for i in [1,0.1,0.01,0.001]: # Running Lasso Regression across range of alphas

		alpha_val = i

		lasso = linear_model.Lasso(alpha = alpha_val)

		kf = KFold(n_splits=10)

		sub_rmse_lasso = 0

		for train_index, test_index in kf.split(x_vals):
			X_train, X_test = x_vals.values[train_index], x_vals.values[test_index]
			y_train, y_test = y_vals.values[train_index], y_vals.values[test_index]

			lasso.fit(X_train,y_train)

			y_pred = lasso.predict(X_test)

			# df_coeff = pd.DataFrame(zip(headers,lasso.coef_))
			# print df_coeff
			
			rmse_lasso = math.sqrt(mean_squared_error(y_test,y_pred))
			sub_rmse_lasso = rmse_lasso + sub_rmse_lasso

		avg_rmse_lasso = sub_rmse_lasso / kf.n_splits

		# Finding optimal alpha according to Avg RMSE for 10 fold cross validation
		if avg_rmse_lasso < rmse_comp:
			optimal_alpha = lasso.alpha
			rmse_comp = avg_rmse_lasso

		print "Avg RMSE for Lasso Regression with alpha: " + str(lasso.alpha) + " is " + str(avg_rmse_lasso)

		# Total RMSE for Lasso Regression

		lasso_tot = linear_model.Lasso(alpha = alpha_val)

		lasso_tot.fit(x_vals,y_vals)
		y_vals_lasso_pred = lasso_tot.predict(x_vals)

		rmse_lasso_tot = math.sqrt(mean_squared_error(y_vals,y_vals_lasso_pred))

		print "Total RMSE for Lasso Regression with alpha: " + str(lasso_tot.alpha) + " is " +str(rmse_lasso_tot)
		print " "

	# Generating coefficients with optimal alpha value
	print "Optimal alpha value according to 10-fold cross validation is: " + str(optimal_alpha)
	print ""

	lasso_tot_optimal = linear_model.Lasso(alpha = optimal_alpha)

	lasso_tot_optimal.fit(x_vals,y_vals)
	y_vals_lasso_pred_optimal = lasso_tot_optimal.predict(x_vals)

	rmse_lasso_optimal = math.sqrt(mean_squared_error(y_vals,y_vals_lasso_pred_optimal))

	print "Total RMSE for Lasso Regression with optimal alpha: " + str(lasso_tot_optimal.alpha) + " is " +str(rmse_lasso_optimal)
	print ""

	# To print optimal coefficients 
	lasso_coeff = pd.DataFrame(zip(headers,lasso_tot_optimal.coef_))
	print lasso_coeff

def RidgeVLassoVUnreg(filename):

	print "Optimal coefficients for Lasso Regression\n"
	LassoRegs(filename)

	print ""

	print "Optimal coefficients for Ridge Regression\n"
	RidgeRegs(filename)

	print ""

	print "Opitmal coefficents for unregularized model (alpha = 0, Linear Regression)\n"
	LinearRegs(filename)





def main():

	# Only un-comment and run ONE of the following lines at a time

	# LinearRegs('housing_data.csv') # Problem 4 
	# PolyRegs('housing_data.csv') # Problem 4
	# RidgeRegs('housing_data.csv') 
	# LassoRegs('housing_data.csv')
	RidgeVLassoVUnreg('housing_data.csv') # Run this for Problem 5
	


if __name__ == "__main__":
    main()
