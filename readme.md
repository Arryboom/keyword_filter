# Keyword Filter

a simple nonsense sentence filter for chinese,gonna filter out low quality information sentence such as sentence that contains too much personal emotional express.

Junk news/articles etc is wasting people's life and dealing no good to our health,let's limit these shits get showed togther.

- CurrentVersion:**1.6**

>Front webpage:
bootstrap+jquery+h5

>BackendAPI:
python3.8 with FastAPI and jieba




### Running


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


### Main webpage

- submit new keyword

![](/img/1.png)


- check keyword lists
>some basic word here,if you don't like u can just delete them all and add your own custom black list keyword.

![](/img/2.png)

- test filter

![](/img/3.png)


### API

backend was simple since current it's only support black list keyword filter and some simple format filter.

check docs at  http://your_host:port/docs

should able to see something like below:


![](/img/api.png)



### tips

- backup
the word.db in your main folder is the sqlite db file that actually save your custom keywords,remember to backup it when you need redeploy or upgrade.

- API port modify
if you change the backend service running port or domain,simple edit \html\assets\js\script.min.js
```
var apiurl="http://127.0.0.1:61111"
```
to your new api url location to make it work.


### example

to work with baidu search result filter,use this tampermonkey script (change the line var ```baseapiurl="https://1.1.1.1/"``` to your host,for current browser,you need a valid ssl certificate too,if you running in local you can generate a certificate yourself and trust it)

```
// ==UserScript==
// @name         百度杀手
// @name:en      Baidu_killer
// @namespace    http://tampermonkey.net/
// @version      0.29
// @description  自动屏蔽垃圾搜索结果
// @description:en  Auto Remove all-All-ALL junks on baidu.
// @require https://cdn.staticfile.org/jquery/2.0.3/jquery.min.js
// @github	 https://www.github.com/arryboom/nodanmu
// @author       arryboom
// @match        *://*.baidu.com/*
// @run-at document-idle
// ==/UserScript==


(function() {
        var baseapiurl="https://1.1.1.1/";


var get_page_tittle=function(){
var result_db=new Array();
$(".result").filter(".c-container").each(function(){
        result=new Object();
        result.tittle=$(this).children("h3").children("a").text();
        result.id=$(this).attr("id");
        result_db.push(result);
        req=new Object();
        req.text=result.tittle;
        ajaxcheck(req,result.id);
        delete result;
        delete req;
        delete id
        });
return result_db;
}

var del_result=function(theid){
        $(".result.c-container").filter("#"+theid).remove();
}

var check_remove=function(res,theid){
        if (res.toLowerCase()=="true"){
                del_result(theid);
        }
}

var ajaxcheck=function(req,id){
                $.ajax({
        type : "POST",
        contentType: "application/json;charset=UTF-8",
        url : baseapiurl+"checkjunk/",
        data : JSON.stringify(req),
        success : function(res) {
                check_remove(res,id);
        },
        error : function(e){
                console.log(e.status);
                console.log(e.responseText);
        }
});
}


var search_rec_ajaxcheck=function(req,ztext){
                $.ajax({
        type : "POST",
        contentType: "application/json;charset=UTF-8",
        url : baseapiurl+"checkjunk/",
        data : JSON.stringify(req),
        success : function(res) {
                check_remove_recommendsearch(res,ztext);
        },
        error : function(e){
                console.log(e.status);
                console.log(e.responseText);
        }
});
}
var check_remove_recommendsearch=function(res,ztext){
if(res.toLowerCase()=="true"){
$("th").each(function(){
if($(this).children("a").text()==ztext){
        $(this).remove();
};
});}
};

var remove_shits_recommendsearch=function(){
$("th").each(function(){
search_rec=$(this).children("a").text();
zreq=new Object();
zreq.text=search_rec;
search_rec_ajaxcheck(zreq,search_rec);
delete zreq;
delete search_rec;
});}
        var remove_shits=function(){
                get_page_tittle();
        };
        setTimeout(function(){console.log("#####Eat your shits back,Baidu#####")},5000)
    document.addEventListener("DOMSubtreeModified", remove_shits);
        document.addEventListener("DOMSubtreeModified", remove_shits_recommendsearch);


})();
```
