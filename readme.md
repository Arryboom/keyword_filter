#Keyword Filter

a simple nonsense sentence filter for chinese,gonna filter out low infomation sentence or sentence that contains too much personal emotional express.

Junk news/articles etc is wasting people's life and deal no good to our health,let's limit these shits togther.

- CurrentVersion:**1.3**

>Front webpage:
bootstrap+jquery+h5

>BackendAPI:
python3.8 with FastAPI and jieba




###Running


1.install necessary python module:

```
pip install fastapi uvicorn
```
2.running backend service in main dir
```
uvicorn main:app --reload --port 61111
```
3.use your broswer to open /html/index.html
>if you deploy it on your webserver,it will be http://yourdomain/
>it's not recommend to deploy this project to public webserver directly,it may contains some security related problem at this version(like xss).

###Main webpage

- submit new keyword

![](/img/1.png)


- check keyword lists
>some basic word here,if you don't like u can just delete them all and add your own custom black list keyword.

![](/img/2.png)

- test filter

![](/img/3.png)


###API

backend was simple since current it's only support black list keyword filter and some simple format filter.

check docs at  http://your_host:port/docs

should able to see something like below:


![](/img/api.png)



###tips

- backup
the word.db in your main folder is the sqlite db file that actually save your custom keywords,remember to backup it when you need redeploy or upgrade.

- API port modify
if you change the backend service running port or domain,simple edit \html\assets\js\script.min.js
```
var apiurl="http://127.0.0.1:61111"
```
to your new api url location to make it work.


