import numpy as np
import openpyxl as xlsx
import os
import pandas as pd
import plotnine
import scipy.optimize as optimize
import scipy.stats as stats
import sys
import time
import src.goals_model as Goals
import src.goals_const as CONST
import src.goals_utils as Utils
from percussion import ancprev, hivprev

## TODO: make fill_hivprev_template, plot_fit_* members of GoalsFitter

## Install percussion, the likelihood model package:
## python -m pip install git+https://rlglaubius:${token}@github.com/rlglaubius/percussion.git

def fill_hivprev_template(hivsim, template):
    # Poor practice first cut: loop. Since the template rows are invariant from
    # one simulation to the next, we may be able to precompute and store the
    # indices needed to calculate the model's prevalence estimates
    nobs = len(template.index)
    pop = template['Population']
    sex = template['Gender']
    yidx = template['Year'] - hivsim.year_first     # convert from years to indices relative to the first year of projection
    amin = template['AgeMin'] - CONST.AGE_ADULT_MIN # convert from ages to years since entry into the adult model
    amax = template['AgeMax'] - CONST.AGE_ADULT_MIN + 1
    for row in range(nobs):
        match pop[row]:
            case 'All': pop_min, pop_max = CONST.POP_MIN, CONST.POP_MAX + 1
            case 'FSW': pop_min, pop_max = CONST.POP_FSW, CONST.POP_FSW + 1
            case 'MSM': pop_min, pop_max = CONST.POP_MSM, CONST.POP_MSM + 1
            case _: sys.stderr.write("Error: Unrecognized population %s" % (pop[row]))

        match sex[row]:
            case 'All':    sex_min, sex_max = CONST.SEX_MC_MIN, CONST.SEX_MC_MAX + 1
            case 'Female': sex_min, sex_max = CONST.SEX_FEMALE, CONST.SEX_FEMALE + 1
            case 'Male':   sex_min, sex_max = CONST.SEX_MALE_U, CONST.SEX_MALE_C + 1
            case _: sys.stderr.write("Error: Unrecognized gender %s" % (sex[row]))

        pop_hiv = hivsim.pop_adult_hiv[yidx[row], sex_min:sex_max, amin[row]:amax[row], pop_min:pop_max, :, :].sum()
        pop_neg = hivsim.pop_adult_neg[yidx[row], sex_min:sex_max, amin[row]:amax[row], pop_min:pop_max].sum()
        template.at[row,'Prevalence'] = pop_hiv / (pop_hiv + pop_neg)

def plot_fit_anc(hivsim, ancdat, tiffname):
    anc_data = ancdat.anc_data.copy()
    anc_data['Source'] = ['Census' if site=='Census' else 'ANC-%s' % (kind) for site, kind in zip(anc_data['Site'], anc_data['Type'])]

    mod_data = pd.DataFrame({'Year'     : list(range(hivsim.year_first, hivsim.year_final + 1)),
                             'Prevalence' : hivsim.births_exposed / hivsim.births.sum((1)),
                             'Site'       : 'Goals',
                             'Source'     : 'Goals'})

    p = (plotnine.ggplot(anc_data[anc_data['Site'] != 'Census'])
         + plotnine.aes(x='Year', y='Prevalence', color='Source', group='Site')
         + plotnine.geom_line()
         + plotnine.geom_point()
         + plotnine.geom_line(data=anc_data[anc_data['Site'] == 'Census'])
         + plotnine.geom_point(data=anc_data[anc_data['Site'] == 'Census'])
         + plotnine.geom_line(data=mod_data)
         + plotnine.theme_bw())
    p.save(filename=tiffname, dpi=600, units="in", width=6.5, height=5.0, pil_kwargs={"compression" : "tiff_lzw"})

def plot_fit_hiv(hivsim, hivdat, tiffname):
    hiv_data = hivdat.hiv_data.copy()
    hiv_data['Age'] = ['%s-%s' % (amin, amax) for (amin, amax) in zip(hiv_data['AgeMin'], hiv_data['AgeMax'])]
    hiv_data.rename(columns={'Value' : 'Prevalence'}, inplace=True)

    # Capture HIV prevalence every year for the populations with data
    pop_frame = hiv_data.groupby(['Population', 'Gender', 'AgeMin', 'AgeMax']).size().reset_index(name='Prevalence')
    yrs_frame = pd.DataFrame({'Year' : range(hivsim.year_first, hivsim.year_final + 1)})
    mod_data = yrs_frame.join(pop_frame, how='cross')
    fill_hivprev_template(hivsim, mod_data)
    mod_data['Age'] = ['%s-%s' % (amin, amax) for (amin, amax) in zip(mod_data['AgeMin'], mod_data['AgeMax'])]

    p = (plotnine.ggplot(hiv_data[hiv_data['AgeMax'] > 14])
         + plotnine.aes(x='Year', y='Prevalence', color='Gender')
         + plotnine.geom_point()
         + plotnine.geom_line(data=mod_data[mod_data['AgeMax'] > 14])
         + plotnine.facet_grid('Population~Age', scales='free_y')
         + plotnine.theme_bw()
         + plotnine.theme(axis_text_x = plotnine.element_text(angle=90)))
    p.save(filename=tiffname, dpi=600, units="in", width=16, height=9, pil_kwargs={"compression" : "tiff_lzw"})

def test_mixing_weight(hivsim,file,year_final):
    pop_prefs_all = pd.read_csv(file,header = None)
    for iter in range(62):  
        #print(iter)
        pop_prefs = pop_prefs_all.iloc[iter]
        
        pop_prefs =  pop_prefs.to_numpy()
        pop_prefs =  np.reshape(pop_prefs, (-1, 2))

        hivsim.pop_assort[:] = hivsim.calc_pop_assort(pop_prefs)

        ## TODO: could skip invalidation if only ANC likelihood parameters are being varied
        hivsim.invalidate(-1) # needed so that Goals will recalculate the projection
        hivsim.project(year_final)

        ## Save and output infections and prevalence before full calibration
        new_infections = np.sum(hivsim.new_infections, axis=(2))[:,:,7]
        dt = pd.DataFrame(new_infections, columns = ['female','male','male_c'])
        dt['pop']='POP_TGW'
        new_col = range(1970,year_final+1)
        dt['year'] = new_col


        for i in range(7):
            new_infections = np.sum(hivsim.new_infections, axis=(2))[:,:,i]

            df2 = pd.DataFrame(new_infections, columns = ['female','male','male_c'])
            df2['year'] = new_col
            df2['iter'] = iter
            if i == 0:
                df2['pop']= 'POP_NOSEX'
            if i == 1:
                df2['pop']=  'POP_NEVER'
            if i == 2:
                df2['pop']=  'POP_UNION'
            if i == 3:
                df2['pop']= 'POP_SPLIT'
            if i == 4:
                df2['pop']=  'POP_PWID'
            if i == 5:
                df2['pop']=  'POP_FSW_CFSW'
            if i == 6:
                df2['pop']=  'POP_MSM'
            dt = pd.concat([dt, df2])
        
        name_out = "C:\Proj\Repositories\GoalsARMPython\outputs\sensitivity\mixing_weights\infections_" + str(iter) + ".csv"
        dt.to_csv(name_out, index=False)

def test_same_sex_var(hivsim,file,year_final):
    age_prefs_all = pd.read_csv(file,header = None)
    for iter in range(15):  
        
        age_prefs = age_prefs_all.iloc[iter]
        age_prefs = np.array(age_prefs, dtype=np.float64, order="C")
        age_prefs = age_prefs.reshape((3,1))
        
        hivsim.age_mixing[:] = hivsim.calc_partner_prefs(age_prefs)
        
        hivsim.invalidate(-1) # needed so that Goals will recalculate the projection
        hivsim.project(year_final)

        ## Save and output infections and prevalence before full calibration
        new_infections = np.sum(hivsim.new_infections, axis=(2))[:,:,7]
        dt = pd.DataFrame(new_infections, columns = ['female','male','male_c'])
        dt['pop']='POP_TGW'
        new_col = range(1970,year_final+1)
        dt['year'] = new_col

        for i in range(7):
            new_infections = np.sum(hivsim.new_infections, axis=(2))[:,:,i]

            df2 = pd.DataFrame(new_infections, columns = ['female','male','male_c'])
            df2['year'] = new_col
            df2['iter'] = iter
            if i == 0:
                df2['pop']= 'POP_NOSEX'
            if i == 1:
                df2['pop']=  'POP_NEVER'
            if i == 2:
                df2['pop']=  'POP_UNION'
            if i == 3:
                df2['pop']= 'POP_SPLIT'
            if i == 4:
                df2['pop']=  'POP_PWID'
            if i == 5:
                df2['pop']=  'POP_FSW_CFSW'
            if i == 6:
                df2['pop']=  'POP_MSM'
            dt = pd.concat([dt, df2])
        
        name_out = "C:\Proj\Repositories\GoalsARMPython\outputs\sensitivity\same_sex_var\infections_" + str(iter) + ".csv"
        dt.to_csv(name_out, index=False)
        
# wrappers around scipy stats log densities that can be used
# in standard ways
def wrap_beta(x, shape1, shape2):
    return stats.beta.logpdf(x, shape1, shape2)

def wrap_gamma(x, shape, scale):
    return stats.gamma.logpdf(x, shape, scale=scale)

def wrap_lognorm(x, meanlog, sdlog):
    # https://stats.stackexchange.com/questions/33036/fitting-log-normal-distribution-in-r-vs-scipy
    return stats.lognorm.logpdf(x, sdlog, scale=np.exp(meanlog))

def wrap_norm(x, mean, sd):
    return stats.norm.logpdf(x, loc=mean, scale=sd)

class Parameter:
    def __init__(self, init, dist, par1, par2):
        ## We pad the support of prior distributions to exclude values near
        ## finite boundaries. The distributions typically have log density
        ## of -inf at their boundaries, which can cause some otherwise fast
        ## optimization methods to fail.
        self.padding = 1e-10

        self.initial_value = init
        self.prior_name = dist
        self.parameter1 = par1
        self.parameter2 = par2
        self.fitted_value = np.nan # placeholder

        match dist:
            case CONST.DIST_BETA:
                self._prior = wrap_beta
                self.support = (self.padding, 1.0 - self.padding)
            case CONST.DIST_GAMMA:
                self._prior = wrap_gamma
                self.parameter2 = 1.0 / par2 # convert rate to scale
                self.support = (self.padding, +np.inf)
            case CONST.DIST_LOGNORMAL:
                self._prior = wrap_lognorm
                self.support = (self.padding, +np.inf)
            case CONST.DIST_NORMAL:
                self._prior = wrap_norm
                self.support = (-np.inf, +np.inf)
            case _:
                raise ValueError('Unrecognized probability distribution %s' % (dist))
    
    def prior(self, theta):
        return self._prior(theta, self.parameter1, self.parameter2)

class GoalsFitter:
    def __init__(self, par_xlsx, anc_csv, hiv_csv):
        self.init_hivsim(par_xlsx)
        self.init_data_anc(anc_csv)
        self.init_data_hiv(hiv_csv)
        self.init_fitting(par_xlsx)

    def init_hivsim(self, par_xlsx):
        self.hivsim = Goals.Model()
        self.hivsim.init_from_xlsx(par_xlsx)
        self.year_first = self.hivsim.year_first
        self.year_final = self.hivsim.year_final
        self.year_range = range(0, self.year_final - self.year_first + 1)

    def init_data_anc(self, anc_csv):
        self._ancdat = ancprev.ancprev(self.year_first)
        self._ancdat.read_csv(anc_csv)

    def init_data_hiv(self, hiv_csv):
        self._hivdat = hivprev.hivprev(self.year_first)
        self._hivdat.read_csv(hiv_csv)
        self._hivest = self._hivdat.projection_template()

    def init_fitting(self, par_xlsx):
        # Setting data_only=True lets the fitter use the calculated value of Excel
        # equations. This way the FittingInputs sheet can automatically pull values
        # from other input tabs.
        wb = xlsx.load_workbook(filename=par_xlsx, read_only=True, data_only=True)
        par_dict = Utils.xlsx_load_fitting_pars(wb[CONST.XLSX_TAB_FITTING])
        wb.close()

        # Create Parameter objects out of the parameter data. Drop parameters 
        # that the user has indicated should not be fitted
        self._pardat = {key : Parameter(val[0], val[1], val[2], val[3]) for key, val in par_dict.items() if val[4] != False}

        # Several methods need to refer to parameter values stored in an array,
        # without corresponding metadata. We keep a sorted list of keys so that
        # these values can be used appropriately.
        self._par_keys = sorted(self._pardat.keys())

    def prior(self, params):
        """! Prior density on log scale """
        return sum([self._pardat[key].prior(params[idx]) for idx, key in enumerate(self._par_keys)])

    def likelihood(self, params):
        """! Log-likelihood """
        self.project(params)
        self._ancest = self.hivsim.births_exposed / self.hivsim.births.sum((1))
        fill_hivprev_template(self.hivsim, self._hivest)
        lhood_hiv = self._hivdat.likelihood(self._hivest)
        lhood_anc = self._ancdat.likelihood(self._ancest)
        print("%0.2f %0.2f\t%s" % (lhood_hiv, lhood_anc, params))
        return lhood_hiv + lhood_anc

    def posterior(self, params):
        """"! Posterior density on log scale """
        return self.prior(params) + self.likelihood(params)
    
    def project(self, params):
        """! Set fitting parameter values into the model then run a projection """
        # TODO: Move the parameter setting code into its own code so that it can
        # be benchmarked.
        # TODO: replace this looped case statement with a dictionary from keys to
        # functions that set the specific parameter. That should be populated
        # in self.__init__. Check if this helps with speed at all.
        for idx, key in enumerate(self._par_keys):
            match key:
                case CONST.FIT_INITIAL_PREV:
                    self.hivsim.epi_pars[CONST.EPI_INITIAL_PREV] = params[idx]
                case CONST.FIT_TRANSMIT_F2M:
                    self.hivsim.epi_pars[CONST.EPI_TRANSMIT_F2M] = params[idx]
                case CONST.FIT_TRANSMIT_M2F:
                    self.hivsim.epi_pars[CONST.EPI_TRANSMIT_M2F] = params[idx]
                case CONST.FIT_LT_PARTNER_F:
                    self.hivsim.partner_time_trend[CONST.SEX_FEMALE,:] = params[idx]
                case CONST.FIT_LT_PARTNER_M:
                    self.hivsim.partner_time_trend[CONST.SEX_MALE,  :] = params[idx]
                case CONST.FIT_PARTNER_AGE_MEAN_F:
                    self.hivsim.partner_age_params[0,CONST.SEX_FEMALE] = (80.0 - 15.0) * params[idx] + 15.0
                case CONST.FIT_PARTNER_AGE_MEAN_M:
                    self.hivsim.partner_age_params[0,CONST.SEX_MALE  ] = (80.0 - 15.0) * params[idx] + 15.0
                case CONST.FIT_PARTNER_AGE_SCALE_F:
                    self.hivsim.partner_age_params[1,CONST.SEX_FEMALE] = params[idx]
                case CONST.FIT_PARTNER_AGE_SCALE_M:
                    self.hivsim.partner_age_params[1,CONST.SEX_MALE  ] = params[idx]
                case CONST.FIT_PARTNER_POP_FSW:
                    self.hivsim.partner_pop_ratios[CONST.POP_FSW-1,CONST.SEX_FEMALE] = params[idx] # subtract 1 since partner_pop_ratios starts at POP_NEVER=1 instead of POP_NOSEX=0
                case CONST.FIT_PARTNER_POP_CLIENT:
                    self.hivsim.partner_pop_ratios[CONST.POP_CSW-1,CONST.SEX_MALE  ] = params[idx]
                case CONST.FIT_HIV_FRR_LAF:
                    self.hivsim.hiv_frr['laf'] = params[idx]
                case CONST.FIT_ANCSS_BIAS:
                    self.hivsim.likelihood_par[CONST.LHOOD_ANCSS_BIAS] = params[idx]
                case CONST.FIT_ANCRT_BIAS:
                    self.hivsim.likelihood_par[CONST.LHOOD_ANCRT_BIAS] = params[idx]
                case CONST.FIT_VARINFL_SITE:
                    self.hivsim.likelihood_par[CONST.LHOOD_VARINFL_SITE] = params[idx]
                case CONST.FIT_VARINFL_CENSUS:
                    self.hivsim.likelihood_par[CONST.LHOOD_VARINFL_CENSUS] = params[idx]
                case _:
                    raise ValueError('Unrecognized parameter %s' % (key))
        
        ## TODO: could skip these calls if none of the constituent inputs are being varied
        self.hivsim._proj.init_transmission(
                self.hivsim.epi_pars[CONST.EPI_TRANSMIT_F2M],
                self.hivsim.epi_pars[CONST.EPI_TRANSMIT_M2F],
                self.hivsim.epi_pars[CONST.EPI_TRANSMIT_M2M],
                self.hivsim.epi_pars[CONST.EPI_TRANSMIT_PRIMARY],
                self.hivsim.epi_pars[CONST.EPI_TRANSMIT_CHRONIC],
                self.hivsim.epi_pars[CONST.EPI_TRANSMIT_SYMPTOM],
                self.hivsim.epi_pars[CONST.EPI_TRANSMIT_ART_VS],
                self.hivsim.epi_pars[CONST.EPI_TRANSMIT_ART_VF])
        self.hivsim._proj.init_epidemic_seed(self.hivsim.epi_pars[CONST.EPI_INITIAL_YEAR] - self.year_first,
                                             self.hivsim.epi_pars[CONST.EPI_INITIAL_PREV])

        self.hivsim.partner_rate[:] = self.hivsim.calc_partner_rates(self.hivsim.partner_time_trend,
                                                                     self.hivsim.partner_age_params,
                                                                     self.hivsim.partner_pop_ratios)
        
        frr_age = self.hivsim.hiv_frr['age'] * self.hivsim.hiv_frr['laf']
        frr_cd4 = self.hivsim.hiv_frr['cd4']
        frr_art = self.hivsim.hiv_frr['art'] * self.hivsim.hiv_frr['laf']
        self.hivsim._proj.init_hiv_fertility(frr_age[self.year_range,:], frr_cd4, frr_art)

        self._ancdat.set_parameters(self.hivsim.likelihood_par[CONST.LHOOD_ANCSS_BIAS],
                                    self.hivsim.likelihood_par[CONST.LHOOD_ANCRT_BIAS],
                                    self.hivsim.likelihood_par[CONST.LHOOD_VARINFL_SITE],
                                    self.hivsim.likelihood_par[CONST.LHOOD_VARINFL_CENSUS])
    

        pop_ratios_all = pd.read_csv("C:\Proj\Repositories\GoalsARMPython\inputs\\num_partners_sensitivity.csv",header = None)
        for iter in range(33):  
        #print(iter)
            pop_ratios = pop_ratios_all.iloc[iter]
            pop_ratios =  pop_ratios.to_numpy()
            pop_ratios = np.append(pop_ratios,np.nan)
            pop_ratios =  np.reshape(pop_ratios, (7,2))
     
            self.hivsim.partner_pop_ratios = pop_ratios
            print(self.hivsim.partner_pop_ratios)
            self.hivsim.partner_rate[:] = self.hivsim.calc_partner_rates(self.hivsim.partner_time_trend,
                                                                        self.hivsim.partner_age_params,
                                                                        self.hivsim.partner_pop_ratios)

        
            ## TODO: could skip invalidation if only ANC likelihood parameters are being varied
            self.hivsim.invalidate(-1) # needed so that Goals will recalculate the projection
            self.hivsim.project(self.year_final)

             ## Save and output infections and prevalence before full calibration
            new_infections = np.sum(self.hivsim.new_infections, axis=(2))[:,:,7]
            dt = pd.DataFrame(new_infections, columns = ['female','male','male_c'])
            dt['pop']='POP_TGW'
            new_col = range(1970,self.year_final+1)
            dt['year'] = new_col


            for i in range(7):
                new_infections = np.sum(self.hivsim.new_infections, axis=(2))[:,:,i]

                df2 = pd.DataFrame(new_infections, columns = ['female','male','male_c'])
                df2['year'] = new_col
                df2['iter'] = iter
                if i == 0:
                    df2['pop']= 'POP_NOSEX'
                if i == 1:
                    df2['pop']=  'POP_NEVER'
                if i == 2:
                    df2['pop']=  'POP_UNION'
                if i == 3:
                    df2['pop']= 'POP_SPLIT'
                if i == 4:
                    df2['pop']=  'POP_PWID'
                if i == 5:
                    df2['pop']=  'POP_FSW_CFSW'
                if i == 6:
                    df2['pop']=  'POP_MSM'
                dt = pd.concat([dt, df2])
            
            name_out = "C:\Proj\Repositories\GoalsARMPython\outputs\sensitivity\\num_partners\infections_" + str(iter) + ".csv"
            dt.to_csv(name_out, index=False)

        test_same_sex_var(self.hivsim, "C:\Proj\Repositories\GoalsARMPython\inputs\same_sex_var_sensitivity.csv",self.year_final)
        test_mixing_weight(self.hivsim, "C:\Proj\Repositories\GoalsARMPython\inputs\mixing_weight_sensitivity.csv",self.year_final)
            
    def calibrate(self, method='Nelder-Mead'):
        """! Calibrate the model to ANC and HIV prevalence data
        @param method see scipy.optimize.minimize. Only methods that allow bounds can be used.
        @return a dictionary that lists the fitted parameters with their final values
        @return the diagnostic object returned by scipy optimize
        """
        bounds = optimize.Bounds(lb = [self._pardat[key].support[0] for key in self._par_keys],
                                 ub = [self._pardat[key].support[1] for key in self._par_keys])
        p_init = np.array([self._pardat[key].initial_value for key in self._par_keys])
        optres = optimize.minimize(lambda p : -self.posterior(p), p_init, method=method, bounds=bounds)
        p_best = optres.x

        for i in range(len(self._par_keys)):
            self._pardat[self._par_keys[i]].fitted_value = p_best[i]

        return self._pardat, optres

def main(par_file, anc_file, hiv_file):
    Fitter = GoalsFitter(par_file, anc_file, hiv_file)
    pars, diag = Fitter.calibrate(method='Nelder-Mead')

    ## Use only if testing mixing weights - no need to recalibrate the whole model
   

    ## TODO: The outro below violates encapsuation by accessing "private"
    ## data in _ancdat and _hivdat (drop "_", or move the plot methods into
    ## Fitter?) and by calling the Fitter.likelihood(...) method, which
    ## relies on using implementation details gleaned from diag that the 
    ## caller should not know or care about.
    print("+=+ Fitting complete +=+")
    print({key : val.fitted_value for key, val in pars.items()})
    print("%d likelihood evaluations" % (diag.nfev))
    print("Converged: %s" % (diag.success))
    print(Fitter.likelihood(diag.x))
    plot_fit_anc(Fitter.hivsim, Fitter._ancdat, "ancfit.tiff")
    plot_fit_hiv(Fitter.hivsim, Fitter._hivdat, "hivfit.tiff")

if __name__ == "__main__":
    sys.stderr.write("Process %d\n" % (os.getpid()))
    time_start = time.time()
    if len(sys.argv) == 1:
        par_file = "inputs/mwi-2023-inputs.xlsx"
        anc_file = "inputs/mwi-2023-anc-prev.csv"
        hiv_file = "inputs/mwi-2023-hiv-prev.csv"
        main(par_file, anc_file, hiv_file)
    elif len(sys.argv) < 3:
        sys.stderr.write("USAGE: %s <input_param>.xlsx <anc_data>.csv <hiv_data>.csv" % (sys.argv[0]))
    else:
        par_file = sys.argv[1]
        anc_file = sys.argv[2]
        hiv_file = sys.argv[3]
        main(par_file, anc_file, hiv_file)
    print("Completed in %s seconds" % (time.time() - time_start))
