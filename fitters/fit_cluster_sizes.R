library(reticulate)
library(spatialwarnings)

results_path = "C://Code//Github//vegetation-dynamics//results"
model = "tricritical"
dataset = "100x100_final"

options(spatialwarnings.constants.reltol = 1e-6)
options(spatialwarnings.constants.maxit = 1e8)

# q_folder = "q0"
# q_value = "0"
# p_values = c("0p616", "0p618", "0p62", "0p625", "0p63", "0p64", "0p65", "0p7", "0p72", "0p73", "0p74")
#p_values = c("0p65")

# q_folder = "q0p25"
# q_value = "0p25"
# p_values = c("0p566", "0p569", "0p57", "0p575", "0p58", "0p59", "0p62", "0p64", "0p65", "0p66")

# q_folder = "q0p5"
# q_value = "0p5"
# p_values = c("0p498", "0p5", "0p502", "0p504", "0p506", "0p508", "0p51", "0p52", "0p53", "0p55", "0p56", "0p57")

q_folder = "q0p75"
q_value = "0p75"
p_values = c("0p399", "0p4", "0p401", "0p403", "0p405", "0p41", "0p42", "0p43", "0p44")

root_path = file.path(results_path, model, q_folder, dataset)
data_frame = data.frame()

for (p in p_values) {
  print(paste("<--- Analyzing", p, "--->"))
  
  file_name = paste("tricritical_", p, "_", q_value, ".pkl", sep="")
  file_path = file.path(root_path, file_name)
  source_python("lattice_parser.py")
  lattices = load_lattices(file_path)
  
  psd_object = patchdistr_sews(lattices, best_by = "BIC", fit_lnorm = FALSE, merge = TRUE, wrap = TRUE)
  psd_stats = psd_object$psd_type
  
  psd_plot = plot_distr(psd_object, best_only = FALSE)
  png(filename=paste(p, "_", q_folder, ".png", sep = ""))
  plot(psd_plot)
  dev.off()
  
  pl_bic = psd_stats$BIC[1]
  tpl_bic = psd_stats$BIC[2]
  exp_bic = psd_stats$BIC[3]
  
  print(paste("Power law BIC:", pl_bic))
  print(paste("TPL BIC:", tpl_bic))
  print(paste("Exp BIC:", exp_bic))
  
  data_frame = rbind(data_frame, c(p, pl_bic, tpl_bic, exp_bic))
}

colnames(data_frame)[1] = "p"
colnames(data_frame)[2] = "PL"
colnames(data_frame)[3] = "TPL"
colnames(data_frame)[4] = "Exp"

write.csv(data_frame, paste(q_folder, "_csd", ".csv", sep=""))