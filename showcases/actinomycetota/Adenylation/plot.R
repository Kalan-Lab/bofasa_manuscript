library(ggplot2)
library(cowplot)

colors <- c("#D5E3EF", "#C6D8E9", "#B7CDE3", "#A9C3DE", "#9CB7D7", "#94A6CE", "#8C96C6", "#8C82BC", "#8C6FB3", "#8A5DAA", "#884AA1", "#863595", "#831F87", "#7B0D76", "#640660", "#4D004B")
names(colors) <- c("OG0000028_5", "OG0000028_13", "OG0000028_3", "OG0000028_14", "OG0000028_38", "OG0000028_21", "OG0000028_30", "OG0000028_2", "OG0000028_23", "OG0000028_31", "OG0000028_0", "OG0000028_4", "OG0000028_6", "OG0000028_7", "OG0000028_56", "OG0000028_57")

dtrak <- read.table("dog_track.txt", header=T, sep='\t')
dheat <- read.table("dog_heatmap_track.txt", header=T, sep='\t')

# dog     dog_order       species species_order   count
# dog     dog_order       amp_binding_proportion  nrps_proportion total_count

pdf("dog_heatmap.pdf", height=5, width=20)
dh <- ggplot(dheat, aes(y=reorder(dog, dog_order), x=reorder(species, species_order), fill=count)) + geom_tile(show.legend=F) + theme_classic() + scale_fill_gradient2(low='#474746', mid='#e8cc6f', high='#e86f7b', midpoint=1) + theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) + xlab("") + ylab("") + theme(text = element_text(size=25))
db1 <- ggplot(dtrak, aes(y=reorder(dog, dog_order), x=amp_binding_proportion, fill=color)) + geom_bar(stat='identity', show.legend=F) + scale_fill_manual(values=colors) + theme_bw() + theme(axis.title.y=element_blank(), axis.text.y=element_blank(), axis.ticks.y=element_blank()) + xlab("") + ylab("") + theme(text = element_text(size=20))
db2 <- ggplot(dtrak, aes(y=reorder(dog, dog_order), x=nrps_proportion, fill=color)) + geom_bar(stat='identity', show.legend=F) + scale_fill_manual(values=colors) + theme_bw() + theme(axis.title.y=element_blank(), axis.text.y=element_blank(), axis.ticks.y=element_blank()) + ylab("") + xlab("") + theme(text = element_text(size=20))
plot_grid(dh, db1, db2, align='h', rel_widths=c(1,0.2,0.2), ncol=3)
dev.off()
