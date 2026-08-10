library(ggplot2)

dat <- read.table("Plotting_Input.txt", header=T, sep='\t')
# gappy_cat       method  complete_specific       gappy_specific  intersection

pdf("Fig6.pdf", height=5, width=10)
ggplot(dat, aes(x=method, fill=cat, y=value)) + geom_bar(stat='identity', position='dodge', color='black') + theme_classic() + facet_wrap(~gappy_cat) + theme(axis.text.x = element_text(angle = 90, hjust = 1)) + scale_fill_manual(values=c('#3f3f70', '#8888ba', '#5757f7'))
dev.off()
