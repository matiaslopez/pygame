# INITIAL ####
rm(list=ls())
setwd("/home/mlopez/repos/Dropbox/interval timming")

#sudo apt-get install r-cran-rsqlite

list.of.packages <- c("ggplot2", "dplyr")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]

if(length(new.packages)) install.packages(new.packages, dependencies = TRUE)
lapply(list.of.packages, require, character.only = TRUE)


# Load data ----

temp = list.files(pattern="*.csv")

df_raw <- do.call(rbind, lapply(temp, function(x) cbind(read.csv(x, sep=";"), subject=strsplit(x,'\\.')[[1]][1])))

# View(df_raw)                

levels(df_raw$subject)


# Integrity of the data ----

df_raw %>%
  group_by(subject, Block) %>%
  summarize(n=n()) %>%
  ungroup() %>%
  group_by(Block) %>%
  summarize(n=n(), mean=mean(n), min= min(n), max=max(n))

#there is an incomplete subject
df_raw %>%
  group_by(subject, Block) %>%
  summarize(n=n()) %>%
  ungroup() %>% group_by(subject) %>%
  summarize(n2=n()) %>% 
  filter(n2!=7)

#Remove Ian Molina  
df_raw %>% ungroup()%>%
  filter(subject!="Ian Molina_2016-09-01_11") -> df_raw

df_raw %>% filter(is.na(Subject.Answer.Time))

df_raw %>%
  group_by(subject, Block) %>%
  mutate(trial_num = row_number()) -> df_raw

# End of filtering ------

df_raw %>% select(subject, Block, trial_num, Date, Stimulus.Length,Subject.Answer.Time) %>%
  mutate(diff = Subject.Answer.Time - Stimulus.Length) %>% 
  mutate(stim = Block %in% c("SUBJECT-1", "SUBJECT-2", "SUBJECT-3") ) %>%
  mutate(short_subject=substr(subject, 0, 4)) %>%
  mutate(block_name = ifelse(stim, paste0("Block ", substr(Block,9,9), " - ", Stimulus.Length/1000, " (sec)"), 
                             "None") ) %>%
  ungroup() -> df


# Plot delta answer ---------
df %>% filter(stim) %>%
  ggplot(aes(x=diff, fill=factor(Stimulus.Length))) +
  geom_histogram(bins = 30) +
  facet_wrap(~block_name, ncol=1) -> p
p + xlab(label = "Difference to correct answer" ) +
  scale_fill_discrete(guide = FALSE)

df %>% filter(stim) %>%
  mutate(block_name = factor(block_name, levels=(rev(unique(df$block_name))))) %>%
  ggplot(aes(x=diff, fill=block_name)) +
  geom_density(alpha=.5) + xlab(label = "Difference to correct answer" ) +
  scale_fill_discrete(guide = guide_legend(reverse=TRUE)) +
  geom_vline(xintercept = 0,linetype=2)

# Plot regular difference -----
df %>% filter(stim) %>%
  filter(short_subject %in% c("Adri", "Laut", "Taie", "Owen", "Este")) %>%
  mutate(diff_sign = factor(ifelse(abs(diff)<0.1*Stimulus.Length, "Correct", 
                            ifelse(diff>0.1*Stimulus.Length, "Slower", "Faster")),
                            levels=c("Faster", "Correct", "Slower"))) %>%
  ggplot(aes(x=trial_num, y=diff, color=diff_sign)) +
  geom_point() +
  # facet_grid(short_subject~block_name)
  facet_grid(block_name~short_subject) +
  coord_cartesian(ylim = c(-3000,3000))
  # scale_color_discrete(guide = FALSE)

df %>% filter(stim) %>%
  # filter(short_subject %in% c("Adri", "Laut", "Taie", "Owen", "Este", "Maxi")) %>%
  # filter(short_subject %in% unique(df$short_subject)[1:8]) %>%
  # filter(short_subject %in% unique(df$short_subject)[9:16]) %>%
  # filter(short_subject %in% unique(df$short_subject)[17:24]) %>%
  filter(short_subject %in% unique(df$short_subject)[25:32]) %>%
  group_by(subject, Block) %>%
  mutate(cum_diff=cumsum(diff)) %>%
  # mutate(diff_sign = (cum_diff>0)) %>%
  mutate(diff_sign = factor(ifelse(abs(cum_diff)<0.1*Stimulus.Length*trial_num, "Regular", 
                                   ifelse(cum_diff>0.1*Stimulus.Length, "Slower", "Faster")),
                            levels=c("Faster", "Regular", "Slower"))) %>% 
  ggplot(aes(x=trial_num, y=cum_diff, color=diff_sign)) +
  stat_smooth(method = "lm", col = "yellow") +
  # facet_grid(subject~Stimulus.Length)
  facet_grid(block_name~short_subject) +
  # scale_color_discrete(guide = FALSE)
  geom_line(aes(y=0.1*Stimulus.Length*trial_num), color="black") + 
  geom_line(aes(y=-0.1*Stimulus.Length*trial_num), color="black") +
  geom_point() 

