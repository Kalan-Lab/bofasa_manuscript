library('ggplot2')

dat <- read.table("Benchmarking_Results_for_Plot.txt", header=T, sep='\t')

pdf("Simpan_Benchmarking.pdf", height=3, width=7)
ggplot(dat, aes(x=Method, y=Value, fill=Category)) + geom_bar(color='black', stat='identity', position='dodge') + theme_classic() + theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) + scale_fill_manual(values=c('#2d26b5', '#c7426a'))
dev.off()
