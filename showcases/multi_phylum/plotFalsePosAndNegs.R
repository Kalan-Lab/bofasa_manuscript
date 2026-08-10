library(ggplot2)

dat <- read.table('Minus_One_Overview_Reformatted.txt', header=T, sep='\t')
# method  category        value

colors <- c('#262626', '#808080')
names(colors) <- c('full', 'minus_one')

pdf('Minus_One_Overview.pdf', height=3, width=4)
ggplot(dat, aes(x=reorder(method, ord), y=value, fill=category)) + geom_bar(stat='identity', color='black') + theme_classic() + theme(axis.text.x = element_text(angle=45, vjust=1, hjust=1)) + scale_fill_manual(values=colors)
dev.off()
