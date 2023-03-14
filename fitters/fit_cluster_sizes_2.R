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
p_values = c("0p72")
# p_values = c("0p65", "0p7", "0p72", "0p74")

root_path = file.path(results_path, model, q_folder, dataset)

for (p in p_values) {
  file_name = paste("lattices_", p, "_", q_value, ".pkl", sep="")
  file_path = file.path(root_path, file_name)
  source_python("lattice_parser.py")
  lattices = load_lattices(file_path)
  
  logical_lattices = lapply(lattices, convert_logical)

  # logical_lattices = list()
  # 
  # for (i in 1:length(lattices)) {
  #   logical_lattice = convert_logical(lattices[[i]])
  #   logical_lattices = append(logical_lattices, logical_lattice)
  # }
  
  indicator_psdtype(logical_lattices)
}