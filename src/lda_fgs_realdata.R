##' #######################################################################
##' This is a script to stress-test FGS on the associated press dataset 
##'
##' Last modified on: June 16, 2014 
##' 
##' Examples:
##' Rscript lda_fgs_realdata.R "E:/Datasets/ap" "ap" .1 .5 100 2000 1500 50
##' Rscript lda_fgs_realdata.R "E:/E-Discovery/trec2010index-wa/Q201-R/tm" "Q201-R" 5 1001 1000 1
##' Rscript lda_fgs_realdata.R "E:/E-Discovery/trec2010index-wa/Q201-S/tm" "Q201-S" 5 1001 1000 1
##' Rscript lda_fgs_realdata.R "E:/E-Discovery/trec2010index-wa/Q202-R/tm" "Q202-R" 5 1001 1000 1
##' Rscript lda_fgs_realdata.R "E:/E-Discovery/trec2010index-wa/Q202-S/tm" "Q202-S" 5 1001 1000 1
##' Rscript lda_fgs_realdata.R "E:/E-Discovery/trec2010index-wa/Q203-R/tm" "Q203-R" 5 1001 1000 1
##' Rscript lda_fgs_realdata.R "E:/E-Discovery/trec2010index-wa/Q203-S/tm" "Q203-S" 5 1001 1000 1
##' Rscript lda_fgs_realdata.R "E:/E-Discovery/trec2010index-wa/Q207-R/tm" "Q207-R" 5 1001 1000 1
##' Rscript lda_fgs_realdata.R "E:/E-Discovery/trec2010index-wa/Q207-S/tm" "Q207-S" 5 1001 1000 1
##' #######################################################################

rm(list=ls()); # Cleanup the current R state 


# Handles commandline arguments  ------------------------------------------

args                         <- commandArgs(TRUE)
data.dir                     <- args[1] 
prefix                       <- args[2] 
K                            <- as.numeric(args[3])
if (length(args) > 3){
  max.iter                   <- as.numeric(args[4])
  burn.in                    <- as.numeric(args[5])
  spacing                    <- as.numeric(args[6])
} else {
  max.iter                   <- 1100
  burn.in                    <- 1000
  spacing                    <- 50
}
store.Dir                    <- 1
alpha                        <- 1/K
eta                          <- 1/K
cat("\nCommandline Arguments:\n")
cat(paste("\ndata.dir:", data.dir))
cat(paste("\nprefix:", prefix))
cat(paste("\nalpha:", alpha))
cat(paste("\neta:", eta))
cat(paste("\nspacing:", spacing))
cat(paste("\nmax.iter:", max.iter))
cat(paste("\nburn.in:", burn.in))
cat("\n")

# 
# data.dir                     <- "E:/E-Discovery/edrmv2txt-a-b-index-t50-s/tm" # "E:/Datasets/ap"
# prefix                       <- "edrmv2txt-a-b-index-t50-s" # "ap"
# alpha                        <- .1 
# eta                          <- .5 
# K                            <- 100  
# max.iter                     <- 1100 # the maximum number of Gibbs iterations
# burn.in                      <- 1000
# spacing                      <- 50
# store.Dir                    <- 1


# lda_fgs_realdata <- function(data.dir, prefix, alpha, eta, K, max.iter, burn.in, spacing, store.Dir){

# Loads necessary libraries and sets global variables  --------------------

cat("\n################################################\n\n")

set.seed(1983)
options(digits=2)

library(MCMCpack)
library(ldahp)

cat("\n################################################\n")


# Loads data  -------------------------------------------------------------

cat("\nLoading data...\n")
setwd(data.dir) # Sets the working dir
vocab.file                   <- paste(prefix, ".ldac.vocab", sep="")
doc.file                     <- paste(prefix, ".ldac", sep="")
ptm                          <- proc.time();
vocab                        <- readLines(vocab.file);
documents                    <- read_docs(doc.file);
# ds                           <- vectorize_docs(documents)
doc.N                        <- calc_doc_lengths(documents)
data.load.ptm                <- proc.time() - ptm;
num.docs                     <- length(documents)
V                            <- length(vocab)
cat("\nData loading time:", data.load.ptm[3]);
# TODO: 
# Need to check it out whether we can have a better way for representing  
# documents in the corpus    

# Gibbs sampling  ---------------------------------------------------------

cat("\nGibbs sampling...\n")
ptm                          <- proc.time();
alpha.v                      <- array(alpha, dim=c(K, 1));                          
# model                        <- lda_fgs(K, V, ds$wid+1, doc.N, alpha.v, 
#                                         eta, max.iter, burn.in, spacing, 
#                                         store.Dir);

model                        <- lda_fgs_blei_corpus(K, V, doc.N, documents, 
                                                    alpha.v, eta, max.iter, 
                                                    burn.in, spacing, 
                                                    store.Dir);
gibbs.ptm                    <- proc.time() - ptm;


# Saves every object into a file ------------------------------------------

rdata.file                   <- paste(prefix, "-fgs-h(", round(eta,  digits=4), 
                                      ",", round(alpha,  digits=4), 
                                      ")-K", K, ".RData", sep="")[1]
save.image(rdata.file)

cat("\nRData is saved to:", rdata.file);
cat("\nData loading time:", data.load.ptm[3]);
cat("\nGibbs sampling time:", gibbs.ptm[3]);



# lbeta <- model$beta[,,10];
# ttw <- t(top_topic_words(lbeta, vocab, num.words=30))
# setwd(data.dir) # Sets the working dir
# write.csv(ttw, file="fgs-top30-topic-words.txt", quote=F, col.names=F)

#setwd(data.dir) # Sets the working dir
theta.file <- paste(prefix, "-K", K, "-Gibbs.lda.theta", sep="")
st <- t(model$theta[,,1])
write.table(st, file=theta.file, quote=F, row.names=F, col.names=F)

rm(list=ls()[ls() != "args"]); # Cleanup the current R state 

# }
# 
# lda_fgs_realdata(data.dir, prefix, alpha, eta, K, max.iter, burn.in, spacing, store.Dir)
