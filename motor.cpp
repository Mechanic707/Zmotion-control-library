#include "motor.h"

//x,y,z输出轴圈数
float rev_output_x(float distance)
{
    return distance / D_RATIO_X;
}
float rev_output_y(float distance)
{
    return distance / D_RATIO_Y;
}
float rev_output_z(float distance)
{
    return distance / P_Z;
}
//x,y,z原始轴圈数
float rev_src_x(float rev_output)
{
    return rev_output * RATIO_X;
}
float rev_src_y(float rev_output)
{
    return rev_output * RATIO_Y;
}
float rev_src_z(float rev_output)
{
    return rev_output * RATIO_Z;
}
//x,y,z 由移动距离转化返回原始电机圈数
float distance_to_srcRev(int iaxis, float distance)
{
    if(iaxis == 0)
    	return rev_src_x(rev_output_x(distance));
    if(iaxis == 1)
    	return rev_src_y(rev_output_y(distance));
    if(iaxis == 2)
    	return rev_src_z(rev_output_z(distance));
}

//单轴圈数执行, 此函数给下面函数打包用
void iaxis_move_rev(ZMC_HANDLE g_handle, int iaxis, float speed, float rev)
{
    ZAux_Direct_SetAtype(g_handle, iaxis, 1);

    ZAux_Direct_SetUnits(g_handle, iaxis, UNITS);
    ZAux_Direct_SetInvertStep(g_handle, iaxis, 1);
    ZAux_Direct_SetSpeed(g_handle, iaxis, speed);
    ZAux_Direct_SetAccel(g_handle, iaxis, 2000);
    ZAux_Direct_SetDecel(g_handle, iaxis, 2000);
    ZAux_Direct_SetSramp(g_handle, iaxis, 100);
    ZAux_Direct_Single_Move(g_handle, iaxis, rev);
}

void iaxis_move_rev_abs(ZMC_HANDLE g_handle, int iaxis, float speed, float rev)
{
    ZAux_Direct_SetAtype(g_handle, iaxis, 1);

    ZAux_Direct_SetUnits(g_handle, iaxis, UNITS);
    ZAux_Direct_SetInvertStep(g_handle, iaxis, 1);
    ZAux_Direct_SetSpeed(g_handle, iaxis, speed);
    ZAux_Direct_SetAccel(g_handle, iaxis, 2000);
    ZAux_Direct_SetDecel(g_handle, iaxis, 2000);
    ZAux_Direct_SetSramp(g_handle, iaxis, 100);
    ZAux_Direct_Single_MoveAbs(g_handle, iaxis, rev);
}


//x,y,z单轴圈数执行
void iaxis_XYZ(ZMC_HANDLE g_handle, int iaxis, float speed, float distance)
{
    iaxis_move_rev(g_handle, iaxis, speed, distance_to_srcRev(iaxis, distance));
}

//iaxis_move_rev_abs
void iaxis_XYZ_abs(ZMC_HANDLE g_handle, int iaxis, float speed, float distance)
{
    iaxis_move_rev_abs(g_handle, iaxis, speed, distance_to_srcRev(iaxis, distance));
}


//A轴输出轴圈数
float rev_output_a(float angle)
{
    return angle / 360.0;
}
//A轴原始轴圈数
float rev_src_a(float rev_output)
{
    return rev_output * RATIO_A;
}
//A 由转动角度转化返回原始电机圈数
float angle_to_srcRev(float angle)
{
	return rev_src_a(rev_output_a(angle));
}

//a单轴圈数执行
void iaxis_A(ZMC_HANDLE g_handle, int iaxis, float speed, float angle)
{
    iaxis_move_rev(g_handle, iaxis, speed, angle_to_srcRev(angle));
}

void iaxis_A_abs(ZMC_HANDLE g_handle, int iaxis, float speed, float angle)
{
    iaxis_move_rev_abs(g_handle, iaxis, speed, angle_to_srcRev(angle));
}

//连续运动
/**
 *连续运动
 *dir:-1, 往回跑；
 */
void iaxis_continuous_move(ZMC_HANDLE g_handle, int iaxis, float speed, int dir)
{

    ZAux_Direct_SetAtype(g_handle, iaxis, 1); //设置轴 iaxis 为脉冲输出轴
    ZAux_Direct_SetUnits(g_handle, iaxis, UNITS); //设置轴 iaxis 轴参数以 UNITS 个脉冲为单位
    ZAux_Direct_SetInvertStep(g_handle, iaxis, 1); //设置轴 iaxis 为脉冲+方向模式
    ZAux_Direct_SetSpeed(g_handle, iaxis, speed); //设置轴 iaxis 速度
    ZAux_Direct_SetAccel(g_handle, iaxis, 2000); //设置轴 iaxis 加速度为 2000UNITS/s/s
    ZAux_Direct_SetDecel(g_handle, iaxis, 2000); //设置轴 iaxis 减速度为 2000UNITS/s/s
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
    iaxis_continuous_move(g_handle, 2, 1, 1);
    iaxis_continuous_move(g_handle, 3, 1, 1);
    iaxis_continuous_move(g_handle, 4, 5, -1);
    iaxis_continuous_move(g_handle, 5, 5, 1);
    iaxis_continuous_move(g_handle, 6, 1, 1);
}



void motor_test(ZMC_HANDLE g_handle, int iaxis, float speed, float distance)
{
    float pulse = 5000.0;
    //distance = distance * 19.0;

    ZAux_Direct_SetAtype(g_handle, iaxis, 1); //设置轴 iaxis 为脉冲输出轴
    ZAux_Direct_SetUnits(g_handle, iaxis, pulse); //设置轴 iaxis 轴参数以 UNITS 个脉冲为单位
    ZAux_Direct_SetInvertStep(g_handle, iaxis, 1); //设置轴 iaxis 为脉冲+方向模式
    ZAux_Direct_SetSpeed(g_handle, iaxis, speed); //设置轴 iaxis 速度
    ZAux_Direct_SetAccel(g_handle, iaxis, 2000); //设置轴 iaxis 加速度为 2000UNITS/s/s
    ZAux_Direct_SetDecel(g_handle, iaxis, 2000); //设置轴 iaxis 减速度为 2000UNITS/s/s
    ZAux_Direct_SetSramp(g_handle, iaxis, 100); //设置轴 iaxisS 曲线时间 0(梯形加减速)

    ZAux_Direct_Single_Move(g_handle, iaxis, distance);
}




