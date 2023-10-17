#
# This file includes modifications by Alex
#

calc_bic <- function(fit_output, data_len) {
  bic = fit_output$npars * log(data_len) - 2 * (fit_output$ll)
  return(bic)
}


# This function will fit the three distributions to a tabulated set of change
# sizes (dS).
# dS is the change in size, tabulated data is the number of time each dS
# occurs. They must be vectors of the same length
fit_distrs <- function(dS, tabulated_data) {
  if ( all(diff(tabulated_data) < 0) ) {
    warning("Make sure your data is not the inverse cumulative function, i.e. N(dS>=k) instead of N(dS=k)")
  }
  
  print("in fit distrs")

  # Create a (very long) vector containing raw occurrences
  raw_occurrences <- unlist(lapply(seq_along(dS), function(i) {
    rep(dS[i], tabulated_data[i])
  }))
  
  print(length(raw_occurrences))
  
  print("created raw occurrences")

  # Your distributions do not start at 0, so use an xmin here. This is
  # important to get the normalization constants of the distributions right
  xmin <- min(dS)

  # Fit exponential, PL, TPL with proper xmin
  expfit <- exp_fit(raw_occurrences, xmin = xmin)
  print("exp fit done")
  
  plfit <- pl_fit(raw_occurrences, xmin = xmin)
  print("pl fit done")
  
  tplfit <- tpl_fit(raw_occurrences, xmin = xmin)
  print("tpl fit done")

  # Predict response. Here we use spatialwarnings internal functions, see
  # provided fitpsd.R code if you want to have the details.
  exp_probs <- spatialwarnings:::ddisexp(dS, expfit[["cutoff"]], xmin = xmin)
  exp_cprobs <- spatialwarnings:::ipdisexp(dS, expfit[["cutoff"]], xmin = xmin)
  
  pl_probs <- spatialwarnings:::dpl(dS, plfit[["plexpo"]], xmin = xmin)
  pl_cprobs <- spatialwarnings:::ippl(dS, plfit[["plexpo"]], xmin = xmin)
  
  tpl_probs <- spatialwarnings:::dtpl(dS,tplfit[["plexpo"]], tplfit[["cutoff"]], xmin = xmin)
  tpl_cprobs <- spatialwarnings:::iptpl(dS, tplfit[["plexpo"]], tplfit[["cutoff"]], xmin = xmin)

  # Put predictions in df
  # column p contains the probabilities (P(x=k)), ip the inverse cumulative
  # probs (P(x>=k)).
  predictions <- rbind(
    data.frame(psdtype = "pl",  dS = dS, p = pl_probs, ip = pl_cprobs),
    data.frame(psdtype = "exp", dS = dS, p = exp_probs, ip = exp_cprobs)
    # data.frame(psdtype = "tpl", dS = dS, p = tpl_probs, ip = tpl_cprobs)
  )

  # Put fits in list object
  fits <- list(exp = expfit, pl = plfit)
  # fits <- list(exp = expfit, pl = plfit, tpl = tplfit)

  # Compute observed distribution. p contains the probabilities (P(x=k)),
  # ip the inverse cumulative probs (P(x>=k)).
  obs <- data.frame(dS = dS,
                    p = tabulated_data / sum(tabulated_data),
                    ip = sapply(dS, function(x) sum(tabulated_data[dS >= x]) / sum(tabulated_data) ) )

  # Return everything
  list(predictions = predictions,
       fits = fits,
       obs = obs)
}

# Compute the inverse cumulative distribution of a set of values
inv_cumu_distr <- function(xvals, yvals) {
  cdistr <- sapply(xvals, function(x) yvals[xvals >= x] / sum(yvals) )
  # Normalize
  data.frame(x = xvals, y = cdistr)
}

library(reticulate)
library(spatialwarnings)

# results_path = "C://Code//Github//vegetation-dynamics//results"
# model = "tricritical"
# dataset = "100x100_residue"

# Parameters for Alex
results_path <- "..//results"
model = "tricritical"
dataset = "paper"
options(spatialwarnings.constants.maxit = 1e4)
options(spatialwarnings.constants.reltol = 1e-4)

q_folder = "q0"
p_values = c("test") # ideal for debugging
# p_values = c("0p616", "0p618", "0p62", "0p625", "0p63", "0p64", "0p65", "0p7", "0p72")

# q_folder = "q0p25"
# p_values = c("0p566", "0p568", "0p57", "0p575", "0p58", "0p59", "0p62", "0p64")

# q_folder = "q0p5"
# p_values = c("0p498", "0p5", "0p502", "0p504", "0p506", "0p508", "0p51", "0p52", "0p53", "0p55")

# q_folder = "q0p75"
# p_values = c("0p399", "0p4", "0p401", "0p403", "0p405", "0p41", "0p42")

data_frame = data.frame()

root_path = file.path(results_path, model, q_folder, dataset)

for (p in p_values) {
  print(paste("<--- Analyzing", p, "--->"))

  # load data
  file_name = paste(p, "_changes.txt", sep="")
  file_path = file.path(root_path, p, file_name)
  source_python("load_changes_AG.py")
  changes_distr = load_changes(file_path)

  # format data
  x_start = 3 # remove first two points corresponding to ds = 0, and ds = +/- 1
  x_range = x_start:length(changes_distr)
  changes_distr = changes_distr[x_start:length(changes_distr)]
  data_len = length(changes_distr)

  # What to the changes in changes_icdf correspond to?
  dS <- x_range - 1 # the true dS values corresponding to observations
                    # it starts at 2 because we remove 0 and +/- 1 (?)
  
  print("Load complete")

  # Fit distributions
  distribs <- fit_distrs(dS, changes_distr)

  # Display
  require(ggplot2)

  # Show inverse cumulative distribution
  ggplot(NULL) +
    geom_point(aes(x = dS, y = ip),
               data = subset(distribs[["obs"]], ip > 0)) +
    geom_line(aes(x = dS, y = ip, color = psdtype),
              data = distribs[["predictions"]]) +
    scale_y_continuous(trans = "log10") + # comment to remove log scale
    scale_x_continuous(trans = "log10") +
    labs(x = "dS", y = "P(x>=dS)")
  ggsave(filename=paste(p, "_", q_folder, "_icdf.png", sep=""))
  
  print("Showing ICDF")

  # Show probability distribution
  ggplot(NULL) +
    geom_point(aes(x = dS, y = p),
               data = subset(distribs[["obs"]], p > 0)) +
    geom_line(aes(x = dS, y = p, color = psdtype),
              data = distribs[["predictions"]]) +
    scale_y_continuous(trans = "log10") +
    scale_x_continuous(trans = "log10") +
    labs(x = "dS", y = "P(x=dS)")
  ggsave(filename=paste(p, "_", q_folder, "_pdf.png", sep=""))
  
  print("Showing PDF")

  # Extract bic for every fit. Note that the BIC takes the number of
  # observations, not the length of the vector in which you stored the
  # number of obs for each dS.
  n_obs <- sum(changes_distr)
  BICs <- c(p,
            calc_bic(distribs[["fits"]][["pl"]], n_obs),
            calc_bic(distribs[["fits"]][["exp"]], n_obs)
            # calc_bic(distribs[["fits"]][["tpl"]], n_obs)
            )

  # fit exp
  # Alex: OK, this is incorrect: exp_fit expects the observations of dS, not
  # the already-tabulated data (= number of times a given dS appears). We can
  # recreate it from your tabulated data by repeating values as needed.
#   changes_distr_raw <- unlist(lapply(seq_along(changes_distr), function(i) {
#     rep(dS[i], changes_distr[i])
#   }))

  # Here we fit with an xmin = 2 because you can't have dS below that value
#   exp_output = exp_fit(changes_distr_raw, xmin = 2)
#   y <- exp( - exp_output[["cutoff"]] * dS)
#   exp_prediction <- inv_cumu_distr(dS, y)

  # Show distribution and fit
#   changes_icdf_norm <- inv_cumu_distr(dS, changes_distr)
#   plot(dS, changes_icdf_norm, main = sprintf("cd of %s", p),
#        log = "y")
#   lines(exp_prediction[, "x"], exp_prediction[ ,"y"],
#         log = "y",
#         col = "red")

#   # We predict
#   b = exp_output$cutoff
#   plot(x_range, log(changes_icdf / norm_factor),
#        main = paste("cd of", p, "- semilogy plot + exp fit"))
#
#   lines(x_range, -b * x_range, main="exp fit")

  # fit power-law
#   pl_output = pl_fit(changes_icdf)
#   exponent = pl_output$plexpo
#   plot(log(x_range), log(changes_icdf / norm_factor), main=paste("cd of", p, "- log log plot + pl fit"))
#   lines(log(x_range), log(x_range ^ -exponent), main="pl fit")

  # fit tpl
#   tpl_output = tpl_fit(changes_icdf)
#   exponent = tpl_output$plexpo
#   b = tpl_output$cutoff
#   plot(log(x_range), log(changes_icdf / norm_factor), main=paste("cd of", p, "- log log plot + tpl fit"))
#   lines(log(x_range), log((x_range ^ -exponent) * exp(-b * x_range)), main="tpl fit")

  # calculate BIC values
#   pl_bic = calc_bic(pl_output, data_len)
#   tpl_bic = calc_bic(tpl_output, data_len)
#   exp_bic = calc_bic(exp_output, data_len)
#   print(paste("Power-law BIC:", pl_bic))
#   print(paste("Truncated Power-law BIC:", tpl_bic))
#   print(paste("Exponential BIC:", exp_bic))

  print(paste("BICs (pl/exp/tpl): ", BICs[2], BICs[3]))

  # append to data frame
  data_frame <- rbind(data_frame, BICs)
}

colnames(data_frame)[1] = "p"
colnames(data_frame)[2] = "PL"
colnames(data_frame)[3] = "Exp"
# colnames(data_frame)[4] = "TPL"

# save BIC values as CSV
write.csv(data_frame, paste(q_folder, "_cd", ".csv", sep=""))
