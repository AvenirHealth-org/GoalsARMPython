import os
import pandas as pd
import numpy as np
import goals.goals_const as CONST
import sys
from goals.goals_model import Model

## This script calculates numbers of vertical HIV transmissions from mothers to children
## This takes as input a Goals ARM Excel workbook and a CSV file reporting the number of
## reproductive-age women in the population by age (15, 16, ..., 49) and HIV status:
## HIV_PRIMARY  Women with prevalent, untreated primary stage HIV infection
## HIV_GEQ_500  Women with prevalent, untreated HIV infection, CD4>=500
## HIV_350_500  Women with prevalent, untreated HIV infection, CD4 [350,500)
## HIV_200_350  Women with prevalent, untreated HIV infection, CD4 [200, 350)
## HIV_100_200	Women with prevalent, untreated HIV infection, CD4 [100, 200)
## HIV_050_100	Women with prevalent, untreated HIV infection, CD4 [50, 100)
## HIV_000_050  Women with prevalent, untreated HIV infection, CD4 [0, 50)
## HIV_ART      Women with prevalent HIV infection on ART
## HIV_NEG      Women without HIV
## HIV_NEW      Women with incident HIV infection

def main(xlsx_name, csv_name, data_path):
    model = Model()
    model.init_from_xlsx(xlsx_name)

    females = np.genfromtxt(csv_name, delimiter=',', skip_header=1, usecols=range(1,11))
    births = model.births_hiv_exposed(2000, females)
    infections = model.new_child_infections(2000, females, births)
    np.savetxt(data_path + "\\vt.csv", infections, delimiter=',')
    # out_frame = array2frame(infections, ['SDNVP', 'DUAL', 'OPT_A', 'OPT_B', 'ART_BEFORE', "ART_DURING", 'ART_LATE', 'MTCT_RX_NONE', 'MTCT_RX_STOP', 'MTCT_RX_INCI'])
    # out_frame.to_csv(data_path + "\\vt.csv")
    pass

if __name__ == "__main__":
    sys.stderr.write("Process %d\n" % (os.getpid()))
    if len(sys.argv) == 1:
        xlsx_name = "inputs\\example-inputs-mtct.xlsx"
        csv_name  = "inputs\\example-females.csv"
        data_path = "."
        main(xlsx_name, csv_name, data_path)
    elif len(sys.argv) < 4:
        sys.stderr.write("USAGE: %s <input_param>.xlsx <females>.csv <output_path>" % (sys.argv[0]))
    else:
        xlsx_name = sys.argv[1]
        csv_name  = sys.argv[2]
        data_path = sys.argv[3]
        main(xlsx_name, csv_name, data_path)
