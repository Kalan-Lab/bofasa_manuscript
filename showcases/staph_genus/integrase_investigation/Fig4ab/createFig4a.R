library(ggplot2)

dat <- read.table('Simplified_Info_for_Plotting.tsv', header=T, sep='\t')
# og      num_prots       context_conservation_score      phage_context

dat.mge <- dat[dat$phage_context=='True',]
dat.other <- dat[dat$phage_context=='False',]

colors <- c('#9e9b9c', '#cf445e')

pdf('Fig4A.pdf', height=5, width=5)
ggplot(dat.other, aes(x=num_prots, y=context_conservation_score)) + geom_point(alpha=0.2, shape=19, color='#b5b5b5', size=4) + geom_point(data=dat.mge, alpha=0.4, color='#8a243a', size=4, shape=19, aes(x=num_prots, y=context_conservation_score)) + theme_classic() + scale_color_manual(values=colors)  + xlab("") + ylab("") + xlim(0,125) + theme(text=element_text(size=30))
dev.off()
