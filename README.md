These are my assignments and projects that are created for computational linguistics class.

# Auto Correction

The program, firstly, cleans a html document by using regex. Then it tokenize it and calculate the frequency of the apperance of a word in the document. The program takes two parameters, namely 'word' and 'n_suggestions'. It calculates the edit distance of the word and gives n suggestion.

For example:
getSuggestionsWithEditDistance("olöadı", 7) gives the following output: ['olmadı', 'olması', 'olası', 'olanı', 'adı', 'olan', 'alanı']

The program can also make you choose between the option and put it on the memory so that if the user make the typo again, it automatically gives the option that the user choosed before.

For example:
AutoCorrect("kazanmı") gives the following output and user choose among the options.

0 kazandı

1 alanı

2 azami

3 kanalı

4 zamanı

Please give your response:0

Your answer is saved as kazanmı -> kazandı

If the user call the function with the same word, it gives the following output:

Your word is: kazanmı

The correct word is 'kazandı'

# Recommend Songs by Mood

The program recommend songs by your mood. The program use naive bayes to train itself. The program reads song lyrics dataset and based on lyrics recommends songs based on the input. Streamlit package is used so that it can be run on a browser. You can be an example below.

![song-recommends](https://github.com/ahmethaksever/comp-ling/assets/107223224/5f38c10e-e46a-493d-9517-f138a0f2fe32)
