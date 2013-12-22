#####################################################################################################################
## Testing the LDA library in R 
#####################################################################################################################
library(lda);

setwd("F:/Research/datasets/trec2010/Q207-20T/tm")
set.seed(1983); 

num.topics  <- 20; 
itr         <- 5000; ## Num iterations
av          <- 1;
ev          <- 1;
bp          <- 1000;

documents   <- read.documents(filename = "Q207-20T.ldac");
vocab       <- read.vocab(filename = "Q207-20T.ldac.vocab")

result      <- lda.collapsed.gibbs.sampler(documents, num.topics, vocab, itr, alpha=av, eta=ev, burnin=bp, trace=2L);
top.topic.words(result$topics, 20, by.score=TRUE);

# attributes(result)

theta <- result$document_sums
theta <- normalize(theta, dim=1) # normalizes over rows 
num.topics <- nrow(theta)
write(theta, file = "Q207-20T.ldac.theta2", sep = " ", ncolumns=num.topics) # saves to a file 


normalize <- function (XX, dim=1)
{
  ## Normalizes a given matrix XX 
  # 
  # Inputs: 
  #  XX	- data 
  #	dim - normalizing dimension [1] - column wise, [2] - row wise    
  
  
  if (dim == 1){
    cs <- colSums(XX);
    on <- array(1, c(1, dim(XX)[1]));
    Y <- XX / t(cs %*% on);
  }
  else {
    rs <- rowSums(XX);
    on <- array(1, c(1, dim(XX)[2]));
    Y <- XX / (rs %*% on);
  }
  
  return(Y);
  
}
