import os
import globaldata
# from scipy.interpolate import make_interp_spline


def read_file():
    '''
    # 原版
    data_path = "realtime_draw/M_Delay_sch001_0.txt"
    id_path = "realtime_draw/ttfcpro copy.txt"

    id_type_dict = parser_tick(id_path)
    # print(id_type_dict)

    id_points = parser_data(data_path, id_type_dict.keys())
    # id_points = sorted(id_points.items(), key=lambda d:d[0], reverse=False)     # 按消息号升序排列
    # print(id_points)

    return id_type_dict, id_points
    '''

    '''
    读到第一个包含 meanBitLifeTimePerPacket 的line，定位 vector 序号 -> 比如:87
    向下读
    所有开头为 87\t 的行， 都是有效数据
    '''
    project = globaldata.currentProjectInfo.path
    print(project)
    data_path = os.path.join(project, "results", "General-#0.vec")
    print(f"数据文件：{data_path}")
    vector_id = -1
    with open(data_path, 'r', encoding='utf-8') as fp:
        while True:
            try:
                line = fp.readline()
                if line == '':
                    return
                if line.find('meanBitLifeTimePerPacket') > 0: #vector 87 ......
                    strlist = line.split(' ')
                    vector_id = int(strlist[1])
                    break
                continue
            except:
                continue
    id_type_dict = {}
    id_type_dict[vector_id] = '数据包时延'
    id_points = {}
    id_points[vector_id] = [] # 4273个数据点
    with open(data_path, 'r', encoding='utf-8') as fp:
        while True:
            try:
                line = fp.readline()
                if line == '':
                    break
                # 忽略无效行
                if line.find(f'{vector_id}\t') != 0:
                    continue
                line_list = line.strip('\n').split('\t') # 比如："87\t243305\t1.178235161761\t0.011871533499\n"
                # 一行信息遗漏，跳过该行
                if len(line_list) != 4:
                    continue
                id = int(line_list[0]) #id
                print(f"id:{id}, line_list:{line_list}")
                id_points[id].append( [float(line_list[2]), float(line_list[3])] ) #某个id添加新的点
            except:
                continue
    print(len(id_points[vector_id]))
    print(id_points[vector_id].pop() )
    return id_type_dict, id_points


# 解析勾选栏文件
# 输入文件路径
# 返回消息号和消息类型的字典
# 返回格式 {id : type}（id为十进制）
def parser_tick(file_path):
    id_type = {}
    with open(file_path, 'r', encoding='utf-8') as fp:
        for line in fp: #contents like "0x302C00E9,BE"
            line_list = line.strip('\n').split(',')
            # 一行信息遗漏，跳过该行
            if len(line_list) != 2:
                continue
            # 需要将hex转为oct
            id_type[int(line_list[0], 16)] = line_list[1]
    return id_type


# 解析数据文件
# 输入文件路径和消息号列表
# 返回消息号和对应坐标点的字典
# 返回格式{id:[[x, y], [x, y], ... ,[x, y]]}（id为十进制）
def parser_data(file_path, id_list):
    id_points = {}
    for i in id_list: #keys
        id_points[i] = []
    # 解析文件，获取id, x和y
    with open(file_path, 'r', encoding='utf-8') as fp:
        for line in fp:
            # 忽略#开头的行
            if line[0] == '#':
                continue

            line_list = line.strip('\n').split(',')
            # 一行信息遗漏，跳过该行
            if len(line_list) != 4:
                continue

            id = int(line_list[1]) #id，此处是10进制
            del line_list[2]
            del line_list[1]
            id_points[id].append(line_list) #某个id添加新的点

    return id_points


if __name__ == '__main__':
    read_file()
