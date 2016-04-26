# wikipedia_crawler
A project in python to check how many articles will lead to philosophy if you continue clicking on the first link in the article body

This code starts from a random article in Wikipedia, and each time, recursively, follows the first link 
in the body to the next article, till reaches Philosophy or enter a loop.
Then, it calculates the langth of the path.
This can be done repeatedly using a loop, in order to calculate the average length of that path.

Args:
    repeats = number of repeats the code should run (500, unless changed)
    specific_article = allows selecting specific artilce instead of a random
    
Returns as printed output:
    Histogram of the path lengths - TBD
    Average Path length
    % of articles that didn't lead to philosophy
    Running time
