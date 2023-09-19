
library(data.table)
library(ggplot2)
library(readxl)
library(dplyr)
library(ggridges)

setwd("C:/Proj/Repositories/GoalsARMPython/")


#########################
### Same Sex Variance ###
########################

set_values = fread("inputs/same_sex_var_sensitivity.csv")
colnames(set_values) = c("hetero_mean","heter_var","same_sex_var")
key = fread("outputs/sensitivity/same_sex_var/key.csv")

dt = list()
for(i in 0:14){
  d1 = fread(paste0("outputs/sensitivity/same_sex_var/infections_",i,".csv"))
  d1[,iter := i]
  dt <- rbind(dt,d1)
}


#dt = dt[year %in% 1990:2023]
dt_m = melt(dt, id.vars = c("iter","pop","year"))
setnames(dt_m, c("variable","value"),c("sex","new_inf"))

dt_m = merge(dt_m, key, by = "iter",allow.cartesian = T)

yr = 2020

pdf("outputs/sensitivity/same_sex_var/plots/infections_by_pop.pdf",height = 8, width = 10)
#Population specific infections
  gg1 = ggplot(dt_m[year %in% c(1980,1990,2000,2010,2020) & sex != "male_c" & sex == "female"]  , aes(param_value, new_inf, col=factor(year))) + 
              geom_line() + labs(x = "Same-sex variance value", y = "New Infections") +
              facet_wrap(~pop , scale="free_y") + theme_bw() +
              scale_color_discrete(name = "Year") +
              theme(legend.position = "bottom") + 
              ggtitle(paste0("Females"))
  
  gg2 = ggplot(dt_m[year %in% c(1980,1990,2000,2010,2020) & sex != "male_c" & sex == "male"]  , aes(param_value, new_inf, col=factor(year))) + 
    geom_line() + labs(x = "Same-sex variance value", y = "New Infections") +
    facet_wrap(~pop , scale="free_y") + theme_bw() +
    scale_color_discrete(name = "Year") +
    theme(legend.position = "bottom") + 
    ggtitle(paste0("Males"))
  
  print(gg1); print(gg2)

dev.off()

#Sum of infections

dt_sum = dt_m %>% 
  group_by(sex, param, param_value,year,iter) %>% 
  summarise(new_inf = sum(new_inf)) %>% data.table()  

pdf("outputs/sensitivity/same_sex_var/plots/total_infections.pdf",height = 8, width = 10)
  g1 = ggplot(dt_sum[year %in% c(1990,2000,2010,2020) & sex != "male_c" ], aes(param_value, new_inf)) +
      facet_grid(year~sex ) + 
      geom_line() + 
      theme_bw()  +
      labs(y = "Total new infections",
           x = "Same-sex variance value",)

  print(g1)

dev.off()

#Infections time series
#t might be good to have another set of graphs where colors correspond to selected years (1980, 1990, 2000, 2010, 2020?) with one graph per parameter and sex. That would need to be normalized somehow so that the peak epidemic years don't wipe out the scale 
params = unique(dt_m$param)
pdf("outputs/sensitivity/mixing_weights/plots/infections_by_year.pdf",height = 8, width = 10)
for(i in 1:length(params)){
  for(ss in unique(dt_m$sex)){
    gg = ggplot(dt_m[year %in% c(1980,1990,2000,2010,2020) & sex == ss & param == params[i]], aes(param_value, new_inf, col=factor(year))) + 
      geom_line() +
      labs(x = "Mixing weight (%)", y = "New Infections", title = paste0(toupper(ss)," infections\nPop mixing weight varied: ",params[i])) +
      facet_wrap(~pop , scale="free_y") + theme_bw() +
      theme(legend.position = "bottom")  
    print(gg)
  }
}
dev.off()

test1  = fread("new-hiv.csv")
test1 = test1 %>% group_by(Year, Sex, Risk) %>% summarise(val = sum(Value)) %>% data.table()
test1[Year %in% 0:10 & Risk == 1 & Sex == 0]
