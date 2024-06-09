library(reticulate)
library(spatialwarnings)

results_path = "C://Code//Github//vegetation-dynamics//results"
# model = "tricritical"
model = "tricritical"
dataset = "paper"

options(spatialwarnings.constants.reltol = 1e-8)
options(spatialwarnings.constants.maxit = 1e8)

# q_folder = "q0"
# q_value = "0"
# p_values = c("0p616", "0p618", "0p62", "0p625", "0p63", "0p64", "0p65", "0p7", "0p72", "0p74")
# p_values = c("0p65")

# q_folder = "q0p25"
# q_value = "0p25"
# p_values = c("0p566", "0p569", "0p57", "0p575", "0p58", "0p59", "0p62", "0p64", "0p65", "0p66")

# q_folder = "q0p5"
# q_value = "0p5"
# p_values = c("0p498", "0p5", "0p502", "0p504", "0p506", "0p508", "0p51", "0p52", "0p53", "0p54", "0p55", "0p57")

# q_folder = "q0p75"
# q_value = "0p75"
# p_values = c("0p399", "0p4", "0p401", "0p403", "0p405", "0p41", "0p42", "0p43", "0p44")

q_folder = "q0p92"
q_value = "0p92"
p_values = c("0p282", "0p283", "0p284", "0p285", "0p29")

root_path = file.path(results_path, model, dataset)
data_frame = data.frame()

# rainfall_values = c("300", "400", "500", "600", "700", "770", "830", "850", "900")

if (model == "tricritical") {
  values = p_values
  root_path = file.path(results_path, model, q_folder, dataset)
} else {
  values = rainfall_values
  root_path = file.path(results_path, model, dataset)
}

for (p in values) {
  print(paste("<--- Analyzing", p, "--->"))
  
  file_name = paste(p, "_final_lattices.pkl", sep="")
  file_path = file.path(root_path, p, file_name)
  source_python("lattice_parser.py")
  lattices = load_lattices(file_path)
  
  psd_object = patchdistr_sews(lattices, best_by = "BIC", fit_lnorm = FALSE, merge = TRUE, wrap = TRUE)
  psd_stats = psd_object$psd_type
  
  psd_plot = plot_distr(psd_object, best_only = FALSE)
  
  if (model == "tricritical") {
    png(filename=paste(p, "_", q_folder, ".png", sep = ""))
  } else {
    png(filename=paste(p, ".png", sep = ""))
  }
  
  plot(psd_plot)
  dev.off()
  
  pl_bic = psd_stats$BIC[1]
  tpl_bic = psd_stats$BIC[2]
  exp_bic = psd_stats$BIC[3]
  
  pl_expo = psd_stats$plexpo[1]
  exp_trunc = psd_stats$cutoff[3]
  tpl_expo = psd_stats$plexpo[2]
  tpl_trunc = psd_stats$cutoff[2]
  
  print(paste("Power law BIC:", pl_bic))
  print(paste("TPL BIC:", tpl_bic))
  print(paste("Exp BIC:", exp_bic))
  
  if (model == "tricritical") {
    p_float = as.double(gsub("p", ".", p))
  } else {
    p_float = as.integer(p)
  }
  
  data_frame = rbind(data_frame, c(p_float, pl_bic, tpl_bic, exp_bic, pl_expo, exp_trunc, tpl_expo, tpl_trunc))
}

if (model == "tricritical") {
  colnames(data_frame)[1] = "p"
} else {
  colnames(data_frame)[1] = "rainfall"
}

colnames(data_frame)[2] = "PL"
colnames(data_frame)[3] = "TPL"
colnames(data_frame)[4] = "Exp"
colnames(data_frame)[5] = "PL expo"
colnames(data_frame)[6] = "Exp trunc"
colnames(data_frame)[7] = "TPL expo"
colnames(data_frame)[8] = "TPL trunc"

data_frame[is.na(data_frame)] = 0

if (model == "tricritical") {
  write.csv(data_frame, paste(q_folder, "_csd", ".csv", sep=""))
} else {
  write.csv(data_frame, paste("scanlon_csd", ".csv", sep=""))
}
