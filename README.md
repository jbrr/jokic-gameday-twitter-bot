# jokic-gameday-twitter-bot

https://twitter.com/SerbianGoodbye

This is a Twitter bot that posts a video a few hours before each Nuggets game. It's created using AWS SAM, using EventBridge Scheduler to manage the custom schedule, and Lambda to post the tweet. 

## TODO:
- Include opponent team name in the tweet text
- Wait for video upload to process before trying to post tweet, otherwise it just errors out :(
- Actually deploy it on AWS instead of running it locally.