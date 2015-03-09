# 1. 数据选择 #
## 1.1几种选择方法 ##
* .loc 通过label选择，当找不到指定元素时会抛出KeyError，输入可以：
	* 单独的标签，如5或'a'。（注意5被解释成index的label，**并不是**指index的整数位置）
	* 标签的列表或数组['a', 'b', 'c']
	* labels的切片'a':'f'。（注意不同于普通的python切片，开始和结尾**都包括**）
	* A boolean array
* .iloc 主要用于指定位置（从axis的0到length-1）选择，但也可以用a boolean array。除非切片的索引允许冲出范围，否则超出范围的索引.iloc会抛出IndexError的异常，允许输入：
	* 一个整数，如5，这个和.loc石油区别的，**使用.loc[-1]会抛出异常而使用.iloc[-1]会返回最后一个值**
	* 一个整数的列表或数组[4, 3, 0]
	* 整数数据的切片1:7
	* A boolean array
* .ix 支持整数和标签混合输入。但是当axis是基于整数的时候，**ONLY** lable based access and not positinal access is supported. 这种情况下应明确使用哪种，是.iloc还是.loc

以loc为例，各种数据的使用（p.loc['a']等价于p.loc['a'], :, :）	
<table class="table">
	<tr><td>Object Type</td><td>Indexers</td></tr>
	<tr><td>Series</td><td>s.loc[indexer]</td></tr>
	<tr><td>DataFrame</td><td>df.loc[row_indexer,column_indexer]</td></tr>
	<tr><td>Panel</td><td>p.loc[item_indexer,major_indexer,minor_indexer]</td></tr>
</table>
