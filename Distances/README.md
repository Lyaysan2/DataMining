# Distances

For each topic, I took the association words from this site:
https://wordassociation.ru

I parse the habr page and take the text that is presented there for analysis.

I process the text and topics for the presence of stop words, punctuation marks, 
remove the "ё", bring the words to the initial form.

When calculating metrics, I take into account repetitions, because a word may 
accidentally appear in the text once, and in another it is often used 
and these are different situations and the topic changes.

### Lets compare results for two habr pages:
### The first page: https://habr.com/ru/post/356420/

#### jacard metric "sport": 0.003413
#### cosinus metric "sport": 0.005400
###
#### jacard metric "news": 0.020906
#### cosinus metric "news": 0.037352
###
#### jacard metric "shopping": 0.012285
#### cosinus metric "shopping": 0.026993
###
#### jacard metric "science": 0.009259
#### cosinus metric "science": 0.018961

Both metrics show on the news topic, and indeed, this article understands why politicians are still needed.
Other metrics for other topics also match.

### The second page: https://habr.com/ru/post/405943/ about sports as a hobby for health.
It can be seen that the sports metric is higher.

#### jaccard metric "sport": 0.036364
#### cosine metric "sport": 0.080890
###
#### jaccard metric "news": 0.017501
#### cosine metric "news": 0.036082
###
#### jaccard metric "shopping": 0.007054
#### cosine metric "shopping": 0.021729
###
#### jaccard metric "science": 0.010163
#### cosine metric "science": 0.027872