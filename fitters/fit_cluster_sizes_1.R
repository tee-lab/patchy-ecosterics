load("MLE fit and comparison template.RData")
library(ggplot2)
library(grid)
library(poweRlaw)

results_path = "C://Code//Github//vegetation-dynamics//results"
model = "tricritical"
q_value = "q0"
dataset = "100x100"
folders = c("0p65", "0p7", "0p72", "0p74")

root_path = file.path(results_path, model, q_value, dataset)

for (i in 1:length(folders)) {
  # construct path
  folder = folders[i]
  file_name = paste(folder, "_cluster_distribution.txt", sep="")
  file_path = file.path(root_path, folder, file_name)
  print(paste("<---","Analyzing p =", folder, "--->"))
  
  # read distribution
  cluster_distribution = read.table(file_path)
  cluster_distribution = cluster_distribution[-1,]
  data_length = length(cluster_distribution$V1)
  biggest_cluster_size = max(cluster_distribution$V1)
  
  # construct inverse cdf
  inverse_cdf = numeric(length=data_length)
  for (j in 1:biggest_cluster_size) {
    inverse_cdf[j] = sum(cluster_distribution$V2[j:biggest_cluster_size])
  }
  
  # power law fit distribution object
  pl_fit = displ$new(as.numeric(inverse_cdf))
  pl_xmin = estimate_xmin(pl_fit)
  pl_fit$setXmin(pl_xmin)
  pl_pars = estimate_pars(pl_fit)
  pl_fit$setPars(pl_pars$pars)
  
  # exp fit distribution object
  exp_fit = disexp(as.numeric(inverse_cdf))
  exp_xmin = estimate_xmin(exp_fit)
  exp_fit$setXmin(pl_xmin)
  exp_pars = estimate_pars(exp_fit)
  exp_fit$setPars(exp_pars$pars)
  
  # lnorm fit distribution object
  lnorm_fit = dislnorm(as.numeric(inverse_cdf))
  lnorm_xmin = estimate_xmin(lnorm_fit)
  lnorm_fit$setXmin(pl_xmin)
  lnorm_pars = estimate_pars(lnorm_fit)
  lnorm_fit$setPars(lnorm_pars$pars)
  
  # compare power law and exponential fits
  print("Comparing power-law and exp fits")
  com_pl_exp = compare_distributions(pl_fit, exp_fit)
  print(paste("p2:", com_pl_exp$p_two_sided))
  print(paste("p1:", com_pl_exp$p_one_sided))
  
  # compare power law and lnorm fits
  print("Comparing power-law and lnorm fits")
  com_pl_lnorm = compare_distributions(pl_fit, lnorm_fit)
  print(paste("p2:", com_pl_lnorm$p_two_sided))
  print(paste("p1:", com_pl_lnorm$p_one_sided))
  
  # compare exp and lnorm fits
  print("Comparing exp and lnorm fits")
  com_exp_lnorm = compare_distributions(exp_fit, lnorm_fit)
  print(paste("p2:", com_exp_lnorm$p_two_sided))
  print(paste("p1:", com_exp_lnorm$p_one_sided))
  
  # make best fits
  #pl_best_fit = pareto.exp.llr(as.numeric(inverse_cdf), pl_xmin, exp_xmin)
  # ple_best_fit = discpowerexp.fit(as.numeric(inverse_cdf), pl_xmin$xmin)
  
  # compare power-law and power-law with exp cutoff fits
  # power.powerexp.lrt(pl_best_fit, ple_best_fit)
}