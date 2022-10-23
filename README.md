
# ARTIFICIAL INTELLIGENCE ON LEGAL LANGUAGE PROCESSING: USING DEEP LEARNING TO FOUND THE REGULATORY LAW FRAMEWORK FOR THE THIRD SECTOR

This paper deals with the application of artificial intelligence algorithms in processing legal language to identify a complete set of rules applicable to a given legal theme. In this study, we sought to delimit the regulatory framework that involves the Third Sector, based on the data set on the Brazilian regulation flow (RegBR). From the bibliographic research, machine learning techniques were applied to automate the classification of each sentence within the analyzed normative acts, allowing to identify to what extent a norm applies to the selected topic. BERT model with fine-tuning by a Brazilian legal dataset was highly effective, reaching 94% of precision (F1-Score and AUC). The results include a total found of 2,359 rules spread in 611 normative acts on the 1,330,190 sentences distributed in 51 thousand regulations contained in the dataset, demonstrating how the applied techniques can contribute to the improvement of the themes involved.

Figure 01 describes the overview of machine learning tasks that will be discussed in the following sections.

The pre-trained BERTIMBAL version BERT-large-portuguese-cased model was fine-tuned with training with TDS dataset. It used the hyper-parameter suggested by Devlin et al. (2019) for fine-tuning downstream tasks:
* batch size  = 16;
* learning rate = 2e-5;
* epochs= 4;
* dropout rate of 0.1.

In our research, we used the PyTorch library. McCormick & Ryan (2019) inspired the source code, and the dataset and the developed model are online on GitHub (https://github.com/mbjesus/regbr/). It applied the Adam Optimization Algorithm from PyTorch worked in a GPU Nvidia. 

After each epoch, the fine-tuned model was evaluated with the VDS dataset. The training loss rate decreased with each epoch, demonstrating that it could learn from the training data. However, the Evaluation loss rate remained practically constant.

F1-Score and AUC metrics increased slightly.  These numbers reinforce that the four training epochs proposed by Devlin et al. (2019) for fine-tuning are sufficient. Table 04 details the metrics of the training and validation stages, and Figure 05 presents the comparison of training and validation loss. 


We build a Bootstrap over 1000 samples without repetition from the VDS dataset and calculate the F1-Score and AUC density distribution. As demonstrated in Figure 06, the distribution is close to Normal Distribution. Consequently, we can estimate the confidence interval with α = 5% for these metrics based on the Limit Central Theorem. The confidence interval for F1-Score was 92% and 98% and for AUC was 93% and 98%.

Finally, in the Deployment stage, 1,330,190 sentences were classified, and the BERT model labeled 2,538 sentences as TS. Business experts analyzed the results and found 27 incorrect classifications, and we removed these sentences from the TS dataset. After that, we merge the sentences to rebuild the original document to compute the metrics. The result was used to build the legal framework for the third sector.
These complete results of automated classification were revised by humans again. The conclusion is that the computational model obtained an assertiveness of 93.94%. In the end, 710 regulations were found with the prediction of the algorithm, of which 611 were correctly predicted. The total of rule sentences predicted was 2,511, where 2,359 was about TS. For comparison, the first search using keywords returns just 17 regulations against more than 610 with machine learning.


The results achieved the proposed objectives, demonstrating that the analysis and classification promoted with the BERT model with fine-tuning with a Brazilian legal dataset were highly effective, reaching 94% F1-Score and 94% de AUC. 

The model processed 1,330,190 sentences and correctly classified 2,359 as TS. This result allowed us to find other 611 laws applicable to the TS, from a set of 50999 rules in the RegBR dataset. From this information, it was possible to evaluate metrics illustrating how this regulation was developed over time.

Thereby, the work contributes to the improvement of research in machine learning and the law for TS. For future work, the aim is to extend the classification to jurisprudential decisions of public accounts, to understand how the public-private collaboration has been inspected by the Brazilian Courts. Furthermore, semantic analysis of the norms can be applied to verify if it limits or grants a right to the TS.


## Acknowledgments

The authors would like to thank the Accounts Court of Goiás (TCE/GO), which under a partnership with the Federal University of Goiás (UFG) for Professional Master's in Public Administration (PROFIAP), made this research possible and kindly provided your datacenter with the GPU’s, without which the results would take much longer. 
