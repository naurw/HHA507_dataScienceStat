#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 16:38:50 2021

@author: William
"""

# =============================================================================
# Questions: 
# 1) Is there a difference between SEX (M:F) and the number of days in hospital?
# 2) Is there a difference between RACE (Caucasian and African American) and the number of days in hospital?
# 3) Is there a difference between RACE (Asian and African American) and the number of lab procedures performed?
# =============================================================================

import pandas as pd 
diabetes = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Datasets/Diabetes/DB1_Diabetes/diabetic_data.csv')

diabetes.info()

import scipy
from scipy.stats import ttest_ind

# =============================================================================
# Question 1: 
# =============================================================================
gender = diabetes['gender']
gender.value_counts()
male = diabetes[diabetes['gender']=='Male']
female = diabetes[diabetes['gender']=='Female']

ttest1 = ttest_ind(male['time_in_hospital'], female['time_in_hospital'])
print('The t-statistic and the p-value are:', ttest1)
## There is a difference because the p-value is signficantly lower than the our alpha of 0.05 or our 95% CI 
## pvalue=1.4217299655114968e-21 < 0.05 

# =============================================================================
# Question 2: 
# =============================================================================
race = diabetes['race']
race.value_counts()

caucasian = diabetes[diabetes['race']=='Caucasian']
africanAmerican = diabetes[diabetes['race']=='AfricanAmerican']

ttest2 = ttest_ind(caucasian['time_in_hospital'], africanAmerican['time_in_hospital'])
print('The t-statistic and the p-value are:', ttest2)
## There is a difference because the p-value is signficantly lower than the our alpha of 0.05 or our 95% CI 
## pvalue=4.178330085585203e-07 < 0.05

# =============================================================================
# Question 3: 
# =============================================================================

asian  = diabetes[diabetes['race']=='Asian']
africanAmerican = diabetes[diabetes['race']=='AfricanAmerican']

ttest3 = ttest_ind(asian['num_lab_procedures'], africanAmerican['num_lab_procedures'])
print('The t-statistic and the p-value are:', ttest3)
## There is a difference because the p-value is signficantly lower than the our alpha of 0.05 or our 95% CI 
## pvalue=6.948907528800307e-05 < 0.05 
