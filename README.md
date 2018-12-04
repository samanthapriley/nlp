# Sample Code for Exploratory NLP in Python

**Table of Contents**

- [Sourcing](#sourcing)
- [Processing](#processing)
- [Visualization](#visualization)
- [Resources](#resources)
   
## Sourcing 
This folder contains three scrapers and sample code for using Reddit's PRAW (API access) library. 

- **army_commented** is a flexible scraper template for obtaining data from straightforward webpages that don't require browser interaction
- **el_corte_ingles_selenium** is a more complicated scraper using selenium to interact with page elements including hovering, scrolling, and clicking
- **praw_sample** pulls submissions and comments based on subreddit and/or keyword search through Reddit's API; you will need to set up your own OAuth key and account
- **YouTube** is a scraper designed to search YouTube for particular keywords, browse through the resulting videos, and pull transcripts

## Processing
This folder contains code using the spaCy natural language library. In terms of required dependencies, you will need Microsoft Visual C++ 14.0 installed on your computer before installing spaCy. You will also need to download the spaCy language models separately depending on which language and data source you are using. 

- **flag_tokens** is a sample file for creating Remove/Reserve classes of words you'd like to either remove or preserve during the spaCy parse
- **matcher_classes** contains sample classes for identifying and tagging certain desired tokens during the parse
- **phrase_extraction** gives examples of using custom syntactic patterns to search for particular topics or phrases within the text
- **sentencizer** is sample code for how to segment the dataset into sub datasets based on flagged tokens; for example, how to extract all sentences that include both the word "doctor" and "appointment" somewhere in the sentence
- **spacy_parsing** is an example script that ties flag_tokens and matcher_classes in, and shows an example of how text data is parsed in spaCy

## Visualization
This folder contains visualization scripts mostly using Scattertext and Seaborn. 

- **displacy_demo** is an interactive IPython notebook for examining the syntactic structure of a parsed sentence using spaCy's syntactic visualizer
- **scattertext_parsed** is sample code for using pre-parsed spaCy documents to create a scattertext
- **scattertext_text** is sample code that includes the spaCy parse before scattertext visualization
- **scattertext_word_similarity** is sample code for using the Scattertext library's word2vec powered similarity explorer
- **top_pos** is sample code written using spaCy to extract top frequent parts of speech from the text and (optionally) index them against COCA
- **visualize_pos** is a Seaborn sample bar visualization that inherits the product of top_pos 

## Resources

#### Selenium 
https://www.seleniumhq.org/
#### PRAW 
https://praw.readthedocs.io/en/latest/
#### spaCy
https://spacy.io/
#### Scattertext
https://github.com/JasonKessler/scattertext
#### Seaborn
https://seaborn.pydata.org/
