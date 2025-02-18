/*
 * BTS7960_control.c
 *
 *  Created on: Jan 3, 2025
 *      Author: GIGABYTE
 */

#include <stdio.h>
#include <stdint.h>
#include "main.h"
#include "BTS7960_control.h"
#include "Robot_control.h"
#include "PID.h"

//TIM2,TIM3,TIM4,TIM1
void readEncoder(TIM_HandleTypeDef *TIM,Motor_measurement_command_typedef *M,Encoder_sign_enum_typedef s)
{
	M->current_cnt=__HAL_TIM_GET_COUNTER(TIM);

	M->current_delta=s*((float)(M->current_cnt-M->previous_cnt));

	if(M->current_delta<-60000)
	{
		M->current_delta+=65536;
	}
	else if(M->current_delta>60000)
	{
		M->current_delta-=65536;;
	}

	M->rpm_measurement=(M->current_delta*60)/(PULSE_PER_ROUND*4*SAMPLE_TIME);
	M->distance=((M->current_delta)/((float)PULSE_PER_ROUND*4))*2*WHEEL_RADIUS*PI;
	M->previous_cnt=M->current_cnt;
}

void motorControl1(Motor_measurement_command_typedef *M,float rpm,Motor_direction_enum_typedef d)
{
	if(d==CONTROL_NORMAL)
		M->current_command_rpm=rpm;
	else if(d==CONTROL_INVERT)
		M->current_command_rpm=-rpm;
	if((M->current_command_rpm>0)&&(M->previous_command_rpm>=0))
	{
		htim1.Instance->CCR1=(uint16_t)(M->current_command_rpm/MAX_RPM*MAX_CCR_VALUE);
		htim1.Instance->CCR2=0;
	}
	else if((M->current_command_rpm<0)&&(M->previous_command_rpm>0))
	{
		htim1.Instance->CCR1=0;
		htim1.Instance->CCR2=0;
		htim1.Instance->CCR2=(uint16_t)(-M->current_command_rpm/MAX_RPM*MAX_CCR_VALUE);
	}
	else if((M->current_command_rpm>0)&&(M->previous_command_rpm<0))
	{
		htim1.Instance->CCR1=0;
		htim1.Instance->CCR2=0;
		htim1.Instance->CCR1=(uint16_t)(M->current_command_rpm/MAX_RPM*MAX_CCR_VALUE);

	}
	else if((M->current_command_rpm<0)&&(M->previous_command_rpm<=0))
	{
		htim1.Instance->CCR1=0;
		htim1.Instance->CCR2=(uint16_t)(-M->current_command_rpm/MAX_RPM*MAX_CCR_VALUE);

	}
	else if(M->current_command_rpm==0)
	{
		htim1.Instance->CCR1=0;
		htim1.Instance->CCR2=0;
	}
	M->previous_command_rpm=M->current_command_rpm;
}

void motorControl2(Motor_measurement_command_typedef *M,float rpm,Motor_direction_enum_typedef d)
{
	if(d==CONTROL_NORMAL)
		M->current_command_rpm=rpm;
	else if(d==CONTROL_INVERT)
		M->current_command_rpm=-rpm;
	if((M->current_command_rpm>0)&&(M->previous_command_rpm>=0))
	{
		htim1.Instance->CCR3=(uint16_t)(M->current_command_rpm/MAX_RPM*MAX_CCR_VALUE);
		htim1.Instance->CCR4=0;
	}
	else if((M->current_command_rpm<0)&&(M->previous_command_rpm>0))
	{
		htim1.Instance->CCR3=0;
		htim1.Instance->CCR4=0;
		htim1.Instance->CCR4=(uint16_t)(-M->current_command_rpm/MAX_RPM*MAX_CCR_VALUE);
	}
	else if((M->current_command_rpm>0)&&(M->previous_command_rpm<0))
	{
		htim1.Instance->CCR3=0;
		htim1.Instance->CCR4=0;
		htim1.Instance->CCR3=(uint16_t)(M->current_command_rpm/MAX_RPM*MAX_CCR_VALUE);

	}
	else if((M->current_command_rpm<0)&&(M->previous_command_rpm<=0))
	{
		htim1.Instance->CCR3=0;
		htim1.Instance->CCR4=(uint16_t)(-M->current_command_rpm/MAX_RPM*MAX_CCR_VALUE);

	}
	else if(M->current_command_rpm==0)
	{
		htim1.Instance->CCR3=0;
		htim1.Instance->CCR4=0;
	}
	M->previous_command_rpm=M->current_command_rpm;
}

/**
 * @note This function is used for controlling motor speed with pid controller
 * 		Before using this function, activate Timer1 with PWM mode,activate other Timers with encoder mode
 * 		Put this function into a sequental rountine with a defined sample time
 * 		We also need to declare typedef struct for storing measurement values and control values
 * @param TIM This is from STM32 API Layer Driver Library
 * @param Motor pointer to a typedef struct for Motor measurement and control
 * @param pid pointer to a typedef struct for PID controllers
 * @param Motor_num define the channel of Timer1 we want to use as pwm signal for our motor
 * @param direction define the direction for motor rotation and encoder reading
 *
**/
void pidMotorControl(TIM_HandleTypeDef *TIM,Motor_measurement_command_typedef *Motor,
		PIDControllers_Typedef *pid,Motor_pwm_pin_enum_typedef Motor_num,
		Motor_direction_enum_typedef direction)
{
	if(direction==CONTROL_NORMAL)
	{
		readEncoder(TIM, Motor,READ_NORMAL);
		pidUpdate(pid, Motor->rpm_measurement, Motor->expected_rpm);
	}

	else if(direction==CONTROL_INVERT)
	{
		readEncoder(TIM, Motor, READ_MINUS);
		pidUpdate(pid, Motor->rpm_measurement,Motor->expected_rpm);
	}
	if(Motor_num==MOTOR_1)
	{
		motorControl1(Motor, pid->u, direction);
	}
	else if(Motor_num==MOTOR_2)
	{
		motorControl2(Motor, pid->u, direction);
	}

}
