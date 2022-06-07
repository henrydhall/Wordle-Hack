# Wordle-Hack
Some Stuff I'm going to play around with to optimize solving wordles. In this file I'll outline the process I used to put this together.

## Rules of Wordle
I'm going to be lazy and refer you to the NY Times to figure this out. Read the directions, try playing, and come back. It makes your experience viewing this better. Here's the link: https://www.nytimes.com/games/wordle/index.html

## Compiling the Word Bank
### A Detour
To begin we need every valid word in Wordle. There are many ways to do this, at the top of our list should be stealing the list by inspecting the game's code. I did not arrive immediately at this conclusion though, so bear with me as I use the dictionary page parser to download the dictionary, then print it. I don't recommend printing it to console, I used print to send the text to a file. I've modified the file to only download the page if the file doesn't exist. While this wasn't the best thing I could have done it isn't completely worthless: I got to practice using requests.get and some bash commmands! In the dictionary_page_parser.py file, I've streamlined it so that python does all the downloading and saving to files. I will not be including the webster.txt file.

* The command I used was python3 dictionary_page_parser.py > websters.txt

Okay now that I got sidetracked we'll steal the words from wordle itself.

### Finding the Official Word Bank
Okay, now we'll get the official bank. Go to https://www.nytimes.com/games/wordle/index.html through your favorite browser. Then right click, select "Inspect", then select "Debugger", then "Sources". This should bring up a directory. Open up the following directory: "Main Thread/www.nytimes.com/games/wordle". This should make the JS file "main.e17c80f8.js" available. Right click on it and download it. I will not be including the main.e17c80f8.js file.

### Parsing the Word List
From here there are a few ways we could go about getting the words into a usable form. By the way, we should compile three sets of words. A list of solutions, a list of guesses, and the combined list. I've done that on my own. I'll include the python file I used for that, but not the files themselves. I used the lists from the JS file, it just took some formatting to make them directly usable in a python file. Then I sorted them, printed them, formatted them, and output them to files using shell commands.

## Letter Occurrence Analysis
Now comes the hard part, using the lists to solve the wordle. At this point I want to do some analysis and figure out how common letters are, if there is a prevalence of double letters, the ideal guesses, and so on. This one is going to be messy, but I'll include the images and graphs and so on. I am going back and forth on what to do with the lists of words, but for now I'll probably pull them from the files each time I need them. I've included bar graphs of occurrences of each letter in words in the "Figures" directory.

* TODO: include figures in the README.

## Solving Puzzles
Now we need to be able to search based on guesses to eliminate words from the list. I'm doing this before finding ideal words because this functionality will be needed to help in that process. The first step is finding the ideal first guess.

### Searching Words
The way that I eliminate words isn't pretty, but it works and that's what counts. Basically there are three important situations, when a letter isn't in the word, when it is in the word but we don't know where, and when we know a letter's position. I included the search_letter function for looking for the most common set of letters in words which I discuss in the next situation.

### Ideal First Guess
Looking at Answer_Words_Once.png we see that the most common letter is 'E', followed by 'A'; this might lead us to think that we should take only words with 'E', 'A', and so on. But we should search by each to see which ones we should eliminate next. I found that 'E' should be followed by 'R', 'A', 'T', and finally 'C'. This gives us the options of "CATER", "CRATE", "REACT", and "TRACE". Later on we'll find the most common positions for letters and narrow it down more, but for now one of these will do.

### Streamlining Letter Elimination
To do this we want to make a game loop of sorts to accept input of some sort to eliminate words and solve the puzzle. At this point we need to be able to get the most common letters and get guesses for them. Getting the most common letters is done in the WordList.most_common_letters() function. It currently just goes through and finds the most common letters without accounting for letters occurring together. It returns the letters in a list in most frequent, and then alphabetical order. The next step is accounting for letters occurring together.

#### Letters Occurring Together
To do this I needed a function to copy the list. It was tricky because if you just return self in the copy function the function just returns what is basically a pointer to the original list. So you have to make a new instance of the class, copy the details, and then return it. It's not pretty, but it works.

### Guess Creator
In order to generate guesses we need to carefully eliminate letters in order of frequency and return the word list. To do this without messing up the original list, we make a copy, get most common letters, and then narrow the list. It shouldn't ever give an empty list of narrowed words, but just in case I check and rerun to the step before there aren't any words left.

### Cleanup
We'll need to make it so it doesn't all break down because of a lower case letter or anything. That's easy, I have made it so guesses the user makes are all made uppercase right away.

## Actually Solving Puzzles
Now we need to make a loop that will let the user input a guess and which letters were correct and which were wrong, and so on. From there we'll move on to making a web application using Flask(maybe) to do all this.

### Getting Guesses
This is easy, just input it the guess, make sure it's valid, and off we go. From there we'll need to break down which letters are in the right position, and so on. That's just more of the same. I am going to make sure that the user answers about what letters are correct and so on are correct.

### Continuing Getting Guesses
This was harder, I wanted to make sure that it didn't just end, so we got that figured out. I also added the option to print all of the remaining answers.