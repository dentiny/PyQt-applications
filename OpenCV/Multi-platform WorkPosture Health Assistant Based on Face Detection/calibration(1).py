# -*- coding: utf-8 -*-

import pickle;
import numpy as np;

if(__name__ == "__main__"):
    distances = list();
    with open("50cm_angle.pkl", 'rb') as f:
        distances = pickle.load(f);
    
    # whether data is authentic
    distances = [d for d in distances if(0 <= d <= 10)];
    print(len(distances)); # 500
    print(np.mean(np.array(distances))); # 66.61948598650947