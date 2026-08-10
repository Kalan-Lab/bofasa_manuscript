#setwd("/Users/raufs/Mounts/calcaneus_local/rauf/bofasa/actino_showcase_dataset/Figure2/Assess_Interesting_NRPS_Related_Domains/")

library(ggplot2)

colors <- c('#A03B44', '#F1B16E', '#F1B16E', '#4B86B8', '#5E4FA2', '#D36D49', '#D36D49')
names(colors) <- c('bofasa', 'orthofinder_v2', 'orthofinder_v3', 'PIRATE', 'scarap', 'SonicParanoid_Default', 'SonicParanoid_Sensitive')

dat1 <- read.table("Bargraph_Input.txt", header=T, sep='\t')
dat2 <- read.table("Scatterplot_Input.txt", header=T, sep='\t')
dat3 <- read.table("Entropy_Data_Bofasa.txt", header=T, sep='\t')
dat4 <- read.table("Metallophore_Barplot_Input.txt", header=T, sep='\t')

pdf("plot_a.pdf", height=4, width=3)
ggplot(dat1, aes(x=method, y=count, fill=method, alpha=alpha)) + 
  geom_bar(stat='identity', color='black', show.legend=F) + theme_classic() +
  scale_fill_manual(values=colors) + xlab("") + ylab("") + 
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) + 
  theme(text=element_text(size=17))
dev.off()

colors <- c('#A03B44', '#F1B16E', '#4B86B8', '#5E4FA2', '#D36D49', '#A1C496')
names(colors) <- c('bofasa', 'OrthoFinder', 'PIRATE', 'SCARAP', 'SonicParanoid', 'KOfam')

dat2.bof <- dat2[dat2$method == 'bofasa',]
dat2.oth <- dat2[dat2$method != 'bofasa',]

pdf("plot_b.pdf",  height=3, width=6)
ggplot(dat2.oth, aes(color=method, shape=as.factor(method_type), x=prot_count, y=genome_count)) + 
  geom_point(alpha=0.7, show.legend=F, size=5) + geom_point(data=dat2.bof, aes(x=prot_count, y=genome_count), size=5, fill='#A03B44', alpha=0.7, show.legend=F) + theme_classic() + 
 scale_color_manual(values=colors) + xlab("") + ylab("") + 
  theme(text=element_text(size=17))
dev.off()

pdf("plot_c.pdf", height=3, width=6)
ggplot(dat3, aes(x=Number.of.genomes.with.OG, y=Context.conservation.score, size=Median.OG.length..bp.)) + 
  geom_point(show.legend=F, color='#A03B44') + theme_classic() + theme(text=element_text(size=17)) + 
  xlab("") + ylab("") 
dev.off()

pdf("plot_c.pdf", height=2.5, width=3)
ggplot(dat4, aes(x=orthogroup, y=count, fill=cat)) + geom_bar(show.legend=F, color='black', stat='identity') + xlab("") + ylab("") + scale_fill_manual(values=c("#424242", "#afb3b0")) + theme_classic() + theme(text=element_text(size=17)) 
dev.off()
#dat <- read.table("NRPS_DOG_Stats.txt", header=T, sep='\t')

#dat$prop_bgc <- dat$instances_in_bgc/dat$tot_instances
#dat$copy_avg <- dat$tot_instances/dat$len_genome_contexts

#dat.filt <- dat[dat$len_genome_contexts >= 23,]
#dat.filt <- dat.filt[dat.filt$prop_bgc >= 0.50,]

#print(head(dat))

#ggplot(dat.filt, aes(x=reorder(dog, bgc_region_length), y=bgc_region_length)) + geom_boxplot()  + theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1))
