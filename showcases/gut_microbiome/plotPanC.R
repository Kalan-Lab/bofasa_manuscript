library(ggplot2)
library(ggExtra)

dat <- read.table('Panel_C_Input.txt', header=T, sep='\t')
# method  large_og_id     proteins        tot_avg_doms_ratio      tot_doms        avg_doms

colors <- c('#A03B44', '#F1B16E', '#F1B16E', '#4B86B8', '#5E4FA2', '#D36D49')
names(colors) <- c('bofasa', 'orthofinder_v2', 'orthofinder_v3', 'pirate', 'scarap', 'sonicparanoid')

pdf('Panel_C.pdf', height=4, width=5)

ggplot(dat, aes(x=proteins, y=tot_avg_doms_ratio, color=method)) + geom_point(alpha=0.3, show.legend=F) + theme_bw() + scale_color_manual(values=colors) + facet_wrap(~method)

#ggMarginal(p, type = "histogram", aes(fill = method), color = "white") #+ scale_fill_manual(values=colors)

dev.off()
