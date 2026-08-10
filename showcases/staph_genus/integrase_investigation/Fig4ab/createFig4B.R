library(ggplot2)

dat <- read.table("BofasaEmgIntegrase_ContextConsScores.txt", header=T, sep='\t')
dat.context <- read.table("Median_CCS_Per_Conservation_Rank.txt", header=T, sep='\t')
# og      num_prots       context_conservation_score      phage_context
#num_prots       median  10per   90per

colors <- c('#9e9b9c', '#AE6B7B')

pdf('Fig4B.pdf', height=5, width=5)
ggplot(dat, aes(x=num_prots, y=context_conservation_score)) + geom_crossbar(data=dat.context, aes(x=num_prots, y=median, ymin=per10, ymax=per90), color='lightgrey', width=3, alpha=0.7) + geom_point(aes(color=phage_context), show.legend=F, size=4) + theme_classic() + scale_color_manual(values=colors)  + xlab("") + ylab("") + xlim(0,125) + theme(text=element_text(size=30)) 
dev.off()
