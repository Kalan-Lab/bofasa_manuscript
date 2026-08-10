library(ggplot2)
library(cowplot)

colors <- c("#E8F6AE", "#D9F0A3", "#C3E698", "#ADDD8E", "#92D183", "#78C679", "#5CB86A", "#41AB5D", "#329750", "#238443", "#11763D", "#006837", "#005630", "#004529")
names(colors) <- c("OG0000054_8", "OG0000054_31", "OG0000054_36", "OG0000054_2", "OG0000054_0", "OG0000054_56", "OG0000054_6", "OG0000054_7", "OG0000054_9", "OG0000054_26", "OG0000054_32", "OG0000790_0", "OG0000790_1", "OG0000790_3")

dtrak <- read.table("dog_track.txt", header=T, sep='\t')
dheat <- read.table("dog_heatmap_track.txt", header=T, sep='\t')

# dog     dog_order       species species_order   count
# dog     dog_order       amp_binding_proportion  nrps_proportion total_count

pdf("dog_heatmap.pdf", height=4.375, width=20)
dh <- ggplot(dheat, aes(y=reorder(dog, dog_order), x=reorder(species, species_order), fill=count)) + geom_tile(show.legend=F) + theme_classic() + scale_fill_gradient2(low='#474746', mid='#e8cc6f', high='#e86f7b', midpoint=1) + theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) + xlab("") + ylab("") + theme(text = element_text(size=25))
db1 <- ggplot(dtrak, aes(y=reorder(dog, dog_order), x=condensation_proportion, fill=color)) + geom_bar(stat='identity', show.legend=F) + scale_fill_manual(values=colors) + theme_bw() + theme(axis.title.y=element_blank(), axis.text.y=element_blank(), axis.ticks.y=element_blank()) + xlab("") + ylab("") + theme(text = element_text(size=20))
db2 <- ggplot(dtrak, aes(y=reorder(dog, dog_order), x=nrps_proportion, fill=color)) + geom_bar(stat='identity', show.legend=F) + scale_fill_manual(values=colors) + theme_bw() + theme(axis.title.y=element_blank(), axis.text.y=element_blank(), axis.ticks.y=element_blank()) + ylab("") + xlab("") + theme(text = element_text(size=20))
plot_grid(dh, db1, db2, align='h', rel_widths=c(1,0.2,0.2), ncol=3)
dev.off()
