library(spatialwarnings)

data = read.table("data.txt")

output = pl_fit(data)

plot(data)