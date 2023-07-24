---
pipeline_tag: sentence-similarity
tags:
- sentence-transformers
- feature-extraction
- sentence-similarity
language: en
---

# Model description

The project aims to train sentence embedding models on very large sentence level datasets using a self-supervised 
contrastive learning objective. We used the pretrained ['MiniLM-L6-H384-uncased'](https://huggingface.co/nreimers/MiniLM-L6-H384-uncased) model and fine-tuned in on a 
1B sentence pairs dataset. We use a contrastive learning objective: given a sentence from the pair, the model should predict which out of a set of randomly sampled other sentences, was actually paired with it in our dataset.

We developped this model during the 
[Community week using JAX/Flax for NLP & CV](https://discuss.huggingface.co/t/open-to-the-community-community-week-using-jax-flax-for-nlp-cv/7104), 
organized by Hugging Face. We developped this model as part of the project:
[Train the Best Sentence Embedding Model Ever with 1B Training Pairs](https://discuss.huggingface.co/t/train-the-best-sentence-embedding-model-ever-with-1b-training-pairs/7354). We benefited from efficient hardware infrastructure to run the project: 7 TPUs v3-8, as well
as intervention from Google’s Flax, JAX, and Cloud team member about efficient deep learning frameworks.

## Intended uses

Our model is intented to be used as a sentence encoder. Given an input sentence, it ouptuts a vector which captures 
the sentence semantic information. The sentence vector may be used for information retrieval, clustering or sentence 
similarity tasks.

## How to use

Here is how to use this model to get the features of a given text using [SentenceTransformers](https://github.com/UKPLab/sentence-transformers) library:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('flax-sentence-embeddings/all_datasets_v4_MiniLM-L6')
text = "Replace me by any text you'd like."
text_embbedding = model.encode(text)
# array([-0.01559514,  0.04046123,  0.1317083 ,  0.00085931,  0.04585106,
#        -0.05607086,  0.0138078 ,  0.03569756,  0.01420381,  0.04266302 ...],
#        dtype=float32)
```

# Training procedure

## Pre-training 

We use the pretrained ['MiniLM-L6-H384-uncased'](https://huggingface.co/nreimers/MiniLM-L6-H384-uncased) which is a 6 layer version of 
['microsoft/MiniLM-L12-H384-uncased'](https://huggingface.co/microsoft/MiniLM-L12-H384-uncased) by keeping only every second layer. 
Please refer to the model card for more detailed information about the pre-training procedure.

## Fine-tuning 

We fine-tune the model using a contrastive objective. Formally, we compute the cosine similarity from each possible sentence pairs from the batch.
We then apply the cross entropy loss by comparing with true pairs.

### Hyper parameters

We trained ou model on a TPU v3-8. We train the model during 540k steps using a batch size of 1024 (128 per TPU core).
We use a learning rate warm up of 500. The sequence length was limited to 128 tokens. We used the AdamW optimizer with
a 2e-5 learning rate. The full training script is accessible in this current repository.

### Training data

We use the concatenation from multiple datasets to fine-tune our model. The total number of sentence pairs is above 1 billion sentences.
We sampled each dataset given a weighted probability which configuration is detailed in the `data_config.json` file.


| Dataset                                                  | Paper                                    | Number of training tuples  |
|:--------------------------------------------------------:|:----------------------------------------:|:--------------------------:|
| [GOOAQ: Open Question Answering with Diverse Answer Types](https://github.com/allenai/gooaq) | [paper](https://arxiv.org/pdf/2104.08727.pdf) | 3,012,496 |
| [Stack Exchange](https://huggingface.co/datasets/flax-sentence-embeddings/stackexchange_title_body_jsonl) | - | 364,001 |
| [Flickr 30k](https://shannon.cs.illinois.edu/DenotationGraph/) | [paper](https://transacl.org/ojs/index.php/tacl/article/view/229/33) | 317,695 |
| [COCO 2020](COCO 2020) | [paper](https://link.springer.com/chapter/10.1007%2F978-3-319-10602-1_48) | 828,395|
| [Code Search](https://huggingface.co/datasets/code_search_net) | - | 1,151,414 |
| [TriviaqQA](https://huggingface.co/datasets/trivia_qa) | - | 73,346 |
| [SQuAD2.0](https://rajpurkar.github.io/SQuAD-explorer/) | [paper](https://aclanthology.org/P18-2124.pdf) | 87,599 |
| [Natural Questions (NQ)](https://ai.google.com/research/NaturalQuestions) | [paper](https://transacl.org/ojs/index.php/tacl/article/view/1455) | 100,231 |
| [Simple Wikipedia](https://cs.pomona.edu/~dkauchak/simplification/) | [paper](https://www.aclweb.org/anthology/P11-2117/) | 102,225 |
| [Quora Question Pairs](https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs) | - | 103,663 |
| [Altlex](https://github.com/chridey/altlex/) | [paper](https://aclanthology.org/P16-1135.pdf) | 112,696 |
| [Wikihow](https://github.com/pvl/wikihow_pairs_dataset) | [paper](https://arxiv.org/abs/1810.09305) | 128,542 |
| [Sentence Compression](https://github.com/google-research-datasets/sentence-compression) | [paper](https://www.aclweb.org/anthology/D13-1155/) | 180,000 |
| AllNLI ([SNLI](https://nlp.stanford.edu/projects/snli/) and [MultiNLI](https://cims.nyu.edu/~sbowman/multinli/) | [paper SNLI](https://doi.org/10.18653/v1/d15-1075), [paper MultiNLI](https://doi.org/10.18653/v1/n18-1101) | 277,230 | 
| [Eli5](https://huggingface.co/datasets/eli5) | [paper](https://doi.org/10.18653/v1/p19-1346) | 325,475 |
| [SPECTER](https://github.com/allenai/specter) | [paper](https://doi.org/10.18653/v1/2020.acl-main.207) | 684,100 |
| [S2ORC](https://github.com/allenai/s2orc) Title/Abstract | [paper](https://aclanthology.org/2020.acl-main.447/) | 41,769,185 |
| [S2ORC](https://github.com/allenai/s2orc) Citation/Citation | [paper](https://aclanthology.org/2020.acl-main.447/) | 52,603,982 |
| [S2ORC](https://github.com/allenai/s2orc) Citation/Abstract | [paper](https://aclanthology.org/2020.acl-main.447/) | 116,288,806 |
| [PAQ](https://github.com/facebookresearch/PAQ) | [paper](https://arxiv.org/abs/2102.07033) | 64,371,441 |
| [WikiAnswers](https://github.com/afader/oqa#wikianswers-corpus) | [paper](https://doi.org/10.1145/2623330.2623677) | 77,427,422 |
| SearchQA | - | 582,261 |
| [Yahoo Answers](https://www.kaggle.com/soumikrakshit/yahoo-answers-dataset) Title/Answer | [paper](https://proceedings.neurips.cc/paper/2015/hash/250cf8b51c773f3f8dc8b4be867a9a02-Abstract.html) | 1,198,260 |
| [Yahoo Answers](https://www.kaggle.com/soumikrakshit/yahoo-answers-dataset) Title/Question | [paper](https://proceedings.neurips.cc/paper/2015/hash/250cf8b51c773f3f8dc8b4be867a9a02-Abstract.html) | 659,896 |
| [Yahoo Answers](https://www.kaggle.com/soumikrakshit/yahoo-answers-dataset) Question/Answer | [paper](https://proceedings.neurips.cc/paper/2015/hash/250cf8b51c773f3f8dc8b4be867a9a02-Abstract.html) | 681,164 |
| [MS MARCO](https://microsoft.github.io/msmarco/) | [paper](https://doi.org/10.1145/3404835.3462804) | 9,144,553 |
| [Reddit conversationnal](https://github.com/PolyAI-LDN/conversational-datasets/tree/master/reddit) | [paper](https://arxiv.org/abs/1904.06472) | 726,484,430 |
| total | | 1,097,953,922 |