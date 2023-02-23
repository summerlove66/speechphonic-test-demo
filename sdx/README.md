## 高校录取最低录取分数爬虫

### 思路
1.  经简单抓包，该网站 重要数据是通过ajax请求得到，但是经过混淆的，需要通过本地js解密才能得到真实数据，另外接口有多个加密参数。
   <br>
2. 一般这种情况，如果不想花时间去分析js 和其他等反扒措施，可以直接用selenium。一个个学校点进去，然后再点到录取分数 那一栏，操作多效率低，
   这里呢 我准备采取一种，既轻松，效率还不低的方法。该方法也具有一定普遍性
   <br>
   1.  抓取所有高校 univId ，缓存到redis
   2.  读取univId,slelenium打开大学详情页， 启动中间人代理 （mitm_job.py），拦截目标数据
   3. 直接找到js 解密方法（见score.js，直接通过node 调用原来解密方法就可以了

### 运行
  1. *python  uni.py* 
  2. *mitmdump -s .\mitm_job.py -p 8888*