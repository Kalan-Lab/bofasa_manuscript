library(ggplot2)

dat <- read.table("Method_Stats.txt", header=T, sep='\t')
# gappy_cat	method	intersection_proportion	gappy_specific_og_pairs


colors <- c('#A03B44', '#F1B16E', '#F1B16E', '#4B86B8', '#5E4FA2', '#D36D49', '#A1C496')
names(colors) <- c('bofasa', 'orthofinder_v2', 'orthofinder_v3', 'pirate', 'scarap', 'sonicparanoid')

shapes <- c(1, 2, 19, 17)
names(shapes) <- c('open_circle', 'open_triangle', 'fill_circle', 'fill_triangle')

pdf("Method_Stats.pdf", height=3.5, width=4)
#ggplot(dat, aes(color=method, shape=shape, x=intersection_proportion, y=gappy_specific_og_pairs)) + geom_point(size=5, show.legend=F, stroke=2.5) + theme_classic() + scale_color_manual(values=colors) + scale_shape_manual(values=shapes)
ggplot(dat, aes(color=method, shape=shape, x=intersection_proportion, y=gappy_specific_og_pairs)) + geom_point(size=5, show.legend=F, stroke=2.5) + theme_classic() + scale_color_manual(values=colors) + scale_shape_manual(values=shapes)

dev.off()
