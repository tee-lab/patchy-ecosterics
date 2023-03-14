convert_logical <- function(lattice) {
  logical_lattice = matrix(list(), nrow=100, ncol=100)
  
  for (i in 1:100) {
    for (j in 1:100) {
      if (lattice[i,j] == 0) {
        logical_lattice[i,j] = FALSE
      } else {
        logical_lattice[i,j] = TRUE
      }
    }
  }
  return(logical_lattice)
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
  
  file_name = paste("tricritical_", p, "_", q_value, ".pkl", sep="")
  file_path = file.path(root_path, file_name)
  source_python("lattice_parser.py")
  lattices = load_lattices(file_path)
  
  outputs = indicator_psdtype(lattices, wrap=TRUE)
  
  pl_best = 0
  tpl_best = 0
  exp_best = 0
  
  for (output in outputs) {
    if (output$best[1]) {
      pl_best = pl_best + 1
    } else if (output$best[2]) {
      tpl_best = tpl_best + 1
    } else {
      exp_best = exp_best + 1
    }
  }
  
  print(paste("Power-law:", pl_best, "out of", length(lattices), "ensembles"))
  print(paste("Truncated Power-law:", tpl_best, "out of", length(lattices), "ensembles"))
  print(paste("Exponential:", exp_best, "out of", length(lattices), "ensembles"))
}