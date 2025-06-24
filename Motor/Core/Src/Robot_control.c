/*
 * Robot_control.c
 *
 *  Created on: Oct 18, 2024
 *      Author: GIGABYTE
 */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "main.h"
#include "Robot_control.h"
#include "BTS7960_control.h"


void calculatePredictionValue(Robot_model_typedef *R,float sl,float sr)
{
	R->sl=sl;
	R->sr=sr;
	R->b=2*RW_DISTANCE_WHEEL_CENTER;
#if Calibrate_Parameters==1
	R->delta_theta=(R->sr-R->sl)/(2*RW_DISTANCE_WHEEL_CENTER);
	R->s=(R->sr+R->sl)/2;
	R->delta_x=R->s*cosf(R->theta_prediction+R->delta_theta/2);
	R->delta_y=R->s*sinf(R->theta_prediction+R->delta_theta/2);
	R->x_prediction=R->x_prediction+R->delta_x;
	R->y_prediction=R->y_prediction+R->delta_y;
	R->theta_prediction=R->theta_prediction+R->delta_theta;
#endif
}

/**
 * @note This is the function we use for calculating the omega of 2 motors
 **/
void CalculateMotorsOmegas(Robot_model_typedef *R,Motor_measurement_command_typedef *M1,Motor_measurement_command_typedef *M2)
{
#if USING_ULTRASONIC ==1
	if(R->ultrasonic_signal==STOP)
	{
		M1->expected_rpm=0;
		M2->expected_rpm=0;
	}
	else
	{
		M1->expected_rpm=((R->v/(WHEEL_RADIUS))-((RW_DISTANCE_WHEEL_CENTER)*(R->omega/WHEEL_RADIUS)))/(2*PI)*60;
		M2->expected_rpm=((R->v/(WHEEL_RADIUS))+((RW_DISTANCE_WHEEL_CENTER)*(R->omega/WHEEL_RADIUS)))/(2*PI)*60;
	}
#else
	M1->expected_rpm=((R->v/(WHEEL_RADIUS))-((RW_DISTANCE_WHEEL_CENTER)*(R->omega/WHEEL_RADIUS)))/(2*PI)*60;
	M2->expected_rpm=((R->v/(WHEEL_RADIUS))+((RW_DISTANCE_WHEEL_CENTER)*(R->omega/WHEEL_RADIUS)))/(2*PI)*60;
#endif
}

/**
 * @note This is the function we use for dealing with control command that microcontroller gets from
 * 		Bluetooth
 * @note Put this function into void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart){}
 * @param rx_buffer The pointers of data we receive from UART
 * @param M1 The pointer of typedef struct that store first motor information
 * @param M2 The pointer of typedef struct that store second motor information
**/
void MCU2FrameHandler(uint8_t *rx_buffer,Robot_model_typedef *R)
{
	if(rx_buffer[0]!=0)
	{
		R->ultrasonic_signal=rx_buffer[0];
	}
	else
	{
		R->ultrasonic_signal='0';
	}
}



