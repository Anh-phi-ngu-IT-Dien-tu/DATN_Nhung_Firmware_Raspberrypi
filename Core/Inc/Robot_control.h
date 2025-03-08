/*
 * Robot_control.h
 *
 *  Created on: Oct 18, 2024
 *      Author: GIGABYTE
 */

#ifndef INC_ROBOT_CONTROL_H_
#define INC_ROBOT_CONTROL_H_
#ifdef __cplusplus
 extern "C" {
#endif

#include <stdio.h>
#include <stdint.h>
#include "BTS7960_control.h"


#define WHEEL_RADIUS 32.5
#define RW_DISTANCE_WHEEL_CENTER 202.75
#define PI 3.141592654


#define STOP_COMMAND_CHARACTER 's'
#define FORWARD_COMMAND_CHARACTER 'f'
#define BACKWARD_COMMAND_CHARACTER 'b'
#define TURN_LEFT_COMMAND_CHARACTER 'l'
#define TURN_RIGHT_COMMAND_CHARACTER 'r'
#define SEND_CORRECTION_DATA 'c'


typedef struct
{

	float v;// unit mm/s
	float omega;//unit rad/s
#if Calibrate_Parameters ==1
	float x_prediction;
	float y_prediction;
	float theta_prediction;
	float delta_x;
	float delta_y;
	float s;
	float delta_theta;
#endif
	float sl;
	float sr;
	float b;


	uint8_t ultrasonic_signal;
}Robot_model_typedef;



void MCU2FrameHandler(uint8_t *rx_buffer,Robot_model_typedef *R);
void CalculateMotorsOmegas(Robot_model_typedef *R,Motor_measurement_command_typedef *M1,Motor_measurement_command_typedef *M2);
void calculatePredictionValue(Robot_model_typedef *R,float sl,float sr);
#ifdef __cplusplus
}
#endif
#endif /* INC_ROBOT_CONTROL_H_ */
