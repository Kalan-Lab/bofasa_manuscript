library(ggplot2)
library(scales)
library(forcats) # Added for fct_rev()

dat <- read.table("Heatmap_Input.txt", header=T, sep='\t')
# focal_og        bgc_id  scaffold_id     start   end     profile category        best_standardized_score

pdf('Heatmap_Updated.pdf', height=8, width=8)
ggplot(dat, aes(y=bgc_id, x=profile, fill=best_standardized_score)) + 
  geom_tile(color='black') + 
  theme_minimal() + 
  # 1. Reverse the vertical grid panes (focal_og) using fct_rev()
  facet_grid(fct_rev(focal_og) ~ category, space='free', scales='free') + 
  # 2. Reverse the y-axis categorical labels using scale_y_discrete(limits = rev)
  scale_y_discrete(limits = rev) + 
  scale_fill_gradient(low='#FFFFFF', high='#82a6c2', na.value='#ed8e87', limits=c(0, 1), oob = scales::squish) + 
  theme(legend.position='bottom', axis.text.x = element_text(angle = 45, hjust = 1))

dev.off()
