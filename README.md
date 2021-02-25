# RSS-to-email
This project targeted to check new records in RSS and then send an email  
For using, please rename ```example_email_settings.txt``` to ```email_settings.txt``` and put there actual data  
Or it could be used with env file for Dockered apps. Just put actual data in env file, then type ```source example.env```  
For the first start run  
```python3 rss_to_email.py --coldstart```  
to populate current item list from the RSS  
The link to RSS source to parse located in ```rss_source.txt```  
In case you prefer dockered application:  
```docker build -t rss:1.7 .  
docker run --env-file=.env --name=rss_to_email rss:1.7  
docker start rss_to_email```  
Put this script into cron, and you will be happy. Enjoy!
