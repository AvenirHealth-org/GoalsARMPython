## +===+ Excel workbook constants +============================================+
## Names of input workbook tabs
XLSX_TAB_CONFIG       = "Config"
XLSX_TAB_PASFRS       = "FertilityInputs"
XLSX_TAB_MIGR         = "MigrInputs"
XLSX_TAB_INCI         = "DirectIncidenceInputs"
XLSX_TAB_PARTNER      = "PartnershipInputs"
XLSX_TAB_MIXNG_MATRIX = "MixingMatrix"
XLSX_TAB_CONTACT      = "ContactInputs"
XLSX_TAB_POPSIZE      = "PopSizeInputs"
XLSX_TAB_EPI          = "EpiInputs"
XLSX_TAB_STIPREV      = "STIPrevInputs"
XLSX_TAB_HIV_FERT     = "HIVFertilityInputs"
XLSX_TAB_ADULT_PROG   = "HIVDiseaseInputs"
XLSX_TAB_ADULT_ART    = "ARTAdultInputs"
XLSX_TAB_MALE_CIRC    = "MCInputs"
XLSX_TAB_MTCT_RATES   = "MTCTRateInputs"
XLSX_TAB_BF           = "BreastfeedingInputs"
XLSX_TAB_DIRECT_CLHIV = "DirectCLHIV"
XLSX_TAB_LIKELIHOOD   = "LikelihoodInputs"
XLSX_TAB_FITTING      = "FittingInputs"

## The Excel file specifies inputs for 1970-2050, the projection
## uses a subset of these
XLSX_FIRST_YEAR = 1970
XLSX_FINAL_YEAR = 2050

## Configuration tab tags
CFG_FIRST_YEAR       = "first.year"
CFG_FINAL_YEAR       = "final.year"
CFG_UPD_NAME         = "upd.file"
CFG_USE_UPD_PASFRS   = "use.upd.pasfrs"
CFG_USE_UPD_MIGR     = "use.upd.migr"
CFG_USE_DIRECT_INCI  = "use.direct.inci"
CFG_USE_DIRECT_CLHIV = "use.direct.clhiv"

## EpiInputs tab tags
EPI_TRANSMIT_F2M     = "transmit.f2m"
EPI_TRANSMIT_M2F     = "transmit.m2f"
EPI_TRANSMIT_M2M     = "transmit.m2m"
EPI_TRANSMIT_CHRONIC = "transmit.chronic"
EPI_TRANSMIT_PRIMARY = "transmit.primary"
EPI_TRANSMIT_SYMPTOM = "transmit.symptom"
EPI_TRANSMIT_ART_VS  = "transmit.art.vs"
EPI_TRANSMIT_ART_VF  = "transmit.art.vf"
EPI_TRANSMIT_STI_NEG = "effect.sti.neg"
EPI_TRANSMIT_STI_POS = "effect.sti.pos"
EPI_EFFECT_VMMC      = "effect.vmmc"
EPI_EFFECT_CONDOM    = "effect.condom"
EPI_ART_MORT_WEIGHT  = "art.mort.weight"
EPI_INITIAL_YEAR     = "seed.time"
EPI_INITIAL_PREV     = "seed.prev"

## MTCTRateInputs tab tags
MTCT_PN_NONE_000_200  = "peri.none.lt.200"
MTCT_PN_NONE_200_350  = "peri.none.200.350"
MTCT_PN_NONE_GEQ_350  = "peri.none.gt.350"
MTCT_PN_INCI          = "peri.inci"
MTCT_PN_SDNVP         = "peri.sdnvp"
MTCT_PN_DUAL          = "peri.dual"
MTCT_PN_OPT_A         = "peri.opt.a"
MTCT_PN_OPT_B         = "peri.opt.b"
MTCT_PN_ART_BEFORE    = "peri.art.before"
MTCT_PN_ART_DURING    = "peri.art.during"
MTCT_PN_ART_LATE      = "peri.art.late"
MTCT_BF_NONE_000_200  = "bf.none.lt.200"
MTCT_BF_NONE_200_350  = "bf.none.200.350"
MTCT_BF_NONE_GEQ_350  = "bf.none.gt.350"
MTCT_BF_INCI          = "bf.inci"
MTCT_BF_SDNVP_000_350 = "bf.sdnvp.lt.350"
MTCT_BF_SDNVP_GEQ_350 = "bf.sdnvp.gt.350"
MTCT_BF_DUAL_000_350  = "bf.dual.lt.350"
MTCT_BF_DUAL_GEQ_350  = "bf.dual.gt.350"
MTCT_BF_OPT_A         = "bf.opt.a"
MTCT_BF_OPT_B         = "bf.opt.b"
MTCT_BF_ART_BEFORE    = "bf.art.before"
MTCT_BF_ART_DURING    = "bf.art.during"
MTCT_BF_ART_LATE      = "bf.art.late"

## LikelihoodInputs tab tags
LHOOD_ANCSS_BIAS     = "ancss.bias"
LHOOD_ANCRT_BIAS     = "ancrt.bias"
LHOOD_VARINFL_SITE   = "var.infl.site"
LHOOD_VARINFL_CENSUS = "var.infl.census"

## FittingInputs tab tags
FIT_INITIAL_PREV        = EPI_INITIAL_PREV
FIT_TRANSMIT_F2M        = EPI_TRANSMIT_F2M
FIT_TRANSMIT_M2F        = EPI_TRANSMIT_M2F
FIT_TRANSMIT_STI_NEG    = EPI_TRANSMIT_STI_NEG
FIT_TRANSMIT_STI_POS    = EPI_TRANSMIT_STI_POS
FIT_FORCE_PWID          = "force.pwid"
FIT_LT_PARTNER_F        = "lt.partner.f"
FIT_LT_PARTNER_M        = "lt.partner.m"
FIT_PARTNER_AGE_MEAN_F  = "partner.age.mean.f"
FIT_PARTNER_AGE_MEAN_M  = "partner.age.mean.m"
FIT_PARTNER_AGE_SCALE_F = "partner.age.scale.f"
FIT_PARTNER_AGE_SCALE_M = "partner.age.scale.m"
FIT_PARTNER_POP_FSW     = "partner.pop.fsw"
FIT_PARTNER_POP_CLIENT  = "partner.pop.client"
FIT_PARTNER_POP_MSM     = "partner.pop.msm"
FIT_PARTNER_POP_TGW     = "partner.pop.tgw"
FIT_ASSORT_GEN          = "assort.gen"
FIT_ASSORT_FSW          = "assort.fsw"
FIT_ASSORT_MSM          = "assort.msm"
FIT_ASSORT_TGW          = "assort.tgw"
FIT_HIV_FRR_LAF         = "hiv.frr.laf"
FIT_ANCSS_BIAS          = LHOOD_ANCSS_BIAS
FIT_ANCRT_BIAS          = LHOOD_ANCRT_BIAS
FIT_VARINFL_SITE        = LHOOD_VARINFL_SITE
FIT_VARINFL_CENSUS      = LHOOD_VARINFL_CENSUS

## +===+ Model constants +=====================================================+
## Model constants are aligned with values in GoalsARM_Core DPConst.H

## +-+ Sex and male circumcision status +--------------------------------------+
SEX_FEMALE = 0 # female
SEX_MALE   = 1
SEX_MALE_U = 1 # male, uncircumcised
SEX_MALE_C = 2 # male, circumcised
SEX_MIN    = 0
SEX_MAX    = 1
SEX_MC_MIN = 0
SEX_MC_MAX = 2
N_SEX    = SEX_MAX - SEX_MIN + 1
N_SEX_MC = SEX_MC_MAX - SEX_MC_MIN + 1

## Map from sex and circumcision status (SEX_FEMALE, SEX_MALE_U, SEX_MALE_C) to sex alone
sex = [SEX_FEMALE, SEX_MALE, SEX_MALE]

## +-+ Age constants +---------------------------------------------------------+
AGE_MIN = 0
AGE_MAX = 80
AGE_CHILD_MIN = AGE_MIN
AGE_CHILD_MAX = 14
AGE_ADULT_MIN = AGE_CHILD_MAX + 1
AGE_ADULT_MAX = AGE_MAX
AGE_BIRTH_MIN = AGE_ADULT_MIN # minimum reproductive age
AGE_BIRTH_MAX = 49            # maximum reproductive age

N_AGE = AGE_MAX - AGE_MIN + 1
N_AGE_CHILD = AGE_CHILD_MAX - AGE_CHILD_MIN + 1 # number of child ages
N_AGE_ADULT = AGE_ADULT_MAX - AGE_ADULT_MIN + 1 # number of adult ages
N_AGE_BIRTH = AGE_BIRTH_MAX - AGE_BIRTH_MIN + 1 # number of reproductive ages

## +-+ Behavioral risk constants +---------------------------------------------+
POP_NOSEX = 0 # male or female, never had sex
POP_NEVER = 1 # male or female, never married
POP_UNION = 2 # male or female, married or in stable union
POP_SPLIT = 3 # male or female, previously married
POP_PWID = 4  # male or female, people who inject drugs
POP_FSW = 5   # female only, female sex workers
POP_CSW = 5   # male only, male clients of female sex workers
POP_BOTH = 5  # male or female, female sex workers or their clients
POP_MSM = 6   # male only, men who have sex with men
POP_TGW = 7   # male only, transgender women

POP_MIN = 0
POP_MAX = 7
N_POP = POP_MAX - POP_MIN + 1

POP_KEY_MIN = POP_PWID
POP_KEY_MAX = POP_MAX
N_POP_KEY = POP_KEY_MAX - POP_KEY_MIN + 1

## +-+ HIV infection stage constants +-----------------------------------------+
## Child categories (CD4 percent), ages 0-4
HIV_PRC_GT_30 = 0
HIV_PRC_26_30 = 1
HIV_PRC_21_25 = 2
HIV_PRC_16_20 = 3
HIV_PRC_11_15 = 4
HIV_PRC_05_10 = 5
HIV_PRC_LT_05 = 6

## Child categories, ages 5-14
HIV_NUM_GEQ_1000 = 0
HIV_NUM_750_1000 = 1
HIV_NUM_500_750  = 2
HIV_NUM_350_500  = 3
HIV_NUM_200_350  = 4
HIV_NUM_LT_200   = 5
HIV_NUM_INVALID  = 6 # Not used

## Adult (ages 15+) categories, defined by CD4 counts
HIV_PRIMARY = 0
HIV_GEQ_500 = 1
HIV_350_500 = 2
HIV_200_350 = 3
HIV_100_200 = 4
HIV_050_100 = 5
HIV_000_050 = 6

HIV_CHILD_PRC_MIN = 0 # Children aged 0-4
HIV_CHILD_PRC_MAX = 6 # Children aged 0-4
HIV_CHILD_NUM_MIN = 0 # Children aged 5-14
HIV_CHILD_NUM_MAX = 5 # Children aged 5-14

HIV_CHILD_MIN = 0 # Children 0-14 (will include HIV_NUM_INVALID for ages 5-14)
HIV_CHILD_MAX = 6

HIV_ADULT_MIN = 0
HIV_ADULT_MAX = 6

HIV_MIN = 0
HIV_MAX = 6

N_HIV_CHILD_PRC = HIV_CHILD_PRC_MIN - HIV_CHILD_PRC_MAX + 1
N_HIV_CHILD_NUM = HIV_CHILD_NUM_MAX - HIV_CHILD_NUM_MIN + 1
N_HIV_CHILD     = HIV_CHILD_MAX - HIV_CHILD_MIN + 1
N_HIV_ADULT     = HIV_ADULT_MAX - HIV_ADULT_MIN + 1
N_HIV           = HIV_MAX - HIV_MIN + 1

## +-+ HIV diagnosis (Dx) and treatment (Tx) constants +---------------------+
		
DTX_UNAWARE = 0 # HIV-positive but status-unaware
DTX_AWARE   = 1 # HIV-positive and status-aware but not on ART
DTX_PREV_TX = 2 # HIV-positive and previously on ART
DTX_ART1    = 3 # Months [0,6) on ART
DTX_ART2    = 4 # Months [6,12) on ART
DTX_ART3    = 5 # Months [12,\infty) on ART

DTX_MIN = 0
DTX_MAX = 5

# Bounds for looping just for off-ART states
DTX_OFF_MIN = 0
DTX_OFF_MAX = 2

# Bounds for looping just over on-ART states
DTX_ART_MIN = 3
DTX_ART_MAX = 5

N_DTX = DTX_MAX - DTX_MIN + 1
N_ART = DTX_ART_MAX - DTX_ART_MIN + 1

## +=+ MTCT constants +========================================================+
## +-+ MTCT timing +-----------------------------------------------------------+
MTCT_PN = 0 # perinatal
MTCT_BF = 1 # breastfeeding

# detailed transmission timing during breastfeeding
MTCT_MOS_00_02 =  1 # [0,2) months after delivery
MTCT_MOS_02_04 =  2 # [2,4) months
MTCT_MOS_04_06 =  3 # [4,6) months
MTCT_MOS_06_08 =  4
MTCT_MOS_08_10 =  5
MTCT_MOS_10_12 =  6
MTCT_MOS_12_14 =  7
MTCT_MOS_14_16 =  8
MTCT_MOS_16_18 =  9
MTCT_MOS_18_20 = 10
MTCT_MOS_20_22 = 11
MTCT_MOS_22_24 = 12
MTCT_MOS_24_26 = 13
MTCT_MOS_26_28 = 14
MTCT_MOS_28_30 = 15
MTCT_MOS_30_32 = 16
MTCT_MOS_32_34 = 17
MTCT_MOS_34_36 = 18 # [34,36) months

MTCT_MIN = 0
MTCT_MAX = 1

MTCT_MOS_MIN = 0
MTCT_MOS_MAX = 18

N_MTCT = MTCT_MAX - MTCT_MIN + 1
N_MTCT_MOS = MTCT_MOS_MAX - MTCT_MOS_MIN + 1

## +-+ MTCT regimens +---------------------------------------------------------+
MTCT_RX_SDNVP      = 0 # Single-dose nevirapine
MTCT_RX_DUAL       = 1 # WHO 2006 dual ARV regimens (described in doi:10.1136/sextrans-2012-050709)
MTCT_RX_OPT_A      = 2 # Option A (described in ISBN: 978 92 4 159981 8)
MTCT_RX_OPT_B      = 3 # Option B (described in ISBN: 978 92 4 159981 8)
MTCT_RX_ART_BEFORE = 4 # ART initiated before current pregnancy
MTCT_RX_ART_DURING = 5 # ART initiated during current pregnancy >=4 weeks before delivery
MTCT_RX_ART_LATE   = 6 # ART initiated during current pregnancy <4 weeks before delivery
MTCT_RX_NONE       = 7 # No prophylaxis
MTCT_RX_STOP       = 8 # Stopped prophylaxis
MTCT_RX_INCI       = 9 # Incident infection during pregnancy

MTCT_RX_MIN = 0
MTCT_RX_MAX = 9

N_MTCT_RX = MTCT_RX_MAX - MTCT_RX_MIN + 1

## +-+ MTCT-relevant maternal CD4 categories +---------------------------------+
MTCT_CD4_000_200 = 0 # [0,200) CD4 cells/mm3
MTCT_CD4_200_350 = 1 # [200,350) CD4 cells/mm3
MTCT_CD4_GEQ_350 = 2 # [350,\infty) CD4 cells/mm3

MTCT_CD4_MIN = 0
MTCT_CD4_MAX = 2

N_MTCT_CD4 = MTCT_CD4_MAX - MTCT_CD4_MIN + 1

## +===+ Fitting constants +===================================================+
DIST_LOGNORMAL = 'Lognormal'
DIST_NORMAL    = 'Normal'
DIST_GAMMA     = 'Gamma'
DIST_BETA      = 'Beta'
