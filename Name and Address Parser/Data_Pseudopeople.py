# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 20:46:22 2023

@author: onais
"""

import pseudopeople 
pseudopeople.generate_decennial_census(source="C:/Users/onais/Downloads/pseudopeople_input_data_ri_1_0_0/", seed=0, config=None, year=2020, verbose=False).to_csv("2020DataSet.csv", encoding='utf-8')






