library(ggplot2)

dat <- read.table('Integrase_OGs_Across_Methods.txt', header=T, sep='\t')
# method  og      og_tot_prots    cat        count

colors <- c('#9e9b9c', '#cf445e', '#333332')

pdf('Fig3B.pdf', height=3, width=10)
ggplot(dat, aes(x=reorder(og, og_tot_prots), y=count, fill=cat)) + geom_bar(stat='identity') + theme_classic() + facet_grid(.~method, space='free', scales='free') + scale_fill_manual(values=colors) 
dev.off()
