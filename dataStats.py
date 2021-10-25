#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 18:27:36 2021

@author: William
"""

import pandas as pd 
diabetes = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Datasets/Diabetes/DB1_Diabetes/diabetic_data.csv')
diabetes

len(diabetes)
##Initial glance of dataframe: 
##Unique columns  = encounter_id
##Grouper = patient_nbr
##There are question marks for categoricals (weight); would replace the ? --> NaN or NULL 

diabetesSmall = diabetes.sample(100)

diabetes.info()
# Columns of interest: 
# time_in_hospital 
# num_lab_procedures 
# num_procedures (non lab) 
# num_medicaitons
# number_diagnoses 

import numpy as np
diabetes.replace('?', np.NaN)

##Create a new columnn of interest 

diabetes['totalCountProcedures'] = diabetes['num_procedures'] + diabetes['num_lab_procedures']
list(diabetes)


#################################################################################
################################## Question 1 ###################################
#################################################################################
####### Is there a correlation between time in hospital and the number of #######
#################################lab procedures? ################################
#################################################################################
######## Yes there is a correlation; it is somwhere between 0.32 and 0.34 #######
#################################################################################

timeInHospital = diabetes['time_in_hospital'] ### No more than 14 days were included ###
labProcedures = diabetes['num_lab_procedures'] ### 132 procedures within 14 days ### 

# Shapiro-Wilk Test - UNIVARIATE TEST / correlation 
from numpy.random import seed
from numpy.random import randn
from scipy.stats import shapiro
# seed the random number generator
seed (1)
# generate univariate observations
data = 5 * randn(100) + 50
# normality test
timeInHospital_stat, timeInHospital_p = shapiro(timeInHospital)
print('Statistics=%.3f, p=%.3f' % (timeInHospital_stat, timeInHospital_p))
# interpret
alpha = 0.05
if timeInHospital_p > alpha:
	print('Sample looks Gaussian (fail to reject H0)')
else:
	print('Sample does not look Gaussian (reject H0)')

labProcedures_stat, labProcedures_p = shapiro(labProcedures)
print('Statistics=%.3f, p=%.3f' % (labProcedures_stat, labProcedures_p))
# interpret
alpha = 0.05
if labProcedures_p > alpha:
	print('Sample looks Gaussian (fail to reject H0)')
else:
	print('Sample does not look Gaussian (reject H0)')
    
### PASSED NORMALCY ###
### Data is significant; rejected NULL hypothesis ###

from matplotlib import pyplot
# seed the random number generator
seed(1)
# generate univariate observations
data = 5 * randn(100) + 50
# histogram plot
pyplot.hist(timeInHospital) ### Right skewed ### 
pyplot.show()

pyplot.hist(labProcedures)
pyplot.show()

# histogram using pandas instead of pyplot
diabetes['time_in_hospital'].hist(bins=20)
diabetes['num_lab_procedures'].hist(bins=20)


############### HOMOGENEITY ###############
# Barlett's test is used to test if the groups, which can be referred to as k, have equal variances.
# Barlett's test can test for equality between 2 or more groups.
import scipy.stats as stats

stats.bartlett(timeInHospital, labProcedures) ### More ram efficient than the one below ####
stats.bartlett(diabetes['time_in_hospital'], diabetes['num_lab_procedures']) ### Yields the same results ^ p-value = 0.0, which is < 0.04 means the data is HETERO (failed HOMO test) =  reject the H0 ###

### Statistically significant for differences in residual variation BUT sharpiro PASSED ###
## Will perform pearson and spearman ### 

from scipy.stats import spearmanr, pearsonr

# Pearson r is in between -1 to +1 --> LINEAR relationship
# Spearson rho is bewteen -1 to +1 --> MONOTONIC relationship 

spearmancorrelation, spearmanp = spearmanr(timeInHospital, labProcedures)
pearsoncorrelation, pearsonp = pearsonr(timeInHospital, labProcedures)

scipyPearsonOutput = pd.DataFrame({'Correlation': pearsoncorrelation, 'PValue': pearsonp, 'CorrType': 'Pearson', 'From': 'SciPy'}, index =[0])
scipySpearmanOutput = pd.DataFrame({'Correlation': spearmancorrelation, 'PValue': spearmanp, 'CorrType': 'Spearson', 'From': 'SciPy'}, index =[0])

corrCombined = pd.concat([scipyPearsonOutput, scipySpearmanOutput])

## Example 2 - from PANDAS - PEARON and SPEARMAN CORRELATIONS
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html
# does NOT include P-value 
import pandas as pd

pd_pearson = diabetes['time_in_hospital'].corr(diabetes['num_lab_procedures'], method='pearson')
pd_spearman = diabetes['time_in_hospital'].corr(diabetes['num_lab_procedures'], method='spearman')

pandasPearsonOutput = pd.DataFrame({'Correlation': pd_pearson, 'PValue': 'NOT PROVIDED', 'CorrType': 'Pearson','From': 'Pandas'}, index =[0])
pandasSpearmanOutput = pd.DataFrame({'Correlation': pd_spearman, 'PValue': 'NOT PROVIDED', 'CorrType': 'Spearson', 'From': 'Pandas'}, index =[0])

corrCombinedOutputs = pd.concat([corrCombined, pandasPearsonOutput, pandasSpearmanOutput]) ### FOUR tests performed ### 

#################################################################################
################################## Question 2 ###################################
#################################################################################
#### Is there a correlation between time in number of dianogses and the total ###
#################### number of procedures (non labs + labs)? ####################
#################################################################################
######## Yes there is a correlation; it is somwhere between 0.16 and 0.17 #######
#################################################################################

numberDiagnoses = diabetes['number_diagnoses']
totalCountProcedures = diabetes['totalCountProcedures']


numberDiagnoses_stat, numberDiagnoses_p = shapiro(numberDiagnoses)
print('Statistics=%.3f, p=%.3f' % (numberDiagnoses_stat, numberDiagnoses_p))
# interpret
alpha = 0.05
if numberDiagnoses_p > alpha:
	print('Sample looks Gaussian (fail to reject H0)')
else:
	print('Sample does not look Gaussian (reject H0)')

totalCountProcedures_stat, totalCountProcedures_p = shapiro(totalCountProcedures)
print('Statistics=%.3f, p=%.3f' % (totalCountProcedures_stat, totalCountProcedures_p))
# interpret
alpha = 0.05
if totalCountProcedures_p > alpha:
	print('Sample looks Gaussian (fail to reject H0)')
else:
	print('Sample does not look Gaussian (reject H0)')
    
# histogram plot
pyplot.hist(numberDiagnoses).show()
pyplot.hist(totalCountProcedures).show()
###################################################################################
###################################################################################
####### AttributeError: 'tuple' object has no attribute 'show' on histogram #######
###################################################################################
###################################################################################
diabetes['totalCountProcedures'].value_counts()
diabetes['number_diagnoses'].value_counts()
diabetes['number_diagnoses'].describe()
diabetes['totalCountProcedures'].describe()

## No rounding issue it seems ##
## Use pandas for hist## 

diabetes['number_diagnoses'].hist(bins=20)
diabetes['totalCountProcedures'].hist(bins=20)

############### HOMOGENEITY ###############
stats.bartlett(totalCountProcedures, numberDiagnoses)
stats.bartlett(diabetes['number_diagnoses'], diabetes['totalCountProcedures']) 


spearmancorrelation2, spearmanp = spearmanr(numberDiagnoses, totalCountProcedures)
pearsoncorrelation2, pearsonp = pearsonr(numberDiagnoses, totalCountProcedures)

scipyPearsonOutput2 = pd.DataFrame({'Correlation': pearsoncorrelation2, 'PValue': pearsonp, 'CorrType': 'Pearson', 'From': 'SciPy'}, index =[0])
scipySpearmanOutput2 = pd.DataFrame({'Correlation': spearmancorrelation2, 'PValue': spearmanp, 'CorrType': 'Spearson', 'From': 'SciPy'}, index =[0])

corrCombined2 = pd.concat([scipyPearsonOutput2, scipySpearmanOutput2])

## Pandas alternative to SciPy 
pd_pearson2 = diabetes['number_diagnoses'].corr(diabetes['totalCountProcedures'], method='pearson')
pd_spearman2 = diabetes['number_diagnoses'].corr(diabetes['totalCountProcedures'], method='spearman')

pandasPearsonOutput2 = pd.DataFrame({'Correlation': pd_pearson2, 'PValue': 'NOT PROVIDED', 'CorrType': 'Pearson','From': 'Pandas'}, index =[0])
pandasSpearmanOutput2 = pd.DataFrame({'Correlation': pd_spearman2, 'PValue': 'NOT PROVIDED', 'CorrType': 'Spearson', 'From': 'Pandas'}, index =[0])

corrCombinedOutputs2 = pd.concat([corrCombined2, pandasPearsonOutput2, pandasSpearmanOutput2]) 

#################################################################################
################################## Question 3 ###################################
#################################################################################
####### T TEST: is there a difference between sex (male vs female) (IV) #########
########### and the number of procedures performed (DV) ? #######################
#################################################################################
#################################################################################

# gender 
# totalCountProcedures 

# Independent t-test // TWO INDEPENDENT SAMPLES OF SCORES (ASSUMES equal VARIANCE)
from scipy.stats import ttest_ind

female = diabetes[diabetes['gender']=='Female']
male = diabetes[diabetes['gender']=='Male']
ttest_ind(female['totalCountProcedures'], male['totalCountProcedures']) #returns t-statistics and the p-value 


# Dependent t-test // TWO RELATED SAMPLES OF SCORES (ASSUMES equal VARIANCE)
from scipy.stats import ttest_rel

#ttest_rel(female['totalCountProcedures'], male['totalCountProcedures'])

#################################################################################
################################## Question 4 ###################################
#################################################################################
####### T TEST: is there a difference between sex (male vs female) (IV) #########
########### and the number of days in the hospital (DV) ? #######################
#################################################################################
#################################################################################
female = diabetes[diabetes['gender']=='Female']
male = diabetes[diabetes['gender']=='Male']

ttestSexDays = ttest_ind(female['time_in_hospital'], male['time_in_hospital'])

#################################################################################
################################## Question 5 ###################################
#################################################################################
## T TEST: is there a difference between race (Caucasian and African American) ##
######### (IV) and the number of days in the hospital (DV) ? ####################
#################################################################################
#################################################################################
caucasian = diabetes[diabetes['race']== 'Caucasian']
africanamerican = diabetes[diabetes['race']== 'AfricanAmerican']

ttestRaceDays = ttest_ind(caucasian['time_in_hospital'], africanamerican['time_in_hospital'])

#################################################################################
################################## Question 6 ###################################
#################################################################################
## T TEST: is there a difference between race (Asian and African American) ######
######### (IV) and the number of lab procedures (DV) ? ##########################
#################################################################################
#################################################################################
africanamerican = diabetes[diabetes['race']== 'AfricanAmerican']
asian = diabetes[diabetes['race']== 'Asian']

ttestRaceLab = ttest_ind(asian['num_lab_procedures'], africanamerican['num_lab_procedures'])
