# Top Retweets

## Description

Shows the top 10 retweeted tweets (note the retweeted_status field) in a rolling window of time, where the window's start is n minutes ago (where n is defined by the user) and the window's end is the current time.

Output continuously updates and includes the tweet text and number of times retweeted in the current rolling window. You should not use the retweet_count field, but instead count the retweets that your program actually processes.

## Details

The app refreshes (reprints the top ten retweets in the last n minutes) every 10 seconds. 

The top retweets are determined by the amount of times a tweet has been seen (processed by the program) within the rolling window of time. 

Due to the nature of the hash (described below), at times certain RTs with identical text may appear in the top ten list. The hash is built on tweet IDs, with any retweeted tweets being added as sightings to the the original tweets ID in the hash. If the text has been copy/pasted, for example, it would not have the same ID as another, so it will show up as a discrete hash entry with possible RTs coming from its ID. 

Twitter Streaming API requires a filter with at least track or a location parameter. This is currently set to one of the top retweeted users, Harry_Styles. 

### Modifications to Stream Listener

- On each new status in the stream, the data is processed and stored to a hash. The keys to this hash are tweet IDs: if the tweet is a retweet, the key is the tweet.retweet_status.id, or originating tweet's id; otherwise, the key is tweet.id. 

- The values of in this hash are lists of tuples, (tweet.text, tweet.created_at), with a new tuple added at each tweet sighting. 

- This satisfies the spec of not using the retweet_count field, but rather counting the retweets in the context of the hash. 


## To Use 
	- pip install tweepy 

	- Obtain Twitter Credentials and set in ENV

## Examples 
![Example 1](/img/example.png)

## Libraries Used

Python - https://github.com/tweepy/tweepy (example: https://github.com/tweepy/tweepy/blob/master/examples/streaming.py)
