
library(data.table)
library(ggplot2)
library(readxl)
library(dplyr)
library(ggridges)

setwd("C:/Proj/Repositories/GoalsARMPython/")


#######################
### MIXING WEIGHTS ###
#####################

set_values = fread("inputs/mixing_weight_sensitivity.csv")
colnames(set_values) = c("POP_NEVER_F","POP_UNION_F",
                         "POP_SPLIT_F","POP_PWID_F",
                         "POP_FSW_CFSW_F","POP_MSM_F","POP_TGX_F",
                          "POP_NEVER_M","POP_UNION_M",
                          "POP_SPLIT_M","POP_PWID_M",
                          "POP_FSW_CFSW_M","POP_MSM_M","POP_TGX_M")
key = fread("outputs/sensitivity/mixing_weights/key.csv")

dt = list()
for(i in 0:60){
  d1 = fread(paste0("outputs/sensitivity/mixing_weights/infections_",i,".csv"))
  d1[,iter := i]
  dt <- rbind(dt,d1)
}


dt = dt[year %in% 1990:2023]
dt_m = melt(dt, id.vars = c("iter","pop","year"))
setnames(dt_m, c("variable","value"),c("sex","new_inf"))

dt_m = merge(dt_m, key, by = "iter",allow.cartesian = T)

yr = 2020

pdf("outputs/sensitivity/mixing_weights/plots/infections_by_pop.pdf",height = 8, width = 10)
for(yr in c(2000,2010,2020)){
#Population specific infections
  gg1 = ggplot(dt_m[year == yr & sex != "male_c" & sex == "female"  & grepl("F",param) & param != "POP_FSW_CFSW_M"], aes(param_value, new_inf, col=param)) + 
              geom_line() + labs(x = "Mixing weight (%)", y = "New Infections") +
              facet_wrap(~pop , scale="free_y") + theme_bw() +
              scale_color_discrete(name = "Population weight \n being varied") +
              theme(legend.position = "bottom") + 
              ggtitle(paste0("Females year ",yr," (female weights)"))
  
  gg2 = ggplot(dt_m[year == yr & sex != "male_c" & sex == "female"  & grepl("M",param)], aes(param_value, new_inf, col=param)) + 
    geom_line() + labs(x = "Mixing weight (%)", y = "New Infections") +
    facet_wrap(~pop , scale="free_y") + theme_bw() +
    scale_color_discrete(name = "Population weight \n being varied") +
    theme(legend.position = "bottom") + 
    ggtitle(paste0("Females year ",yr," (male weights)"))
  
  gg3 =  ggplot(dt_m[year == yr & sex != "male_c" & 
                       sex == "male" & grepl("_M",param) & iter != 0], 
                aes(param_value, new_inf, col=param)) + 
    geom_line() + labs(x = "Mixing weight (%)", y = "New Infections") +
    facet_wrap(~pop , scale="free_y") + theme_bw() +
    scale_color_discrete(name = "Population weight \n being varied") +
    theme(legend.position = "bottom") + 
    ggtitle(paste0("Males year ",yr," (female weights)"))
  
  gg4 =  ggplot(dt_m[year == yr & sex != "male_c" & 
                       sex == "male" & grepl("_M",param) & iter != 0], 
                aes(param_value, new_inf, col=param)) + 
    geom_line() + labs(x = "Mixing weight (%)", y = "New Infections") +
    facet_wrap(~pop , scale="free_y") + theme_bw() +
    scale_color_discrete(name = "Population weight \n being varied") +
    theme(legend.position = "bottom") + 
    ggtitle(paste0("Males year ",yr," (male weights)"))
  print(gg1); print(gg2); print(gg3); print(gg4)
}
dev.off()

#Sum of infections
dt_m[,weight := "female_weight"]
dt_m[grepl("_M",param), weight := "male_weight"]

dt_sum = dt_m %>% 
  group_by(sex, param, param_value,year,iter,weight) %>% 
  summarise(new_inf = sum(new_inf)) %>% data.table()  

pdf("outputs/sensitivity/mixing_weights/plots/total_infections.pdf",height = 8, width = 10)
for(yr in c(2000,2010,2020)){
  g1 = ggplot(dt_sum[year == yr & sex != "male_c" & weight == "female_weight"], aes(param_value, new_inf, col = param)) +
      facet_wrap(~sex) + 
      geom_line() + 
      theme_bw()  +
      scale_color_discrete(name = "Population weight \n being varied") +
      labs(y = "Total new infections", x = "Mixing weight (%)", 
           title =  paste0("year ",yr," Female weights"))
                                                             
  g2 = ggplot(dt_sum[year == yr & iter != 0 & sex != "male_c" & weight == "male_weight"], aes(param_value, new_inf, col = param)) +
    facet_wrap(~sex) + 
    geom_line() + 
    theme_bw()  +
    scale_color_discrete(name = "Population weight \n being varied") +
    labs(y = "Total new infections", x = "Mixing weight (%)",
              title = paste0("year ",yr," Male weights"))
  
  print(gridExtra::grid.arrange(g1,g2))
}
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
test1[Year %in% 5:10 & Risk == 1 & Sex == 0]
