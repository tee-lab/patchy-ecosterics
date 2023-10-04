calc_bic <- function(fit_output, data_len) {
  bic = fit_output$npars * log(data_len) - 2 * (fit_output$ll)
  return(bic)
}

library(reticulate)
library(spatialwarnings)

results_path = "C://Code//Github//vegetation-dynamics//results"
model = "tricritical"
dataset = "100x100_residue"

q_folder = "q0"
p_values = c("0p65") # ideal for debugging
# p_values = c("0p616", "0p618", "0p62", "0p625", "0p63", "0p64", "0p65", "0p7", "0p72")

# q_folder = "q0p25"
# p_values = c("0p566", "0p568", "0p57", "0p575", "0p58", "0p59", "0p62", "0p64")

# q_folder = "q0p5"
# p_values = c("0p498", "0p5", "0p502", "0p504", "0p506", "0p508", "0p51", "0p52", "0p53", "0p55")
  
# q_folder = "q0p75"
# p_values = c("0p399", "0p4", "0p401", "0p403", "0p405", "0p41", "0p42")

data_frame = data.frame()

root_path = file.path(results_path, model, q_folder, dataset)

for (p in p_values) {
  print(paste("<--- Analyzing", p, "--->"))
  
  # load data
  file_name = paste(p, "_changes.txt", sep="")
  file_path = file.path(root_path, p, file_name)
  source_python("load_changes.py")
  changes_icdf = load_changes(file_path)
  
  # format data
  x_start = 3 # remove first two points corresponding to ds = 0, and ds = +/- 1
  x_range = x_start:length(changes_icdf)
  changes_icdf = changes_icdf[x_start:length(changes_icdf)]
  data_len = length(changes_icdf)
  norm_factor = sum(changes_icdf)
  plot(x_range, changes_icdf, main=paste("cd of", p, "- normal scale"))
  
  # fit exp
  exp_output = exp_fit(changes_icdf)
  b = exp_output$cutoff
  plot(x_range, log(changes_icdf / norm_factor), main=paste("cd of", p, "- semilogy plot + exp fit"))
  plot(x_range, -b * x_range, main="Separate exp fit")
  
  # fit power-law
  pl_output = pl_fit(changes_icdf)
  exponent = pl_output$plexpo
  plot(log(x_range), log(changes_icdf / norm_factor), main=paste("cd of", p, "- log log plot + pl fit"))
  lines(log(x_range), log(x_range ^ -exponent), main="pl fit")
  
  # fit tpl
  tpl_output = tpl_fit(changes_icdf)
  exponent = tpl_output$plexpo
  b = tpl_output$cutoff
  plot(log(x_range), log(changes_icdf / norm_factor), main=paste("cd of", p, "- log log plot + tpl fit"))
  lines(log(x_range), log((x_range ^ -exponent) * exp(-b * x_range)), main="tpl fit")
  
  # calculate BIC values
  pl_bic = calc_bic(pl_output, data_len)
  tpl_bic = calc_bic(tpl_output, data_len)
  exp_bic = calc_bic(exp_output, data_len)
  
  print(paste("Power-law BIC:", pl_bic))
  print(paste("Truncated Power-law BIC:", tpl_bic))
  print(paste("Exponential BIC:", exp_bic))
  
  # append to data frame
  data_frame = rbind(data_frame, c(p, pl_bic, tpl_bic, exp_bic))
}

colnames(data_frame)[1] = "p"
colnames(data_frame)[2] = "PL"
colnames(data_frame)[3] = "TPL"
colnames(data_frame)[4] = "Exp"

# save BIC values as CSV
write.csv(data_frame, paste(q_folder, "_cd", ".csv", sep=""))