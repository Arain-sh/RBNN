import matplotlib.pyplot as plt
import squarify
import random

# 数据创建
name = []*20
# income =[26688,24541,20004,19300,17800,17010,15400,11756,11721,11700,
 #          10450,10100,9309,9157,8600,8560,8150,7920,7644,7003]
income = []
for i in range(10):
    income.append(random.randint(1, 1000))
# 绘图details
colors = ['steelblue','#9999ff','red','indianred','deepskyblue','lime','magenta','violet','peru',  'green','yellow','orange','tomato','lawngreen','cyan','darkcyan','dodgerblue','teal','tan','royalblue']
plot = squarify.plot(sizes = income, # 指定绘图数据
                     label = name, # 指定标签
                     color = colors, # 指定自定义颜色
                     alpha = 0.6, # 指定透明度
                     # value = income, # 添加数值标签
                     edgecolor = 'white', # 设置边界框为白色
                     linewidth=3  # 设置边框宽度为3
                    )
# 设置标签大小为10
plt.rc('font', size=10)
# 设置标题大小
plot.set_title('BinPacking',fontdict = {'fontsize':15})
# 除坐标轴
plt.axis('off')
# 除上边框和右边框刻度
plt.tick_params(top = 'off', right = 'off')
# 图形展示
plt.show()
