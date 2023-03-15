library(reticulate)
library(spatialwarnings)

results_path = "C://Code//Github//vegetation-dynamics//results"
model = "tricritical"
q_folder = "q0"
dataset = "256x256"

q_value = "0"
p_values = c("0p63", "0p65", "0p7", "0p72", "0p74")

root_path = file.path(results_path, model, q_folder, dataset)

for (p in p_values) {
  print(paste("<--- Analyzing", p, "--->"))
  
  file_name = paste("tricritical_", p, "_", q_value, ".pkl", sep="")
  file_path = file.path(root_path, file_name)
  source_python("lattice_parser.py")
  lattices = load_lattices(file_path)
  
  pl_ranges = numeric(length(lattices))
  
  for (i in 1:length(lattices)) {
    pl_ranges[i] = raw_plrange(lattices[[i]])
  }
  print(mean(pl_ranges))
  print(var(pl_ranges))
}