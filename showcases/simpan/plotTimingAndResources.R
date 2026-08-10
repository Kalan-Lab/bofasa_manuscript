library(ggplot2)

dat <- read.table("Timing_and_Resources.txt", header=T, sep='\t')

pdf("Timing.pdf", height=5, width=10)
ggplot(dat, aes(x=method, y=time)) + geom_bar(stat='identity', fill='black') + theme_bw()
dev.off()

pdf("Memory.pdf", height=5, width=10)
ggplot(dat, aes(x=method, y=memory)) + geom_bar(stat='identity', fill='black') + theme_bw()
dev.off()
