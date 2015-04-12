# Sentinents

![Sentinents](http://i.imgur.com/bk0uywi.png)

[Sentinents](http://www.sentinents.me/) is a web visualization of the sentiments expressed across continents for any arbitrary topic. The goal is to give the user a feel for how any part of the world is feeling about a particular topic at any given time, **in real time**. The name is a portmanteau of "sentiment" and "continent".

The Twitter Streaming API is consumed, both sampling the whole set of tweets being sent at any given time, as well as filtering for any topic the user may be interested. From the minute the search term is entered, every tweet is collected, analyzed, and classified (with the Indico Sentiment Analysis API). Results are then streamed from the server to the browser, where they are bucketed by country and visualized on a heatmap showing relative positive and negative sentiments. Specific locations of tweets are also displayed in realtime, as they occur. Hovering over a location, and double clicking, will display more details about exactly the feelings of the region to the topic at hand.
