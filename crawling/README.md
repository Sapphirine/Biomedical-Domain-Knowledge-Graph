# Data Crawling part

The data crawler of wiki and google scholar is shown in the dictionary.

I didn't include scrapy framework in this file, for they are not mainly used in google scholar crawling or wiki crawling, which is the main part of our work.

# Wikipedia

We are using BFS + key word detection to organize URLs, and store the fetched data into MongoDB

# Google Scholar

A Tor + Selenium environment must be built, so that the crawler could work under the agent pool with usually-changing IP address. 

