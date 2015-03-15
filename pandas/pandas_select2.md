# 2. [KEYS]方式与[Slicing ranges]的不同 #
## 2.1 使用[KEYS] ##
在pandas中也可以使用python中原有的方式[]选择数据
<table class="table table-bordered">
	<tr><td>Object Type</td><td>Selection</td><td>Return Value Type</td></tr>
	<tr><td>Series</td><td>series[label]</td><td>scalar value</td></tr>
	<tr><td>DataFrame</td><td>frame[colname]</td><td>Series corresponding to colname</td></tr>
	<tr><td>Panel</td><td>panel[itemname]</td><td>DataFrame corresponing to the itemname</td></tr>
</table>
以DataFrame为例

	df = pd.DataFrame(np.random.randn(6,4), index=list('abcdef'), columns=list('ABCD'))
	df
<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>a</th>
      <td> 1.062280</td>
      <td> 0.010478</td>
      <td>-1.545655</td>
      <td> 0.265307</td>
    </tr>
    <tr>
      <th>b</th>
      <td>-0.272014</td>
      <td> 0.232527</td>
      <td>-0.883105</td>
      <td> 0.011720</td>
    </tr>
    <tr>
      <th>c</th>
      <td>-0.401103</td>
      <td>-0.733637</td>
      <td>-0.204077</td>
      <td>-0.244202</td>
    </tr>
    <tr>
      <th>d</th>
      <td> 0.226431</td>
      <td>-0.072039</td>
      <td>-0.051135</td>
      <td> 1.135403</td>
    </tr>
    <tr>
      <th>e</th>
      <td> 0.195347</td>
      <td>-0.672573</td>
      <td> 1.364266</td>
      <td> 1.007918</td>
    </tr>
    <tr>
      <th>f</th>
      <td>-1.491043</td>
      <td> 0.774079</td>
      <td> 0.764152</td>
      <td>-2.042346</td>
    </tr>
  </tbody>
</table>
</div>
可以使用df['A'], df[['A','C']]选择的是'A', 'C'代表的列，可以使用df[0:2]，选择的是0和1列，**但不包括第2列**，不能使用df[0]。使用[切片]和使用iloc一样都是选择的列。
## 1.2 loc和.iloc对于切片的不同 ##
df.loc['a':'c']包括'c'，而df.iloc[0:2]时不包括2

	print(df.loc['a':'c'])
    print(df.iloc[0:2])
	结果：
              A         B         C         D
    a  1.062280  0.010478 -1.545655  0.265307
    b -0.272014  0.232527 -0.883105  0.011720
    c -0.401103 -0.733637 -0.204077 -0.244202
              A         B         C         D
    a  1.062280  0.010478 -1.545655  0.265307
    b -0.272014  0.232527 -0.883105  0.011720
# 3.Attribute Access  #
df.A和df[A]的结果是一样的，但使用Attribute Access有两点要注意。
## 3.1 创建新的Attribute而不是column ##
如果给不存在的Attribute赋值，创建的时Attribute而不是column

	df.E = list(range(len(df.index)))
	print(df)
	结果没有创建新的列E
	          A         B         C         D
	a  1.062280  0.010478 -1.545655  0.265307
	b -0.272014  0.232527 -0.883105  0.011720
	c -0.401103 -0.733637 -0.204077 -0.244202
	d  0.226431 -0.072039 -0.051135  1.135403
	e  0.195347 -0.672573  1.364266  1.007918
	f -1.491043  0.774079  0.764152 -2.042346
	
直接使用[]方法会创建新的列

	df['E'] = list(range(len(df.index)))
	print(df)
	结果创建了新的列E
	          A         B         C         D  E
	a  1.062280  0.010478 -1.545655  0.265307  0
	b -0.272014  0.232527 -0.883105  0.011720  1
	c -0.401103 -0.733637 -0.204077 -0.244202  2
	d  0.226431 -0.072039 -0.051135  1.135403  3
	e  0.195347 -0.672573  1.364266  1.007918  4
	f -1.491043  0.774079  0.764152 -2.042346  5
## 3.2 使用Attribute，名称有限制 ##
使用Attribute时列名称要符合python变量的定义规则，而且不能是已经存在的方法，所以df.1和df.min之类的都不能用，而使用[]则没有此类限制，df['1']和df['min']都可以使用。

# 4. Fast scalar value getting and setting #
由于使用[]方式选择数据需要区分很多情况（single-label access, slicing, boolean indexing, etc），为了判断到底要找什么需要额外的开销。所以如果是想获取一个scalar value，最快的方法是使用at和iat方法。和loc类似at提供的是基于label，而iat是基于整数位置的。	

	print(df.at['a','A'])
	print(df.iat[0,0])
	1.06227977096
	1.06227977096

# 5. Boolean indexing #
一个很常用的方式是使用boolean vectors去过滤数据，The operators are: | for or, & for and, and ~ for not，当组合使用的时候需要要括号进行分组

	df[df['A']>0]
	df[(df['A']>0)|(df['B']>0)]

## 5.1 结合map方法 ##
	df2 = pd.DataFrame({'a' : ['one', 'one', 'two', 'three', 'two', 'one', 'six'],
                 'b' : ['x', 'y', 'y', 'x', 'y', 'x', 'x'],
                 'c' : randn(7)})
	# only want 'two' or 'three'
	criterion = df2['a'].map(lambda x: x.startswith('t'))
	print(df2[criterion])

	       a  b         c
	2    two  y -0.956077
	3  three  x  0.505570
	4    two  y -0.489219

一个相同但慢一些的方法

	df2[[x.startswith('t') for x in df2['a']]]

# 6. 使用isin #
	df = pd.DataFrame({'vals': [1, 2, 3, 4], 'ids': ['a', 'b', 'f', 'n'],
	                'ids2': ['a', 'n', 'c', 'n']})
	values = ['a', 'b', 1, 3]
	print(df.isin(values))
	输出：
	     ids   ids2   vals
	0   True   True   True
	1   True  False  False
	2  False  False   True
	3  False  False  False
## 6.1 结合any()和all()方法 ##
	values = {'ids': ['a', 'b'], 'ids2': ['a', 'c'], 'vals': [1, 3]}
	row_mask = df.isin(values).any(1)
	print(df[row_mask])
	输出：
	  ids ids2  vals
	0   a    a     1
	1   b    n     2
	2   f    c     3
# 7. where()方法和Masking #
使用boolean vector选择数据得到的是数据的子集，为了获得相同shape的结果使用where方法。
Selecting values from a Series with a boolean vector generally returns a subset of the data. To guarantee that selection output has the same shape as the original data, you can use the where method in Series and DataFrame.	

## 7.1 where方法的参数 ##
where takes an optional other argument for replacement of values where the condition is False

	df.where(df < 0, -df)
默认情况下，where返回的是数据的copy，如果想改变原始数据而不是返回数据的copy可以使用inplace参数

	df_orig.where(df > 0, -df, inplace=True)
mask方法是where的反方法。