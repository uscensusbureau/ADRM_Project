# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 20:46:22 2023

@author: onais
"""

import pseudopeople 

 
config = {
    'decennial_census': { 
        'column_noise': { # "Choose the wrong option" is in the column-based noise category
            'sex': { # Column
                'choose_wrong_option': { # Noise type
                    'cell_probability': 0.05, # Parameter (and value)
                },
            },
        },
    },
}
 
pseudopeople.generate_decennial_census(source="C:/Users/onais/Downloads/pseudopeople_input_data_ri_1_0_0/", seed=0, config=config, year=2020, verbose=False).to_csv("2020DataSet.csv", encoding='utf-8')






