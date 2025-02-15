import os
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

## Output numbers of new infections are written to a CSV file with one row
## per timing of transmission (perinatal, breastfeeding at [0,2), [2,4), ..., [34,36) months after delivery)
## and one column per maternal PMTCT regimen:
##
## SDNVP        Vertical transmission among women who received single-dose nevirapine
## DUAL         Dual ARV regimen
## OPT_A        Option A
## OPT_B        Option B
## ART_BEFORE   Started ART before current pregnancy
## ART_DURING   Started ART during current pregnancy at least 4 weeks before delivery
## ART_LATE     Started ART during current pregnancy less than 4 weeks before delivery
## MTCT_RX_NONE Never received ARVs during pregnancy or breastfeeding
## MTCT_RX_STOP Stopped ARVs during pregnancy or breastfeeding
## MTCT_RX_INCI Vertical transmission after incident maternal HIV infection

def main(xlsx_name, csv_name, year, data_path):
    model = Model()
    model.init_from_xlsx(xlsx_name)

    colnames = ['SDNVP', 'DUAL', 'OPT_A', 'OPT_B', 'ART_BEFORE', 'ART_DURING', 'ART_LATE', 'NONE', 'STOP', 'INCI']

    females = np.genfromtxt(csv_name, delimiter=',', skip_header=1, usecols=range(1,11))
    births = model.births_hiv_exposed(year, females)
    infections = model.new_child_infections(year, females, births)
    np.savetxt(data_path + "\\vt.csv", infections, delimiter=',', header=','.join(colnames), comments="")
    pass

if __name__ == "__main__":
    sys.stderr.write("Process %d\n" % (os.getpid()))
    if len(sys.argv) == 1:
        xlsx_name = "inputs\\example-inputs-mtct.xlsx"
        csv_name  = "inputs\\example-females.csv"
        year = 2000
        data_path = "."
        main(xlsx_name, csv_name, year, data_path)
    elif len(sys.argv) < 5:
        sys.stderr.write("USAGE: %s <input_param>.xlsx <females>.csv <year> <output_path>" % (sys.argv[0]))
    else:
        xlsx_name = sys.argv[1]
        csv_name  = sys.argv[2]
        year      = int(sys.argv[3])
        data_path = sys.argv[4]
        main(xlsx_name, csv_name, year, data_path)
