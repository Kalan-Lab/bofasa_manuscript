library(ggplot2)

dat <- read.table("OG_vs_SCC_Counts.txt", header=T, sep='\t')

colors <- c('#A03B44', '#F1B16E', '#4B86B8', '#5E4FA2', '#D36D49', '#A1C496')
names(colors) <- c('bofasa', 'OrthoFinder', 'PIRATE', 'SCARAP', 'SonicParanoid', 'KOfam')

pdf("OG_vs_SCC.pdf", height=3.5, width=3)
ggplot(dat, aes(x=ogs, y=scc, color=method, shape=as.factor(type))) + geom_point(alpha=0.7, show.legend=F, size=5) + theme_classic() + scale_x_log10() + scale_color_manual(values=colors) + xlab("") + ylab("") + theme(text=element_text(size=17), axis.text.x = element_text(angle = 45, vjust = 1, hjust=1))
dev.off()
