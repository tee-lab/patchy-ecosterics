calc_bic <- function(fit_output, data_len) {
  bic = fit_output$npars * log(data_len) - 2 * (-fit_output$ll)
  return(bic)
}

library(reticulate)
library(spatialwarnings)

results_path = "C://Code//Github//vegetation-dynamics//results"
model = "tricritical"
q_folder = "q0"
dataset = "100x100"

q_value = "0"
p_values = c("0p65", "0p7", "0p72", "0p74")

root_path = file.path(results_path, model, q_folder, dataset)

for (p in p_values) {
  print(paste("<--- Analyzing", p, "--->"))
  
  file_name = paste(p, "_changes.txt", sep="")
  file_path = file.path(root_path, p, file_name)
  source_python("load_changes.py")
  changes_icdf = load_changes(file_path)
  
  x_start = 3
  x_range = 3:length(changes_icdf)
  changes_icdf = changes_icdf[3:length(changes_icdf)]
  data_len = length(changes_icdf)
  
  pl_output = pl_fit(changes_icdf)
  tpl_output = tpl_fit(changes_icdf)
  exp_output = exp_fit(changes_icdf)
  
  pl_bic = calc_bic(pl_output, data_len)
  tpl_bic = calc_bic(tpl_output, data_len)
  exp_bic = calc_bic(exp_output, data_len)
  
  print(paste("Power-law BIC:", pl_bic))
  print(paste("Truncated Power-law BIC:", tpl_bic))
  print(paste("Exponential BIC:", exp_bic))
}