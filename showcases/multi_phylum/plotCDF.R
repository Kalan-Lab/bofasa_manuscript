library(ggplot2)

dat <- read.table("CDF_Plot_Input.txt", header=T, sep='\t')

colors <- c('#A03B44', '#F1B16E', '#4B86B8', '#5E4FA2', '#D36D49', '#A1C496')
names(colors) <- c('bofasa', 'OrthoFinder', 'PIRATE', 'SCARAP', 'SonicParanoid', 'KOfam')

# method  index   cdf     og_size

pdf("CDF_Plot_Input.pdf", height=3.5, width=3)
ggplot(dat, aes(x=index, y=cdf, color=method)) + geom_line(alpha=0.5, show.legend=F, size=1.5, aes(linetype=as.factor(type))) + theme_classic()  + scale_color_manual(values=colors) + xlab("") + ylab("") + theme(text=element_text(size=17)) + theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1))
dev.off()
