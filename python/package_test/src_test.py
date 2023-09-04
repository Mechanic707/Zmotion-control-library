# -*- coding:UTF-8 -*-
import platform
import ctypes
import os

#platform: win x64  
#func: load zmotion dll
zauxdll = ctypes.WinDLL('zauxdll.dll')

class ZMCWrapper:

    # 初始化参数
    def __init__(self):
        self.handle = ctypes.c_void_p()
        self.sys_ip = ""
        self.sys_info = ""
        self.is_connected = False

    ################################控制器连接################################################
    def connect(self, ip, console=[]):
        if self.handle.value is not None:
            self.disconnect()
        ip_bytes = ip.encode('utf-8')
        p_ip = ctypes.c_char_p(ip_bytes)
        print("Connecting to", ip, "...")
        ret = zauxdll.ZAux_OpenEth(p_ip, ctypes.pointer(self.handle))
        msg = "Connected"
        if ret == 0:
            msg = ip + " Connected"
            self.sys_ip = ip
            self.is_connected = True
        else:
            msg = "Connection Failed, Error " + str(ret)
            self.is_connected = False
        console.append(msg)
        console.append(self.sys_info)
        return ret

    # 断开连接
    def disconnect(self):
        ret = zauxdll.ZAux_Close(self.handle)
        self.is_connected = False
        return ret

###############################轴参数设置################################################
    # 设置轴类型
    def set_atype(self, iaxis, iValue):
        ret = zauxdll.ZAux_Direct_SetAtype(self.handle, iaxis, iValue)
        if ret == 0:
            print("Set Axis (", iaxis, ") Atype:", iValue)
        else:
            print("Set Axis (", iaxis, ") Atype fail!")
        return ret

    # 设置脉冲当量
    def set_units(self, iaxis, iValue):
        ret = zauxdll.ZAux_Direct_SetUnits(self.handle, iaxis, ctypes.c_float(iValue))
        if ret == 0:
            print("Set Axis (", iaxis, ") Units:", iValue)
        else:
            print("Set Axis (", iaxis, ") Units fail!")
        return ret

    # 设置轴加速度
    def set_accel(self, iaxis, iValue):
        ret = zauxdll.ZAux_Direct_SetAccel(self.handle, iaxis, ctypes.c_float(iValue))
        if ret == 0:
            print("Set Axis (", iaxis, ") Accel:", iValue)
        else:
            print("Set Accel (", iaxis, ") Accel fail!")
        return ret

    # 设置轴减速度
    def set_decel(self, iaxis, iValue):
        ret = zauxdll.ZAux_Direct_SetDecel(self.handle, iaxis, ctypes.c_float(iValue))
        if ret == 0:
            print("Set Axis (", iaxis, ") Decel:", iValue)
        else:
            print("Set Axis (", iaxis, ") Decel fail!")
        return ret

    # 设置轴运行速度
    def set_speed(self, iaxis, iValue):
        ret = zauxdll.ZAux_Direct_SetSpeed(self.handle, iaxis, ctypes.c_float(iValue))
        if ret == 0:
            print("Set Axis (", iaxis, ") Speed:", iValue)
        else:
            print("Set Axis (", iaxis, ") Speed fail!")
        return ret
    
    #设置绝对坐标值
    def set_dpos(self, iaxis, iValue):
        zauxdll.ZAux_Direct_SetDpos(self.handle, iaxis, ctypes.c_float(iValue))

###############################轴参数读取################################################
    # 读取轴类型
    def get_atype(self, iaxis):
        iValue = (ctypes.c_int)()
        ret = zauxdll.ZAux_Direct_GetAtype(self.handle, iaxis, ctypes.byref(iValue))
        if ret == 0:
            print("Get Axis (", iaxis, ") Atype:", iValue.value)
        else:
            print("Get Axis (", iaxis, ") Atype fail!")
        return ret

    # 读取轴脉冲当量
    def get_untis(self, iaxis):
        iValue = (ctypes.c_float)()
        ret = zauxdll.ZAux_Direct_GetUnits(self.handle, iaxis, ctypes.byref(iValue))
        if ret == 0:
            print("Get Axis (", iaxis, ") Units:", iValue.value)
        else:
            print("Get Axis (", iaxis, ") Units fail!")
        return ret

     # 读取轴加速度
    def get_accel(self, iaxis):
        iValue = (ctypes.c_float)()
        ret = zauxdll.ZAux_Direct_GetAccel(self.handle, iaxis, ctypes.byref(iValue))
        if ret == 0:
            print("Get Axis (", iaxis, ") Accel:",  iValue.value)
        else:
            print("Get Axis (", iaxis, ") Accel fail!")
        return ret

    # 读取轴减速度
    def get_decel(self, iaxis):
        iValue = (ctypes.c_float)()
        ret = zauxdll.ZAux_Direct_GetDecel(self.handle, iaxis, ctypes.byref(iValue))
        if ret == 0:
            print("Get Axis (", iaxis, ") Decel:",  iValue.value)
        else:
            print("Get Axis (", iaxis, ") Decel fail!")
        return ret

    # 读取轴运行速度
    def get_speed(self, iaxis):
        iValue = (ctypes.c_float)()
        ret = zauxdll.ZAux_Direct_GetSpeed(self.handle, iaxis, ctypes.byref(iValue))
        if ret == 0:
            print("Get Axis (", iaxis, ") Speed:",  iValue.value)
        else:
            print("Get Axis (", iaxis, ") Speed fail!")
        return ret
    
    #读取IO口电平
    def get_IO_value(self, IO_num):
        value = -1
        zauxdll.ZAux_Direct_GetIn(self.handle, IO_num, value)
        return value
    
    #功能测试
    def func_test(self):
        print("test")

###############################运动调用####################################################
    # 相对直线运动
    def move(self, iaxis, iValue):
        ret = zauxdll.ZAux_Direct_Single_Move(self.handle, iaxis, ctypes.c_float(iValue))
        if ret == 0:
            print("Axis (", iaxis, ") Move:", iValue)
        else:
            print("Axis (", iaxis, ") Move Fail")
        return ret

    #绝对直线运动
    def absmove(self, iaxis, iValue):
        ret = zauxdll.ZAux_Direct_Single_MoveAbs(self.handle, iaxis, ctypes.c_float(iValue))
        if ret == 0:
            print("Axis (", iaxis, ") Move:", iValue)
        else:
            print("Axis (", iaxis, ") Move Fail")
        return ret

    # 持续运动
    def vmove(self, iaxis, idir):
        ret = zauxdll.ZAux_Direct_Single_Vmove(self.handle, iaxis, idir)
        if ret == 0:
            print("axis (", iaxis, ")Vmoving!")
        else:
            print("Vmoving fail!")
        return ret
    
    #运动停止
    def iaxis_stop(self, iaxis):
        zauxdll.ZAux_Direct_Single_Cancel(self.handle, iaxis, 2)


#------------------------------函数封装------------------------------
def test(ZMCWrapper):
    '''
    测试代码
    
    @param ZMCWrapper: zmotion控制器类

    @return: None
    '''
    ZMCWrapper.func_test()

def connect(ZMCWrapper):
    '''
    控制器连接
    
    @param ZMCWrapper: zmotion控制器类
    '''
    ZMCWrapper.connect("192.168.0.11")

def dis_connect(ZMCWrapper):
    '''
    控制器断连
    
    @param ZMCWrapper: zmotion控制器类
    '''
    ZMCWrapper.disconnect()

def iaxis_stop(ZMCWrapper, iaxis):
    '''
    单轴停止
    
    @param ZMCWrapper: zmotion控制器类
    @param iaxis: 轴号
    '''
    ZMCWrapper.iaxis_stop(iaxis)


UNITS = 400

def set_parameter(ZMCWrapper, iaxis, speed):
    '''
    设置轴参数
    
    @param ZMCWrapper: zmotion控制器类
    @param iaxis: 轴号
    @param speed: 速度 units/s
    '''
    global UNITS
    ZMCWrapper.set_atype(iaxis, 1)
    ZMCWrapper.set_units(iaxis, UNITS)
    ZMCWrapper.set_accel(iaxis, 1000)
    ZMCWrapper.set_decel(iaxis, 1000)
    ZMCWrapper.set_speed(iaxis, speed)

def get_parameter(ZMCWrapper, iaxis):
    '''
    获得轴参数
    
    @param ZMCWrapper: zmotion控制器类
    @param iaxis: 轴号
    '''
    ZMCWrapper.get_atype(iaxis)
    ZMCWrapper.get_units(iaxis)
    ZMCWrapper.get_accel(iaxis)
    ZMCWrapper.get_decel(iaxis)
    ZMCWrapper.get_speed(iaxis)

def set_dpos(ZMCWrapper, iaxis, iValue):
    '''
    设置单轴绝对坐标值
    
    @param ZMCWrapper: zmotion控制器类
    @param iaxis: 轴号
    @param iValue: 绝对坐标值
    '''
    ZMCWrapper.set_dpos(iaxis, iValue)


def iaxis_continuous_move(ZMCWrapper, iaxis, speed, dir):
    '''
    单轴回零
    
    @param ZMCWrapper: zmotion控制器类
    @param iaxis: 轴号
    @param speed: 速度 units/s
    @param dir: 方向-- 1/-1
    '''
    set_parameter(iaxis, speed)
    ZMCWrapper.vmove(iaxis, dir)




def iaxis_all_reback(ZMCWrapper):
    '''
    所有轴回零, 需要根据实际系统修改此函数内部的参数。
    使用此函数时, 在主程序中需通过线程内while或者定时器中断的方式进行IO口电平监测，
    当所有轴上的回零判断IO都为高或低(根据实际系统来定)时，结束复位操作。
    
    @param ZMCWrapper: zmotion控制器类
    '''
    iaxis_continuous_move(ZMCWrapper, 0, 5, 1)
    iaxis_continuous_move(ZMCWrapper, 1, 5, 1)
    iaxis_continuous_move(ZMCWrapper, 2, 5, 1)
    iaxis_continuous_move(ZMCWrapper, 3, 5, 1)
    iaxis_continuous_move(ZMCWrapper, 4, 5, 1)
    iaxis_continuous_move(ZMCWrapper, 5, 5, 1)

def get_allIO_value(ZMCWrapper):
    '''
    获得所有轴对应的IO的电平值
    
    @param ZMCWrapper: zmotion控制器类
    @return: IO value List, List length
    '''
    IO_value = []
    #暂时不采取循环方式，进行单IO测试
    IO_value.append(ZMCWrapper.get_IO_value(0))
    IO_value.append(ZMCWrapper.get_IO_value(1))
    IO_value.append(ZMCWrapper.get_IO_value(2))
    IO_value.append(ZMCWrapper.get_IO_value(3))
    IO_value.append(ZMCWrapper.get_IO_value(4))
    IO_value.append(ZMCWrapper.get_IO_value(5))

    length = len(IO_value)
    return IO_value, length 


#------------------------------电机逻辑------------------------------
def src_move(ZMCWrapper, iaxis, speed, rev):
    '''
    单轴原始轴相对运动
    
    @param ZMCWrapper: zmotion控制器类
    @param iaxis: 轴号
    @param speed: 速度 units/s
    @param rev: 圈数 正反值控制正反转
    '''
    set_parameter(ZMCWrapper, iaxis, speed)
    ZMCWrapper.move(iaxis, rev)

def src_move_abs(ZMCWrapper, iaxis, speed, rev):
    '''
    单轴原始轴绝对运动
    
    @param ZMCWrapper: zmotion控制器类
    @param iaxis: 轴号
    @param speed: 速度 units/s
    @param rev: 圈数 正反值控制正反转
    '''
    set_parameter(ZMCWrapper, iaxis, speed)
    ZMCWrapper.absmove(iaxis, rev)

#减速比
RATIO_iaxis  = 1.0
#传动比
D_RATIO_iaxis = 1.0
#导程
P_iaxis  = 1.0

#直线轴
def rev_output(distance, type):
    '''
    输出轴圈数计算
    
    @param distance: 输出的矢量直线运动距离 
    @param type: 0--传动带
                 1--丝杆
    @return: 输出轴需要转动的矢量圈数
    '''
    if type == 0:
        return distance / D_RATIO_iaxis
    else:
        return distance / P_iaxis

def rev_src(rev_output):
    '''
    原始轴圈数计算
    
    @param rev_output: 输出轴需要转动的矢量圈数
    @return: 原始轴轴需要转动的矢量圈数
    '''
    return rev_output * RATIO_iaxis

def distance_to_srcRev(distance):
    '''
    原始轴圈数计算
    
    @param distance: 输出的矢量直线运动距离
    @return: 原始轴轴需要转动的矢量圈数
    '''
    return rev_src(rev_output(distance))

def iaxis_move_distance(ZMCWrapper, iaxis, speed, distance):
    src_move(ZMCWrapper, iaxis, speed, distance_to_srcRev(distance))

def iaxis_moveabs_distance(ZMCWrapper, iaxis, speed, distance):
    src_move_abs(ZMCWrapper, iaxis, speed, distance_to_srcRev(distance))



#旋转轴
def rev_output_rotate(angle):
    '''
    输出轴圈数计算
    
    @param angle: 输出的矢量角度 
    @return: 输出轴需要转动的矢量圈数
    '''
    return angle / 360.0

def rev_src_rotate(rev_output):
    '''
    原始轴圈数计算
    
    @param angle: 输出轴需要转动的矢量圈数
    @return: 原始轴轴需要转动的矢量圈数
    '''
    return rev_output * RATIO_iaxis

def angle_to_srcRev(angle):
    '''
    原始轴圈数计算
    
    @param angle: 输出的矢量角度
    @return: 原始轴轴需要转动的矢量圈数
    '''
    return rev_src_rotate(rev_output_rotate(angle))

def iaxis_move_angle(ZMCWrapper, iaxis, speed, angle):
    src_move(ZMCWrapper, iaxis, speed, angle_to_srcRev(angle))

def iaxis_moveabs_angle(ZMCWrapper, iaxis, speed, angle):
    src_move_abs(ZMCWrapper, iaxis, speed, angle_to_srcRev(angle))