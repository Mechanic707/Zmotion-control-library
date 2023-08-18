# Zmotion控制手册

### Visual Studio开发配置

1、右击工程--属性--配置属性--c/c++常规--附加包含目录：选取move文件

2、右击工程--属性--配置属性--链接器--常规--附加库目录：选取move文件

3、右击工程--属性--配置属性--链接器--输入：zauxdll.lib zmotion.lib

4、将move文件中的zauxdll.dll和zmotion.dll文件放入visual studio工程的x64/Debug或x64/Release文件夹下（看在哪种方式下开发）

```c++
#include <zmotion.h>
#include <zauxdll2.h>
```



将motor.cpp和motor.h放入工程目录中

解决方案资源管理器--Header Files--添加--现有项--motor.h

解决方案资源管理器--Source Files--添加--现有项--motor.cpp

**!!!注意，#include 使用的是“ ”,不是< >!!!**

```c++
#include "motor.h"
```



### 连接、断开

```c++
ZMC_HANDLE g_handle;
int32 iresult;
char ip[16] = "192.168.0.11";


iresult = ZAux_OpenEth(ip, &g_handle);

if (iresult == 0)
{
     //成功
}
else
{
    //失败
}


//关闭连接
 ZAux_Close(g_handle);
```







### 运动

#### 相对运动

```c++
//@param:  g_handle
//@param:  iaxis
//@param:  speed
//@param:  distance  mm  相对+，-
//@param:  pulse   脉冲/圈
//@param:  pitch   螺距  eg:4mm
void iaxis_move(ZMC_HANDLE g_handle, int iaxis, float speed, float distance，long pulse, float pitch)
{
    float units = ((float)pulse) / pitch;

    ZAux_Direct_SetAtype(g_handle, iaxis, 1);

    ZAux_Direct_SetUnits(g_handle, iaxis, units);
    ZAux_Direct_SetInvertStep(g_handle, iaxis, 1);
    ZAux_Direct_SetSpeed(g_handle, iaxis, speed);
    ZAux_Direct_SetAccel(g_handle, iaxis, 2000);
    ZAux_Direct_SetDecel(g_handle, iaxis, 2000);
    ZAux_Direct_SetSramp(g_handle, iaxis, 100);
    //正值向右，负值向左，直线距离--单位mm
    ZAux_Direct_Single_Move(g_handle, iaxis, distance);
}
```

#### 连续运动

```c++
/**
 *连续运动
 *dir:-1, 往回跑；
 */
void iaxis_continuous_move(ZMC_HANDLE g_handle, int iaxis, float speed, int dir)
{
    units = 10000;

    ZAux_Direct_SetAtype(g_handle, iaxis, 1); //设置轴 iaxis 为脉冲输出轴
    ZAux_Direct_SetUnits(g_handle, iaxis, units); //设置轴 iaxis 轴参数以 units 个脉冲为单位
    ZAux_Direct_SetInvertStep(g_handle, iaxis, 1); //设置轴 iaxis 为脉冲+方向模式
    ZAux_Direct_SetSpeed(g_handle, iaxis, speed); //设置轴 iaxis 速度
    ZAux_Direct_SetAccel(g_handle, iaxis, 2000); //设置轴 iaxis 加速度为 2000units/s/s
    ZAux_Direct_SetDecel(g_handle, iaxis, 2000); //设置轴 iaxis 减速度为 2000units/s/s
    ZAux_Direct_SetSramp(g_handle, iaxis, 100); //设置轴 iaxisS 曲线时间 0(梯形加减速)

    ZAux_Direct_Single_Vmove(g_handle, iaxis, dir);
}



/**
 *连续运动
 *全部往回跑；
 */
void iaxis_all_reback(ZMC_HANDLE g_handle)  //复位调这个函数
{
    iaxis_continuous_move(g_handle, 0, 5, -1);
    iaxis_continuous_move(g_handle, 1, 5, 1);
    //iaxis_continuous_move(g_handle, 2, 1, 1);
   // iaxis_continuous_move(g_handle, 2, 1, 1);
    iaxis_continuous_move(g_handle, 4, 1, 1);
}


```

##### 复位配合

```c++
//放置于QT .h文件的类中
//复位
	QTimer* timer_reback;
	uint32 valuex[1];
	uint32 valuey[1];
	uint32 valuea[1];
	uint32 valueb[1];
	uint32 valuer[1];
	int flag_x = 0;
	int flag_y = 0;
	int flag_a = 0;
	int flag_b = 0;
	int flag_r = 0;

//timer的slot
void timer_reback_monitor();


//对应的.c文件
//复位
    timer_reback = new QTimer();
    timer_reback->setInterval(1); //ms
    timer_reback->stop();
    connect(timer_reback, SIGNAL(timeout()), this, SLOT(timer_reback_monitor()));

	// timer_reback->start();
//定时器中断函数
void bloodsample::timer_reback_monitor()
{
    ZAux_Direct_GetIn(g_handle, 3, valuex);//句柄-IO口-电平值：0、1
    if (valuex[0] == 1)
    {
        ZAux_Direct_SetDpos(g_handle, 0, 0);//句柄-轴号-值，，改轴号就可以。功能：设置当前位置为该轴绝对坐标原点
        ZAux_Direct_Single_Cancel(g_handle, 0, 2);//取消轴运动
        flag_x = 1;
    }

    ZAux_Direct_GetIn(g_handle, 4, valuey);
    if (valuey[0] == 1)
    {
        ZAux_Direct_SetDpos(g_handle, 1, 0);
        ZAux_Direct_Single_Cancel(g_handle, 1, 2);
        flag_y = 1;
    }

   /* ZAux_Direct_GetIn(g_handle, 5, valuea);
    if (valuea[0] == 1)
    {
        ZAux_Direct_SetDpos(g_handle, 2, 0);
        ZAux_Direct_Single_Cancel(g_handle, 2, 2);
        flag_a = 1;
    }*/

    //ZAux_Direct_GetIn(g_handle, 4, valueb);
    //if (valueb[0] == 1)
    //{
    //    ZAux_Direct_SetDpos(g_handle, 2, 0);
    //    ZAux_Direct_Single_Cancel(g_handle, 2, 2);
    //    flag_b = 1;
    //}

    ZAux_Direct_GetIn(g_handle, 7, valuer);
    if (valuer[0] == 1)
    {
        ZAux_Direct_SetDpos(g_handle, 4, 0);
        ZAux_Direct_Single_Cancel(g_handle, 4, 2);
        flag_r = 1;
    }

    if ((flag_x == 1) && (flag_y == 1)  && (flag_r == 1))  //&& (flag_a == 1)
    {
        flag_x = 0;
        flag_y = 0;
        flag_a = 0;
        flag_b = 0;
        flag_r = 0;
        timer_reback->stop();
    }

}

```



































