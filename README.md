# 页面分析

我们来分析一下图片精选页面

![1](http://m.qpic.cn/psb?/V10Lajvl1FgUNv/yhJteiFadlHCYQqOskFM.kLi0nGC9fpkdyOar5jeXjM!/b/dFQBAAAAAAAA&bo=UAbdA1AG3QMDByI!&rf=viewer_4)

这个页面中全部都是套图,我们打开某一套图进行查看.

![2](http://m.qpic.cn/psb?/V10Lajvl1FgUNv/Zq4sxEk8g1LLNwycqoIhzG9bJyeVmILolNHr1O4Hm9g!/b/dLwAAAAAAAAA&bo=aQdqA2kHagMDV3I!&rf=viewer_4)

一开始我想从这个页面获取高清大图,无奈这些高清大图在页面源码中没有😔.

最后右上角发现了一个**列表模式**

![列表](http://m.qpic.cn/psb?/V10Lajvl1FgUNv/SWjcrhLWxpHeILbZfa8fXXbgBHr1eSCzc9pCYapvc1Y!/b/dDUBAAAAAAAA&bo=3gbMA94GzAMDZ0I!&rf=viewer_4)

列表模式显示的都是一些缩略图,那么怎么把缩略图变成高清大图呢?

![](http://m.qpic.cn/psb?/V10Lajvl1FgUNv/FI3Qyh2cBtgt1DbmEPc3E3L2TOm9fnwCVKQdqq6BsEA!/b/dL8AAAAAAAAA&bo=agYpA2oGKQMDR2I!&rf=viewer_4)

可以将缩略图URL里面的**t\_**替换掉,就会发现缩略图就已经变成了高清大图

![](http://m.qpic.cn/psb?/V10Lajvl1FgUNv/yq3h.sNU.emodpYFyMPh*HSRxrOwEUZK6WYqbRITvmA!/b/dL8AAAAAAAAA&bo=jQXhA40F4QMDZ0I!&rf=viewer_4)

# 代码编写

## 爬虫编写

提取精选图片页面中的套图链接

	detail_urls = response.xpath("//ul[@class='content']/li/a/@href").getall()

精选图片页面中下一页的处理

	next_page = response.xpath("//div[@class='pageindex']/a[last()-1]/@href").get()
	        if next_page:
	            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

从套图页面中提取**列表模式**的链接

	list_pattern = response.xpath("//*[@id='cMode']/div/div[@class='side']/script").get()  # 提取列表模式的URL
	        list_pattern = re.findall("/photolist/.*.html", list_pattern)[0]  # 匹配列表模式的url

从列表模式中下载高清大图

	category = response.xpath("//div[@class='mini_left']/a[last()-1]/text()").get()
	image_urls = response.xpath("//ul[@id='imgList']/li/a/img/@src").getall()
	        image_urls = list(map(lambda x: x.replace("t_", ""), image_urls))  # 去除url中的"t_"得到高清大图
	        image_urls = list(map(lambda x: response.urljoin(x), image_urls))
	        yield CarhomehdItem(category=category, image_urls=image_urls)

## 编写ItemPipeline保存图片

	class ImagePipeline(ImagesPipeline):
	    def get_media_requests(self, item, info):
	        request_objs = super(ImagePipeline, self).get_media_requests(item, info)
	        for request_obj in request_objs:
	            request_obj.item = item
	        return request_objs
	
	    def file_path(self, request, response=None, info=None):
	        path = super(ImagePipeline, self).file_path(request, response, info)
	        category = request.item.get("category")
	        image_store = IMAGES_STORE
	        category_path = os.path.join(image_store, category)
	        if not os.path.exists(category_path):
	            os.mkdir(category_path)
	        image_name = path.replace("full/", "")
	        image_path = os.path.join(category_path, image_name)
	        return image_path
