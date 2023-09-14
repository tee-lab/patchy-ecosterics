library(reticulate)
library(spatialwarnings)

results_path = "C://Code//Github//vegetation-dynamics//results"
model = "tricritical"
q_folder = "q0"
dataset = "100x100_final"

q_value = "0"
p_values = c("0p616", "0p618", "0p62", "0p625", "0p63", "0p64", "0p65", "0p7", "0p72")

root_path = file.path(results_path, model, q_folder, dataset)

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
}