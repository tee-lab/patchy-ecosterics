library(poweRlaw)

results_path = "C://Code//Github//vegetation-dynamics//results"
model = "tricritical"
q_value = "q0"
dataset = "max_regime"
folders = c("0p65", "0p7", "0p72", "0p74")


root_path = file.path(results_path, model, q_value, dataset)

for (i in 1:length(folders)) {
  folder = folders[i]
  file_name = paste(folder, "_cluster_distribution.txt", sep="")
  file_path = file.path(root_path, folder, file_name)
  cluster_distribution = read.table(file_path)
  
  biggest_cluster_size = max(cluster_distribution$V1)
  cluster_sizes = c(1:biggest_cluster_size)
  inverse_cdf = vector(length=biggest_cluster_size)
  
  for (j in 1:biggest_cluster_size) {
    inverse_cdf[j] = sum(cluster_distribution$V2[j:biggest_cluster_size + 1])
  }
  inverse_cdf = inverse_cdf / sum(cluster_distribution)
  
  delete_indices = c()
  for (i in 1:(length(inverse_cdf) - 1)) {
    if (inverse_cdf[i] == inverse_cdf[i + 1]) {
      delete_indices = append(delete_indices, i)
    }
  }
  
  inverse_cdf = inverse_cdf[-delete_indices]
  cluster_sizes = cluster_sizes[-delete_indices]
  
  title = paste("Cluster distribution for", folder)
  x_axis = log10(cluster_sizes[2:length(cluster_sizes)])
  y_axis = log10(inverse_cdf[2:length(inverse_cdf)])
  plot(x_axis, y_axis, main=title, xlab="log(cluster size)", ylab="log(inverse cdf)")
}