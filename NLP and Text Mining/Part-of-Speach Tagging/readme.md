# Part-of-Speech Tagging with Feed Forward Neural Network 

### 1. Summary

- Motivation: Course Assignment of *CSCI-B 659 Topics in Artificial Intelligence*
- Task Type: NLP, Neural Network, Research Replication
- Topic: 
- Technologies: 
  - Python 
  - Keras 

### 2. Introduction

The purpose of the following implementation was to replicate the research result presented in the Schmid's 1994 paper [*Part-of-speech tagging with neural networks*](https://www.aclweb.org/anthology/C94-1027.pdf). More specifically, I re-implemented the whole data pipeline to prepared the same format learning data used in the original paper. As for the neural network modeling, since I relied on Keras package to build and train the neural network, I had to make some simplification to the original training architecture. With the architecture specified above, my implementation successfully replicated the original training result. It basically obtained the same model performance as the original implementation.