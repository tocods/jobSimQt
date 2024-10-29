import numpy as np
# from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import matplotlib.animation as ma
from realtime_draw.parserModule import read_file
# from scipy.interpolate import interp1d
# from scipy.interpolate import splev, splrep
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg # pyqt5的画布

X_WIDTH = 30    # 横坐标宽度
X_TICK = 1
X_STEP = 1000    # 从x坐标0至数据点插值间隔
colors = ['black', 'red', 'darkorange', 'gold', 'grey', 'green', 'cyan', 'blue', 'fuchsia', 'blueviolet']     #自定义配色方案
LEFT_LIM = 100      # 左坐标轴的刻度
RIGHT_LIM = 1000    # 右坐标轴的刻度
X_SPEED = 500      # 画图速度
X_START = 0         # 画图起始坐标


class App:
    pause_flag = False
    stop_flag = False
    ax_l = None
    ax_r = None
    pl_list_l = []  # 用于表示左边的坐标轴
    pl_list_r = []  # 用于表示右边的坐标轴

    def __init__(self):
        plt.rcParams['toolbar'] = 'toolmanager'

        plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # plt.figure("Signal", facecolor='lightgray')

        self.fig = plt.figure()

        # 修改toolbar
        tmp = plt.gcf().canvas.manager.toolbar
        # tmp.remove_toolitem('home')
        tmp.remove_toolitem('forward')
        tmp.remove_toolitem('back')
        tmp.remove_toolitem('subplots')
        tmp.remove_toolitem('help')
        self.toolbar = tmp

        # 界面坐标轴刻画
        self.ax_l = self.fig.gca()  # 获取坐标轴
        self.ax_l.set_ylim(0, LEFT_LIM)  # 垂直坐标范围
        self.ax_l.set_xlim(0, X_WIDTH)      # 设置横坐标刻度
        # ticks = []
        # t = 0
        # while t <= X_WIDTH:
        #     ticks.append(t)
        #     t += X_TICK
        # self.ax_l.set_xticks(ticks)
        self.ax_r = self.ax_l.twinx()       # 右坐标轴初始化
        self.ax_r.set_ylim(0, RIGHT_LIM)         # 设置右边纵坐标刻度
        # self.ax_r.set_ylabel('城镇化率')

        # 坐标轴与图表标题
        self.ax_l.set_ylabel('y1')
        self.ax_r.set_ylabel('y2')
        self.ax_l.set_xlabel('t')
        plt.title('延迟时间', fontdict=dict(fontsize=20,family='SimHei'))
        plt.grid(linestyle=':')  # 网格线
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

        # 动画变量初始化
        self.anim = None

    # 重置线条
    def reset(self):
        if self.anim is not None:
            self.anim.event_source.stop()

        # 清除已画线条，并且将坐标轴重置
        self.ax_l.cla()
        self.ax_r.cla()
        self.ax_l.set_ylim(0, LEFT_LIM)  # 垂直坐标范围
        self.ax_l.set_xlim(0, X_WIDTH)
        # ticks = []
        # t = 0
        # while t <= X_WIDTH:
        #     ticks.append(t)
        #     t += X_TICK
        # self.ax_l.set_xticks(ticks)
        self.ax_r.set_ylim(0, RIGHT_LIM)  # 设置右边纵坐标刻度
        self.ax_r.yaxis.set_label_position("right")
        self.ax_r.yaxis.tick_right()

        self.pl_list_l = []  # 用于表示左边的坐标轴
        self.pl_list_r = []  # 用于表示右边的坐标轴

        # self.__init__()

        # 坐标轴与图表标题
        self.ax_l.set_ylabel('y1')
        self.ax_r.set_ylabel('y2')
        self.ax_l.set_xlabel('t')
        plt.title('延迟时间', fontdict=dict(fontsize=20,family='SimHei'))
        plt.grid(linestyle=':')  # 网格线

        self.pause_flag = False
        self.stop_flag = False

    # 生成plot对象
    # virtual:表示是否为虚线的bool值
    # color:指示颜色的字符串
    # left:指示左右坐标轴
    def create_pl_diy_color(self, color, name, virtual, left):
        if left:  # 左坐标轴
            if virtual:
                pl = self.ax_l.plot([], [], c=color, linestyle=':', marker='o', markerfacecolor='r', markersize=1.5,
                                    label=name)[0]       # 有很多个元素，此处取一个处理
            else:
                pl = self.ax_l.plot([], [], c=color, label=name)[0]
            pl.set_data([], [])  # 设置数据，此处给的空数据，以便于之后将生成器的数据传入
            return pl
        else:  # 右坐标轴
            if virtual:
                pl = self.ax_r.plot([], [], c=color, linestyle=':', marker='o', markerfacecolor='r', markersize=1.5,
                                    label=name)[0]     # 有很多个元素，此处取一个处理
            else:
                pl = self.ax_r.plot([], [], c=color, label=name)[0]
            pl.set_data([], [])  # 设置数据，此处给的空数据，以便于之后将生成器的数据传入
            return pl

    # 参数说明
    # virtual：指示实线虚线
    # left：指示左右坐标轴
    def create_pl_rand_color(self, name, virtual, left):
        if left:  # 左坐标轴
            if virtual:
                pl = self.ax_l.plot([], [], linestyle=':', marker='o', markerfacecolor='r', markersize=1.5,
                                    label=name)[0]  # 有很多个元素，此处取一个处理
            else:
                pl = self.ax_l.plot([], [], label=name)[0]
            pl.set_data([], [])  # 设置数据，此处给的空数据，以便于之后将生成器的数据传入
            return pl
        else:  # 右坐标轴
            if virtual:
                pl = self.ax_r.plot([], [], linestyle=':', marker='o', markerfacecolor='r', markersize=1.5,
                                    label=name)[0]  # 有很多个元素，此处取一个处理
            else:
                pl = self.ax_r.plot([], [], label=name)[0]
            pl.set_data([], [])  # 设置数据，此处给的空数据，以便于之后将生成器的数据传入
            return pl

    # 改变图像暂停/运行状态
    def run_pause(self):
        self.pause_flag = not self.pause_flag

    # 完全停止运行
    def stop(self):
        self.stop_flag = True

    # 接收生成器数据的更新函数
    def update(self, data):
        # ============stop===========
        if self.stop_flag:
            return

        x_list, v_list, delimiter = data  # 时间，生成器的值，和generator的return相对应
        for i in range(len(x_list)):
            if x_list[i] is None:
                continue
            if i < delimiter:   # 左坐标轴
                x, y = self.pl_list_l[i].get_data()

                # 获取线条点数据
                # 追加数据
                # x_tmp = float(int(x_list[i])/1000)
                x_cur = 0
                for j in range(len(x_list[i])):
                    x_cur = x_list[i][j] / 1000    # ms转化为s
                    x.append(x_cur)
                    y.append(int(v_list[i][j]))
                # y2.append(v*2-4)

                # 移动坐标轴位置，以便持续观察数据
                # 获取当前坐标轴的最小值与最大值，即坐标系的左右边界
                x_min, x_max = self.ax_l.get_xlim()
                # y_min, y_max = self.ax_r.get_ylim()
                # y_cur = int(v_list[i])
                if x_cur >= x_max:
                    # 平移坐标轴：将最小值变为当前位置减去窗口宽度，最大值变为当前值
                    self.ax_l.set_xlim(x_cur-X_WIDTH, x_cur)
                    # 坐标系起点终点都改变了，需要重新画一个画布
                    self.ax_l.figure.canvas.draw()
                # if y_cur >= y_max :
                #     # 修改数据
                #     # 平移坐标轴：将最小值变为当前位置减去窗口宽度，最大值变为当前值
                #     self.ax_r.set_ylim(0, 100)
                #     self.ax_r.figure.canvas.draw()
                # self.pl_list[i].draw()
                self.pl_list_l[i].set_data(x, y)

            else:   # 右坐标轴
                x, y = self.pl_list_r[i-delimiter].get_data()

                # 获取线条点数据
                # 追加数据
                # x_tmp = float(int(x_list[i])/1000)
                x_cur = 0
                for j in range(len(x_list[i])):
                    x_cur = x_list[i][j] / 1000  # ms转化为s
                    x.append(x_cur)
                    y.append(int(v_list[i][j]))
                # y2.append(v*2-4)

                # 移动坐标轴位置，以便持续观察数据
                # 获取当前坐标轴的最小值与最大值，即坐标系的左右边界
                x_min, x_max = self.ax_r.get_xlim()
                # y_min, y_max = self.ax_r.get_ylim()
                if x_cur >= x_max:
                    # 平移坐标轴：将最小值变为当前位置减去窗口宽度，最大值变为当前值
                    self.ax_r.set_xlim(x_cur - X_WIDTH, x_cur)
                    # 坐标系起点终点都改变了，需要重新画一个画布
                    self.ax_r.figure.canvas.draw()
                    self.ax_r.figure.canvas.draw()
                # if y_cur >= y_max :
                #     # 修改数据
                #     # 平移坐标轴：将最小值变为当前位置减去窗口宽度，最大值变为当前值
                #     self.ax_r.set_ylim(0, 100)
                #     self.ax_r.figure.canvas.draw()
                # self.pl_list[i].draw()
                self.pl_list_r[i-delimiter].set_data(x, y)
        # plt.legend()
        # =========================暂停========================
        # if x_cur >= 38275:
        #     return

    # ======同步======生成器函数
    def generator_sync(self, data_list_l, data_list_r):
        t_list = []  # 时间
        delimiter = len(data_list_l)    # 用于在data_list中分隔左右
        data_list = data_list_l + data_list_r
        line_num = len(data_list)   # 消息种类线条数量
        add_flag = False
        for i in range(line_num):
            t_list.append(0)
        max_x = 0
        while True:
            end_flag = True
            x_list, v_list = [], []
            for i in range(len(data_list)):
                # 对该条线进行循环，将小于max_x的坐标点都加入到列表中
                x, v = [], []
                while True:
                    # 确认该条线数据是否存在，不存在则添加None
                    if t_list[i] < len(data_list[i]):
                        end_flag = False    # 仍有未显示完的数据
                        x_tmp = data_list[i][t_list[i]][0]
                        if int(x_tmp) < max_x:
                            x.append(x_tmp)
                            v.append(data_list[i][t_list[i]][1])
                            # print('x:' + str(x_tmp) + '  y:' + str(data_list[i][t_list[i]][1]))
                            t_list[i] += 1
                            add_flag = True
                        else:
                            # x.append(None)
                            # v.append(None)
                            break
                    else:
                        # x.append(None)
                        # v.append(None)
                        break
                # 将该条线需要刷新的值加入到list中
                x_list.append(x)
                v_list.append(v)
            # 所有线条值已经全部显示
            if end_flag:
                yield x_list, v_list, delimiter

            # print(x, v1, v2)
            if not self.pause_flag:
                max_x += X_SPEED
            else:
                yield x_list, v_list, delimiter

            if add_flag:
                add_flag = False
                # print(max_x)
                yield x_list, v_list, delimiter
                # yield的会保存状态的返回，与return不同

    # 生成器函数
    def generator(self, data_list):
        t = 0  # 时间
        line_num = len(data_list)   # 消息种类线条数量
        while True:
            x, v = [], []
            for lt in data_list:
                # 确认该条线数据是否存在，不存在则添加None
                if t < len(lt):
                    print('x:' + str(lt[t][0]) + '  y:' + str(lt[t][1]))
                    x.append(lt[t][0])
                    v.append(lt[t][1])
                else:
                    x.append(None)
                    v.append(None)

            if not self.pause_flag:
                t += 1

            # print(x, v)
            yield x, v
                # yield的会保存状态的返回，与return不同

    # 插值函数
    def add_data(self, raw_data_list):
        new_data_list = []  # 存储插值完后的坐标值
        # 遍历所有的线条，对线条进行插值
        for value in raw_data_list:
            # 取出原来的x和y坐标
            # np_value = np.array(value).astype(np.float)
            np_value = np.array(value).astype(float)
            # 进行插值,开头加0
            x = np_value[:, 0]
            # print(X)
            y = np_value[:, 1]
            # print(Y)

            # 进行插值
            x_add = np.arange(X_START, x[0], X_STEP, dtype=float)
            # print(x_add)
            y_step = float(y[0])/len(x_add)
            # print(y[0])
            y_add = np.arange(0, y[0], y_step, dtype=float)
            # print(y_add)

            # spl = splrep(x, y)

            # x_smooth = np.linspace(x.min(), x.max(), int(x.max() - x.min()))
            # y_smooth = make_interp_spline(x, y)(x_smooth)
            # 将x，y和前面增加的数据组合起来
            x_smooth = np.hstack((x_add, x))
            y_smooth = np.hstack((y_add, y))

            np_xy = np.dstack((x_smooth, y_smooth))
            # print(np_xy)
            # np_xy = np.hstack[np.transpose(x_smooth), np.transpose(y_smooth)]
            # 插值后重新构造坐标并写入

            new_data_list.append(np_xy.tolist()[0])
        # print(new_data_list)
        return new_data_list

    # data_list_l:
    # data_list_r:
    def run(self, data_list_l, data_list_r, name_list_l, name_list_r):
        # 判断是否使用自定义的配色方案
        color_diy = False
        line_num = len(data_list_l) + len(data_list_r)
        if line_num < len(colors):           # 若是线条数量在配色方案颜色数量以下，则使用自定义配色
            color_diy = True

        # 初始化
        self.pl_list_l = []
        self.pl_list_r = []
        # 左边纵坐标
        c = 0
        for i in range(len(data_list_l)):
            if color_diy:
                pl = self.create_pl_diy_color(colors[c], name_list_l[i], False, True)
                c += 1
            else:
                pl = self.create_pl_rand_color(name_list_l[i], False, True)
            self.pl_list_l.append(pl)
        # 右边纵坐标
        for i in range(len(data_list_r)):
            if color_diy:
                pl = self.create_pl_diy_color(colors[c], name_list_r[i], True, False)
                c += 1
            else:
                pl = self.create_pl_rand_color(name_list_r[i], True, False)
            self.pl_list_r.append(pl)

        # 插值
        new_data_list_l = self.add_data(data_list_l)
        new_data_list_r = self.add_data(data_list_r)
        # new_data_list_l = data_list_l
        # new_data_list_r = data_list_r

        # 显示图例
        self.ax_r.legend(loc='upper right', frameon=False, borderaxespad=0)
        self.ax_l.legend(loc='upper left', frameon=False, borderaxespad=0)


        # 生成动画
        # save the animation object as object member to extend life span
        self.anim = ma.FuncAnimation(self.fig, self.update, self.generator_sync(new_data_list_l, new_data_list_r),
                                     blit=False, interval=5)

# if __name__ == '__main__':
#     app = App()
#     dict = read_file()
#     app.run(dict[53215491])
