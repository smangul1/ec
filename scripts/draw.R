
library(ggplot2)


args = commandArgs(trailingOnly=TRUE)

#ec <- read.table("fiona.igh.ed", header=T)
ec <- read.table(args[1], header=T)


tools <- c("BFC-18","BFC-default","Bless2","Coral-18","Coral-default","ECHO-18","ECHO-default","Fiona","Lighter","Musket","Pollux","Quake","Racer","Reptile","SOAPec")

names(tools) <- c("bfc-18","bfc-default","bless","coral-18","coral-default","echo-18","echo-default","fiona","lighter","musket","pollux","quake","racer","reptile","soapec")

#ec$sample <- factor(ec$sample, levels = rev(levels(ec$sample)))
ec$sample <- factor(ec$sample, levels = c("sim_rl_50_cov_1","sim_rl_75_cov_1","sim_rl_100_cov_1","sim_rl_50_cov_2","sim_rl_75_cov_2","sim_rl_100_cov_2","sim_rl_50_cov_4","sim_rl_75_cov_4","sim_rl_100_cov_4","sim_rl_50_cov_8","sim_rl_75_cov_8","sim_rl_100_cov_8","sim_rl_50_cov_16","sim_rl_75_cov_16","sim_rl_100_cov_16","sim_rl_50_cov_32","sim_rl_75_cov_32","sim_rl_100_cov_32","sim_rl_50_cov_64","sim_rl_75_cov_64","sim_rl_100_cov_64","sim_rl_50_cov_128","sim_rl_75_cov_128","sim_rl_100_cov_128"))


pdf(args[2])

g <- ggplot(ec, aes(sample))         

toolname <- strsplit(args[3], "[.]")
toolname <- toolname[[1]][1]
print(toolname)

g + geom_bar(aes(fill=error), position="fill") + scale_fill_brewer(palette="Spectral") + theme(axis.text.x = element_text(angle = 90, hjust = 1)) + theme(axis.title = element_text(color="#666666", face="bold", size=22)) + ggtitle(paste("Error distribution for ", tools[[toolname]], "(", args[4], ")")) + theme(plot.title = element_text(color="#666666", face="bold", size=20, hjust=0.5)) + theme(axis.text.x=element_text(face="bold")) + theme(axis.text.y=element_text(face="bold"))


dev.off()
