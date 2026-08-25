library(ggplot2)
library(cowplot)

dat <- read.table("All_Timing_and_Resources.txt", header=T, sep='\t')

colors <- c('#A03B44', '#F1B16E', '#4B86B8', '#5E4FA2', '#D36D49', '#A1C496')
names(colors) <- c('bofasa', 'OrthoFinder', 'PIRATE', 'SCARAP', 'SonicParanoid', 'KOfam')

pdf("Timing_and_Memory.pdf", height=10, width=10)

# showcase	method  method_color	time	memory
time <- ggplot(dat, aes(x=method, y=time, fill=method_color)) + geom_bar(stat='identity', color='black') + theme_classic() + facet_grid(.~showcase, scales='free', space='free_x') + theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) + scale_fill_manual(values=colors)
memo <- ggplot(dat, aes(x=method, y=memory, fill=method_color)) + geom_bar(stat='identity', color='black') + theme_classic() + facet_grid(.~showcase, scales='free', space='free_x') + theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) + scale_fill_manual(values=colors)

plot_grid(time, memo, ncol=1)

dev.off()

