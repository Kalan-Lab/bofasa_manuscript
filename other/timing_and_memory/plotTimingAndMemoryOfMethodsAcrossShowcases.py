library(ggplot2)
library(cowplot)

dat <- read.table("All_Timing_and_Resources.txt", header=T, sep='\t')

colors <- c('#A03B44', '#F1B16E', '#4B86B8', '#5E4FA2', '#D36D49', '#A1C496')
names(colors) <- c('bofasa', 'OrthoFinder', 'PIRATE', 'SCARAP', 'SonicParanoid', 'KOfam')

pdf("Timing_and_Memory.pdf", height=5, width=10)

# showcase	method  method_color	time	memory
time <- ggplot(dat, aes(x=method, y=time, fill=method_color)) + geom_bar(stat='identity', color='black') + theme_classic() + facet_grid(showcase~., scales='free')
memo <- ggplot(dat, aes(x=method, y=memory, fill=method_color)) + geom_bar(stat='identity', color='black') + theme_classic() + facet_grid(showcase~., scales='free')

plot_grid(time, memo)

dev.off()

