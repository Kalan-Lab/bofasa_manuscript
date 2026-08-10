library(ggplot2)
library(RColorBrewer)
library(dplyr)

dat <- read.table("SCC_Alignment_TotalLen_vs_GapProp_FilteredHighAmbSites.Modified.txt", header=T, sep='\t')

colors <- c('#A03B44', '#F1B16E', '#4B86B8', '#5E4FA2', '#D36D49', '#A1C496')
names(colors) <- c('bofasa', 'OrthoFinder', 'PIRATE', 'SCARAP', 'SonicParanoid')

mycolors <- colorRampPalette(brewer.pal(9, "Spectral"))(20)

print(head(dat))
pdf("Alignment_Length_vs_Gap_Proportion.pdf", height=3, width=3)
ggplot(dat, aes(x=alignment_length, y=gap_proportion, color=method, shape=as.factor(group))) + geom_point(alpha=0.7, show.legend=F, size=5) + theme_classic() + scale_color_manual(values=colors) + xlab("") + ylab("") + theme(text=element_text(size=17)) + ylim(0,0.001111111115)+ theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1))
dev.off()

