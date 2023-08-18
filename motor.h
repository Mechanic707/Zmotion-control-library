#include <zmotion.h>
#include <zauxdll2.h>
#include <iostream>
#include <math.h> 

using namespace std;

#define UNITS 800.0//全局电机细分   含义：800个脉冲转一圈
#define SPEED_ALL 5.0//全局电机转速，单位：rev/s 不建议使用

//说明：
//x,y,z输出为直线距离，单位:mm。x,y使用传动带；z使用丝杆
//a输出为角度。
//根据实际机器的轴特性，参考给出的四轴代码增改即可。


//减速比
#define RATIO_X 19.0
#define RATIO_Y 19.0
#define RATIO_Z 1.0
#define RATIO_A 100.0

//传动比
#define D_RATIO_X 156.0
#define D_RATIO_Y 78.0
//导程
#define P_Z 2.0

//x,y,z距离;
#define DISTANCE_X RATIO_X*D_RATIO_X
#define DISTANCE_Y RATIO_Y*D_RATIO_Y
#define DISTANCE_Z RATIO_Z*P_Z

//a角度
#define angle_a RATIO_A*360.0



//------------------------------电机运算逻辑部分，可不开放--------------------------
//原始电机转动圈数--相对运动
void iaxis_move_rev(ZMC_HANDLE g_handle, int iaxis, float speed, float rev);
//原始电机转动圈数--绝对运动
void iaxis_move_rev_abs(ZMC_HANDLE g_handle, int iaxis, float speed, float rev);

//x,y,z输出轴圈数
float rev_output_x(float distance);
float rev_output_y(float distance);
float rev_output_z(float distance);
//x,y,z原始轴圈数
float rev_src_x(float rev_output);
float rev_src_y(float rev_output);
float rev_src_z(float rev_output);
//x,y,z 由移动距离转化返回原始电机圈数
float distance_to_srcRev(int iaxis, float distance);

//A轴输出轴圈数
float rev_output_a(float angle);
//A轴原始轴圈数
float rev_src_a(float rev_output);
//A由转动角度转化返回原始电机圈数
float angle_to_srcRev(float angle);
//-------------------------------------------------------------------------------





//------------------------------------用户使用部分--------------------------------
//带_abs后缀的函数名为绝对坐标运动
//x,y,z单轴圈数执行
void iaxis_XYZ(ZMC_HANDLE g_handle, int iaxis, float speed, float distance);
void iaxis_XYZ_abs(ZMC_HANDLE g_handle, int iaxis, float speed, float distance);
//a单轴圈数执行
void iaxis_A(ZMC_HANDLE g_handle, int iaxis, float speed, float angle);
void iaxis_A_abs(ZMC_HANDLE g_handle, int iaxis, float speed, float angle);
//单轴连续运动
void iaxis_continuous_move(ZMC_HANDLE g_handle, int iaxis, float speed, int dir);
//全轴连续运动，用于配合回零逻辑   需要核实方向后修改函数内部的方向参数正负
void iaxis_all_reback(ZMC_HANDLE g_handle);

//测试函数，相对运动，可以忽略此函数
void motor_test(ZMC_HANDLE g_handle, int iaxis, float speed, float distance);
//-------------------------------------------------------------------------------







