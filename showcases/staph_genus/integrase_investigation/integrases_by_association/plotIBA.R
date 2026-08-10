library(ggplot2)
library(cowplot)

heat.dat <- read.table('IBA_Heatmap_Input.txt', header=T, sep='\t')
# protein method  call    method_support  supports

prot.dat <- read.table('IBA_Protein_Input.txt', header=T, sep='\t')
# protein call    method_support

meth.dat <- read.table('IBA_Methods_Input.txt', header=T, sep='\t')
# method  call        count

call.colors.collection <- c('yes' = '#678dc9', 'no' = '#e39fa5', 'maybe' = '#a6a4a4')

# --- THE HEATMAP ---
gg.heat <- ggplot(heat.dat, aes(x=reorder(protein, method_support), y=method, fill=supports)) + 
  geom_tile(fill='black') + 
  theme_classic() + 
  theme(
    legend.position = "none",
    # Rotating the protein names here
    axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1)
  )

# --- THE TOP PROTEIN BARGRAPH ---
gg.prot <- ggplot(prot.dat, aes(x=reorder(protein, method_support), y=method_support, fill=call)) + 
  geom_bar(stat='identity') + 
  scale_fill_manual(values=call.colors.collection) + 
  theme_classic() + 
  theme(
    legend.position = "none", 
    axis.title.x = element_blank(), 
    axis.text.x = element_blank(), # Keep these hidden so they don't double up
    axis.ticks.x = element_blank()
  )

# --- THE SIDE METHOD BARGRAPH ---
gg.meth <- ggplot(meth.dat, aes(y=method, x=count, fill=call)) + 
  geom_bar(stat='identity') + 
  scale_fill_manual(values=call.colors.collection) + 
  theme_classic() + 
  theme(
    legend.position = "none", 
    axis.title.y = element_blank(), 
    axis.text.y = element_blank(),
    axis.ticks.y = element_blank()
  )


# --- THE ASSEMBLY (THE RECONSTRUCTION) ---

# 1. Align the panels first!
# This makes sure the 'bones' of the protein bar and heatmap match perfectly
# before we even think about putting them in a grid.
plots_v <- align_plots(gg.prot, gg.heat, align = 'v', axis = 'lr')

# 2. Build the Top Row
# Use the aligned protein plot (it's the first one in the list we just made)
top_row <- plot_grid(plots_v[[1]], NULL, ncol = 2, rel_widths = c(1, 0.4))

# 3. Build the Bottom Row
# Use the aligned heatmap plot (it's the second one in the list)
# And we align it horizontally with the method bars
bottom_row <- plot_grid(plots_v[[2]], gg.meth, ncol = 2, rel_widths = c(1, 0.4), align = 'h', axis = 'bt')

# 4. Stack 'em up
# Since we already did the hard work with align_plots, this part is easy
final_plot <- plot_grid(top_row, bottom_row, ncol = 1, rel_heights = c(0.3, 1))

# Check the results
pdf('IBA_Figure_Perfect_Alignment.pdf', height=7, width=10)
print(final_plot)
dev.off()
