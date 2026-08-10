library(ggplot2)
library(cowplot)
dat <- read.table("Methods_Comparison_Summary.txt", header=T, sep='\t')
# method1 method2 overlap m1_total_op
df <- cbind(method1=dat$method1, m1_total_op=dat$m1_total_op)
dfs <- cbind(method1=dat$method1, m1_scc_op=dat$m1_scc_op)
dat.filt <- df[!duplicated(df), ]
dat.filts <- dfs[!duplicated(dfs), ]
pdf("Heatmap.pdf", height=8, width=12)
p1 <- ggplot(dat, aes(y=method1, x=method2, fill=overlap)) + geom_tile(color='white', show.legend=T) + scale_fill_gradient(low='#edbc72', high='#941c54') + theme_classic() + theme(legend.position='bottom', axis.text.x = element_text(angle = 45, vjust =1, hjust=1)) + ylab("focal method") + xlab("comparator method") + geom_text(aes(label=round(overlap, 2))) + scale_y_discrete(limits=rev)
p2 <- ggplot(dat.filt, aes(y=method1, x=as.numeric(m1_total_op))) + geom_col(fill='black') + theme_bw()+ xlab("") + ylab("") + theme(axis.title.y=element_blank(), axis.text.y=element_blank(), axis.ticks.y=element_blank(), axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) + scale_y_discrete(limits=rev) 
p3 <- ggplot(dat.filts, aes(y=method1, x=as.numeric(m1_scc_op))) + geom_col(fill='black') + theme_bw()+ xlab("") + ylab("") + theme(axis.title.y=element_blank(), axis.text.y=element_blank(), axis.ticks.y=element_blank(), axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) + scale_y_discrete(limits=rev)
plot_grid(p1, p2, p3,ncol = 3, align='vh', rel_widths=c(1,0.3,0.3))
dev.off()
