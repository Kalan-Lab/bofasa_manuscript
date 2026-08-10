library(ggplot2)
library(gggenes)

dat <- read.table("OG006197_gggenes_input.txt", header=T, sep='\t')

colors <- c("#9B5DE5", "#F15BB5", "#FEE440", "#00BBF9", "#00F5D4", "#702632", "#FFB703", "#023047", "#588157", '#c9c8c7')
names(colors) <- c('OG006197', 'OG006196', 'OG006062', 'OG000192', 'OG006068', 'OG006067', 'OG006184', 'OG006198', 'OG006922', 'Other')

pdf("OG006197.pdf", height=4, width=10)
ggplot(dat, aes(xmin = start, xmax = end, y = bgc_id, fill = ortholog_group)) +
  geom_gene_arrow(arrowhead_height = unit(3, "mm"), arrowhead_width = unit(1, "mm")) +
  facet_wrap(~ bgc_id, scales='free_y',  ncol = 1) + xlim(0,200000) + 
  scale_fill_manual(values = colors) +
  theme_genes()
dev.off()


dat <- read.table("OG019627_gggenes_input.txt", header=T, sep='\t')

colors <- c("#E63946", "#F4A261", "#2A9D8F", "#E76F51", "#264653", "#8D99AE", "#D62828", "#003049", "#FDF0D5", "#c9c8c7")
names(colors) <- c('OG019627', 'OG016096', 'OG012852', 'OG012569', 'OG018362', 'OG019626', 'OG012569', 'OG014458', 'OG014936', 'Other')

pdf("OG019627.pdf", height=4, width=10)
ggplot(dat, aes(xmin = start, xmax = end, y = bgc_id, fill = ortholog_group)) +
  geom_gene_arrow(arrowhead_height = unit(3, "mm"), arrowhead_width = unit(1, "mm")) +
  facet_wrap(~ bgc_id,  ncol = 1, scales='free_y') + 
  scale_fill_manual(values = colors) +
  theme_genes()
dev.off()
