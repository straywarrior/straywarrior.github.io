---
layout: post
title: "写个简单的Chrome插件来屏蔽人人的某些功能"
date: 2015-02-08
categories: 
  - "javascript"
---

人人网也许做得很努力，可也改变不了用户群正在流失的事实。其实一直在努力的又何止是人人网呢，可惜不是每件事情只要努力就一定能有好结果的。不过，怎么样算是”好“？不知道，也不想深刻地去想，还不如问问自己：结果对得起自己的努力么？你真的努力了吗？

其实平常已经不太使用人人网，可还是想写这个插件来偶尔屏蔽一下人人网的某些功能，防止误操作或者手贱，比如：整天推荐各种游戏的“最近使用的应用”...

首先给Chrome插件定义一个manifest.json文件：

```
{
    "name": "RenrenWidgit",
    "version": "1.0",
    "manifest_version": 2,
    "description": "RenrenWidgit", 
    "browser_action":{ "default_icon": "renren-gray.png" }, 
    "background":{ "scripts":["background.js"] },  
    "permissions":[ "http://*.renren.com/*" ],   
    "content_scripts": [ { 
        "matches":["http://*.renren.com/*"], 
        "js": ["jquery.js", "script_renren.js"] }]
}
```

真正要用到的只是jquery.js和script\_renren.js两个东西，icon和background.js只是一个强迫症和完美主义者的恶趣味 :)。

随手找了一个是1.10.2版jquery库，其实只是用了它的选择器，JS原生的getElementById也能搞定，无奈偷懒已成习惯。

script\_renren.js定义如下：

```
$("#right-fix-info").css("display","none");
$("div.recent-app-cont").css("display","none");
chrome.extension.sendRequest({command: "Finished"}, function(response) {
  console.log(response.okay);
});
```

第一行取消显示了历史上的今天，第二行取消显示了“最近使用的应用”。之后的内容只是想提高一下自己的用户体验。它发送了一个消息给扩展后台，告诉它已经在人人页面上处理完了这些事。

background.js定义如下：

```
chrome.extension.onRequest.addListener(
    function(request, sender, sendResponse) {
    if (request.command == "Finished")
    {
      sendResponse({okay: "Everything will be fine"});
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            if (tabs.length === 0)
                return; 
            var tab = tabs[0];
            var tabId = tab.id;
            chrome.browserAction.setIcon({path:"renren.png", tabId: tabId});
        });
    }
    else
      sendResponse({}); 
});
```

background.js处理一件事情：收到前面所说的信息，然后把图标状态从灰色的改成彩色的，顺便在控制台里写一句话。

从此，只要开启插件，我的人人网就没有“最近使用的应用”和“历史上的今天”功能了。

Everything will be fine.

也许我真的不够努力。
