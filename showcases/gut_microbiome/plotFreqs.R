library(ggplot2)

colors <- c('#A03B44', '#F1B16E', '#4B86B8', '#5E4FA2', '#D36D49', '#A1C496')
names(colors) <- c('bofasa', 'OrthoFinder', 'PIRATE', 'SCARAP', 'SonicParanoid', 'KOfam')

dat <- read.table("Ortholog_Frequencies.txt", header=T, sep='\t')

pdf("Ortholog_Frequences.pdf", height=3, width=5.2)
ggplot(dat, aes(x=size, fill=method_name)) + geom_histogram(show.legend=F) + facet_wrap(~method, ncol=3) + theme_classic() + scale_y_log10() + scale_fill_manual(values=colors) + geom_vline(xintercept=100, linetype=2, color='red') 
dev.off()
