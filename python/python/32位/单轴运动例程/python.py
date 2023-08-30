import platform
import ctypes

# ���л����ж�
systype = platform.system()
if systype == 'Windows':
    if platform.architecture()[0] == '64bit':
        zauxdll = ctypes.WinDLL('./zauxdll64.dll')
        print('Windows x64')
    else:
        zauxdll = ctypes.WinDLL('./zauxdll.dll')
        print('Windows x86')
elif systype == 'Darwin':
    zmcdll = ctypes.CDLL('./zmotion.dylib')
    print("macOS")
elif systype == 'Linux':
    zmcdll = ctypes.CDLL('./libbzmotion.so')
    print("Linux")
else:
    print("OS Not Supported!!")


class ZMCWrapper:

    # ��ʼ������
    def __init__(self):
        self.handle = ctypes.c_void_p()
        self.sys_ip = ""
        self.sys_info = ""
        self.is_connected = False

    ###############################����������################################################
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

    # �Ͽ�����
    def disconnect(self):
        ret = zauxdll.ZAux_Close(self.handle)
        self.is_connected = False
        return ret

###############################���������################################################
    # ����������
    def set_atype(self, iaxis, iValue):
        ret = zauxdll.ZAux_Direct_SetAtype(self.handle, iaxis, iValue)
        if ret == 0:
            print("Set Axis (", iaxis, ") Atype:", iValue)
        else:
            print("Set Axis (", iaxis, ") Atype fail!")
        return ret

    # �������嵱��
    def set_units(self, iaxis, iValue):
        ret = zauxdll.ZAux_Direct_SetUnits(self.handle, iaxis, ctypes.c_float(iValue))
        if ret == 0:
            print("Set Axis (", iaxis, ") Units:", iValue)
        else:
            print("Set Axis (", iaxis, ") Units fail!")
        return ret

    # ��������ٶ�
    def set_accel(self, iaxis, iValue):
        ret = zauxdll.ZAux_Direct_SetAccel(self.handle, iaxis, ctypes.c_float(iValue))
        if ret == 0:
            print("Set Axis (", iaxis, ") Accel:", iValue)
        else:
            print("Set Accel (", iaxis, ") Accel fail!")
        return ret

    # ��������ٶ�
    def set_decel(self, iaxis, iValue):
        ret = zauxdll.ZAux_Direct_SetDecel(self.handle, iaxis, ctypes.c_float(iValue))
        if ret == 0:
            print("Set Axis (", iaxis, ") Decel:", iValue)
        else:
            print("Set Axis (", iaxis, ") Decel fail!")
        return ret

    # �����������ٶ�
    def set_speed(self, iaxis, iValue):
        ret = zauxdll.ZAux_Direct_SetSpeed(self.handle, iaxis, ctypes.c_float(iValue))
        if ret == 0:
            print("Set Axis (", iaxis, ") Speed:", iValue)
        else:
            print("Set Axis (", iaxis, ") Speed fail!")
        return ret

###############################�������ȡ################################################
    # ��ȡ������
    def get_atype(self, iaxis):
        iValue = (ctypes.c_int)()
        ret = zauxdll.ZAux_Direct_GetAtype(self.handle, iaxis, ctypes.byref(iValue))
        if ret == 0:
            print("Get Axis (", iaxis, ") Atype:", iValue.value)
        else:
            print("Get Axis (", iaxis, ") Atype fail!")
        return ret

    # ��ȡ�����嵱��
    def get_untis(self, iaxis):
        iValue = (ctypes.c_float)()
        ret = zauxdll.ZAux_Direct_GetUnits(self.handle, iaxis, ctypes.byref(iValue))
        if ret == 0:
            print("Get Axis (", iaxis, ") Units:", iValue.value)
        else:
            print("Get Axis (", iaxis, ") Units fail!")
        return ret

    # ��ȡ����ٶ�
    def get_accel(self, iaxis):
        iValue = (ctypes.c_float)()
        ret = zauxdll.ZAux_Direct_GetAccel(self.handle, iaxis, ctypes.byref(iValue))
        if ret == 0:
            print("Get Axis (", iaxis, ") Accel:",  iValue.value)
        else:
            print("Get Axis (", iaxis, ") Accel fail!")
        return ret

    # ��ȡ����ٶ�
    def get_decel(self, iaxis):
        iValue = (ctypes.c_float)()
        ret = zauxdll.ZAux_Direct_GetDecel(self.handle, iaxis, ctypes.byref(iValue))
        if ret == 0:
            print("Get Axis (", iaxis, ") Decel:",  iValue.value)
        else:
            print("Get Axis (", iaxis, ") Decel fail!")
        return ret

    # ��ȡ�������ٶ�
    def get_speed(self, iaxis):
        iValue = (ctypes.c_float)()
        ret = zauxdll.ZAux_Direct_GetSpeed(self.handle, iaxis, ctypes.byref(iValue))
        if ret == 0:
            print("Get Axis (", iaxis, ") Speed:",  iValue.value)
        else:
            print("Get Axis (", iaxis, ") Speed fail!")
        return ret

###############################�˶�����####################################################
    # ֱ���˶�
    def move(self, iaxis, iValue):
        ret = zauxdll.ZAux_Direct_Single_Move(self.handle, iaxis, ctypes.c_float(iValue))
        if ret == 0:
            print("Axis (", iaxis, ") Move:", iValue)
        else:
            print("Axis (", iaxis, ") Move Fail")
        return ret

    # �����˶�
    def vmove(self, iaxis, idir):
        ret = zauxdll.ZAux_Direct_Single_Vmove(self.handle, iaxis, idir)
        if ret == 0:
            print("axis (", iaxis, ")Vmoving!")
        else:
            print("Vmoving fail!")
        return ret


################################����ʹ��######################################################
zaux = ZMCWrapper()
# ���ӿ�����ip   Ĭ��192.168.0.11
zaux.connect("192.168.0.11")
# ������0����
zaux.set_atype(0, 1)
zaux.set_units(0, 100)
zaux.set_accel(0, 1000)
zaux.set_decel(0, 1000)
zaux.set_speed(0, 1000)
# ��ȡ��0����
zaux.get_atype(0)
zaux.get_untis(0)
zaux.get_accel(0)
zaux.get_decel(0)
zaux.get_speed(0)
# �˶�
zaux.move(0, 100)  # ��0ֱ���˶��ƶ�100

