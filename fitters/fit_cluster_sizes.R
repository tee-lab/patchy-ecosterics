library(reticulate)
library(spatialwarnings)

results_path = "C://Code//Github//vegetation-dynamics//results"
model = "tricritical"
dataset = "100x100_final"

# q_folder = "q0"
# q_value = "0"
# p_values = c("0p616", "0p618", "0p62", "0p625", "0p63", "0p64", "0p65", "0p7", "0p72")

# q_folder = "q0p25"
# q_value = "0p25"
# p_values = c("0p566", "0p569", "0p57", "0p575", "0p58", "0p59", "0p62", "0p64")

# q_folder = "q0p5"
# q_value = "0p5"
# p_values = c("0p498", "0p5", "0p502", "0p504", "0p506", "0p508", "0p51", "0p52", "0p53", "0p55")

q_folder = "q0p75"
q_value = "0p75"
p_values = c("0p399", "0p4", "0p401", "0p403", "0p405", "0p41", "0p42")

root_path = file.path(results_path, model, q_folder, dataset)
data_frame = data.frame()

for (p in p_values) {
  print(paste("<--- Analyzing", p, "--->"))
  
  file_name = paste("tricritical_", p, "_", q_value, ".pkl", sep="")
  file_path = file.path(root_path, file_name)
  source_python("lattice_parser.py")
  lattices = load_lattices(file_path)
  
  outputs = indicator_psdtype(lattices, wrap=TRUE)
  
  pl_bics = c()
  tpl_bics = c()
  exp_bics = c()
  
  for (output in outputs) {
    pl_bic = output$BIC[1]
    if (is.nan(pl_bic) == FALSE) {
      pl_bics = append(pl_bics, pl_bic)
    }
    
    tpl_bic = output$BIC[2]
    if (is.nan(tpl_bic) == FALSE) {
      tpl_bics = append(tpl_bics, tpl_bic)
    }
    
    exp_bic = output$BIC[3]
    if (is.nan(exp_bic) == FALSE) {
      exp_bics = append(exp_bics, exp_bic)
    }
  }
  
  pl_bic_mean = sum(pl_bics) / length(pl_bics)
  tpl_bic_mean = sum(tpl_bics) / length(tpl_bics)
  exp_bic_mean = sum(exp_bics) / length(exp_bics)
  
  print(pl_bic_mean)
  print(tpl_bic_mean)
  print(exp_bic_mean)
  
  data_frame = rbind(data_frame, c(p, pl_bic_mean, tpl_bic_mean, exp_bic_mean))
}

colnames(data_frame)[1] = "p"
colnames(data_frame)[2] = "PL"
colnames(data_frame)[3] = "TPL"
colnames(data_frame)[4] = "Exp"

write.csv(data_frame, paste(q_folder, "_csd", ".csv", sep=""))