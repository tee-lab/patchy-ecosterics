library(reticulate)

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
  
  title = paste("Distribution of cluster ds for", gsub('p', '.', p))
  plot(log10(x_range), log10(changes_icdf), main=title, xlab="log of |ds|", ylab="log of P(|dS|>|ds|)")
}