# GoogleScholarQuery

尝试自动化获取谷歌学术数据。

#### update:
V1. 尝试直接改写[Scopus_spider](https://github.com/luffylg/scopus_spider)，直接获取邮箱效果不理想。

V2. 通过投稿系统获取邮箱，使用selenium+chrome的方式，循环爬取。最大的坑在于页面等待以及Frame框架，并且使用chrome占用资源比较多。

V3. 爬取谷歌学术，搜索邮箱，进入个人学术主页。获取发表文章数和最高引用数。构建过程中坑略多，详见[博客](http://www.luffylg.cn/blog/scholar_spider.html)或代码注释。
