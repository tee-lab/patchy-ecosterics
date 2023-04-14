calc_bic <- function(fit_output, data_len) {
  bic = fit_output$npars * log(data_len) - 2 * (fit_output$ll)
  return(bic)
}

library(reticulate)
library(spatialwarnings)

results_path = "C://Code//Github//vegetation-dynamics//results"
model = "tricritical"
q_folder = "q0p25"
dataset = "100x100"

q_value = "0"
# p_values = c('0p62', '0p63', '0p64', '0p65', '0p66', '0p67', '0p68', '0p69', '0p7', '0p71', '0p72')
p_values = c('0p57', '0p58', '0p59', '0p6', '0p61', '0p62', '0p63', '0p64', '0p65')
# p_values = c('0p5', '0p51', '0p52', '0p53', '0p54', '0p55', '0p56', '0p57')

root_path = file.path(results_path, model, q_folder, dataset)

for (p in p_values) {
  print(paste("<--- Analyzing", p, "--->"))
  folder_path = file.path(root_path, p)
  file_name = paste(p, "_cluster_distribution.txt", sep="")
  file_path = file.path(folder_path, file_name)
  data = read.table(file_path)[,-1]
  cluster_distribution = data[2:length(data)]
  data_len = length(cluster_distribution)
  
  pl_output = pl_fit(cluster_distribution)
  tpl_output = tpl_fit(cluster_distribution)
  exp_output = exp_fit(cluster_distribution)
  
  pl_bic = calc_bic(pl_output, data_len)
  tpl_bic = calc_bic(tpl_output, data_len)
  exp_bic = calc_bic(exp_output, data_len)
  
  print(paste("Power-law BIC:", pl_bic))
  print(paste("Truncated Power-law BIC:", tpl_bic))
  print(paste("Exponential BIC:", exp_bic))
}