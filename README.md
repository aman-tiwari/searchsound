# searchsound
The SEARCHSOUND project aims to capture and express the disconnected flows of emotion in the internet.

## Extenal Libraries
* NLTK
  * Wordnet (for computing word similarities)
* TwitterAPI
* Pianoputer (by Zulko, CC 3.0 Licence, available at https://github.com/Zulko/pianoputer)
    * Pygame
    * Numpy
    * Scipi

# How it works

SEARCHSOUND consumes 1% of the recent messages on twitter. It analyses the semantic distance between the words in the tweet and words commonly associated with emotions.
It converts this semantic knowledge into a series of tones, and plays them.

It has two modes: short- and long-window

* Short-window
    * Tweets are collected over a window of a few minutes to half-hour. Almost all the input data is used.
* Long-window
    * Tweets are collected over a window of weeks, months, or even a year. Every 8 hour, keywords to track are collected from news services. Tweets with these keywords are tracked, and a mean value for each 2-4 hour period is computed. Chords or a small series of tones is generated for each 2-4 hour period from this mean, and the final 'song' is produced from concatenating these.

### But how does it actually work?

It ([twitter_stream](../twitter_stream.py)) uses [TwitterAPI](https://github.com/geduldig/TwitterAPI) and `statuses/sample` to get a stream consisting of 1% of the Twitter Statuses made every second (specifically, ones made between the [657th and the 666th millisecond](http://blog.falcondai.com/2013/06/666-and-how-twitter-samples-tweets-in.html)). As these tweets come in, it uses NLTK to compute the semantic distance (using LCH similarity) between the words in the tweet and a list words representing an emotion (e.g, happiness) and a list representing its opposite (e.g, sadness). After finding whichever one is closer, it applies a special sigmoid function to the values and saves them in a file.

Then, [twitter_player](../twitter_player.py) playes those values using the [Pianoputer](https://github.com/Zulko/pianoputer), with each value corresponding to one note.

## Current Limitations

Long-window functionality isn't implemented in a usable state, it cannot gather keywords itself nor trim down input data enough to form any long-term analysis of the input data.


# Future Plans

* Fully implement long-window functionality
* Consume global searches along with Twitter
* Group all the notes in a short tweet into a chord
