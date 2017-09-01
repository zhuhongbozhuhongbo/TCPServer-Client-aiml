# TCPServer-Client-aiml
一款基于aiml&socket的聊天机器人v1.0

这是基于aiml和socket的聊天机器人，在运行之前，你需要先安装aiml库（具体可参考http://www.itnose.net/detail/6645553.html ）
但是，AIML解释器对中文支持不好。实际上，Python下的Pyaiml模块（解析器）已经能比较好的支持中文，但是也存在以下问题：英文单词间一般都有空格或标点区分，因此具备一种“自然分词”特性，由于中文输入没有以空格分隔的习惯，以上会在实践中造成一些不便。比如要实现有/无空格的输入匹配，就需要在规则库中同时包含这两种模式。可用上传的程序中的_init_.py AimlParser.py DefaultSubs.py Kernel.py LangSupport.py PatternMgr.py Utils.py WordSub.py这8个py文件替换原aiml库中的相应文件，这样经过测试可以较好地支持中文。
上传的文件中TCPClient.py和TCPClient_NonGraphical.py分别为tk GUI界面的客户端和非图形界面的客户端程序，TCPServer.py为服务端程序
运行时，需要先运行服务端程序TCPServer.py，再运行客户端程序，目前支持服务端与多客户端之间通信，并且用户可将自己的.aiml文件（输入文件的绝对路径，例如D:\alice\alice.aiml）上传到服务端进行学习测试

PS:
涉及到aiml语言、socket库、client与server之间文件传输，多进程等知识
在编写aiml时建议按主题来编写，并且一个主题在一个文件里，每个主题用topic来标识，在使用srai递归时，尽量使最模糊的关键词作为源pattern，举个例子：
在上传的BuyTicket.aiml文件中第85-94行则可以说明，否、不、NO、不*是等价的，我们希望得到相同的回答“那要做什么呢？”，应该让模糊匹配词 “不 *”在源category中；另外，pattern中，如果模式匹配的是英文，要全部大写，若是中文，则字与字之间需要用空格隔开；而template则没有此规定...
