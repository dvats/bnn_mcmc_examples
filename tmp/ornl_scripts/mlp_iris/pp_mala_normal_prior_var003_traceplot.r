OUTDIR <- file.path("output", "pp_mala", "multiple_chains", "normal_prior", "var003")

store <- TRUE

nmcmc <- 100000
startmcmc <- 90000

i <- 3 # Chain
j <- 23 # Coordinate

chain <- read.table(file.path(OUTDIR, paste('chain', str_pad(i, 2, pad='0'), '.csv', sep='')), header=FALSE, sep=",")

chainmean <- mean(chain[, j])

if (store) {
  pdf(file=file.path(OUTDIR, "mlp_iris_ppmala_normal_prior_var003_traceplot.pdf"), width=10, height=6)
}

oldpar <- par(no.readonly=TRUE)

par(fig=c(0, 1, 0, 1), mar=c(2.25, 4, 3.5, 1)+0.1)

plot(
  startmcmc:nmcmc,
  chain[startmcmc:nmcmc, j],
  type="l",
  ylim=c(-8, 8),
  col="steelblue2",
  xlab="Iteration",
  ylab="",
  main=bquote(paste(theta[.(j)], ": P-MALA", sep=" ")),
  cex.axis=1.8,
  cex.main=2,
  cex.lab=2,
  yaxt="n"
)

axis(
  2,
  at=seq(-8, 8, by=2),
  labels=seq(-8, 8, by=2),
  cex.axis=1.8,
  las=1
)

lines(
  1:nmcmc,
  rep(chainmean, nmcmc),
  type="l",
  col="black",
  lwd=2
)

par(oldpar)

if (store) {
  dev.off()
}
