/*
 * BTS7960_control.h
 *
 *  Created on: Jan 3, 2025
 *      Author: GIGABYTE
 */

#ifndef INC_BTS7960_CONTROL_H_
#define INC_BTS7960_CONTROL_H_

#ifdef __cplusplus
 extern "C" {
#endif



#include "main.h"
#include "PID.h"

#define PULSE_PER_ROUND 2970
#define MAX_RPM 37
#define MAX_CCR_VALUE 1000-1
#define SAMPLE_TIME 0.02



 typedef enum
 {
 	READ_NORMAL=1,
 	READ_MINUS=-1,
 }Encoder_sign_enum_typedef;
 typedef enum
 {
 	CONTROL_NORMAL,
 	CONTROL_INVERT,
 }Motor_direction_enum_typedef;
 typedef enum
 {
 	MOTOR_1,
 	MOTOR_2,
 }Motor_pwm_pin_enum_typedef;


 typedef struct{
 	float rpm_measurement;
 	int previous_cnt;
 	int current_cnt;

 	float current_delta;

 	float previous_command_rpm;
 	float current_command_rpm;

 	float distance;

 	float expected_rpm;
}Motor_measurement_command_typedef;


void readEncoder(TIM_HandleTypeDef *TIM,Motor_measurement_command_typedef *M,Encoder_sign_enum_typedef s);
void motorControl1(Motor_measurement_command_typedef *M,float rpm,Motor_direction_enum_typedef d);
void motorControl2(Motor_measurement_command_typedef *M,float rpm,Motor_direction_enum_typedef d);
void pidMotorControl(TIM_HandleTypeDef *TIM,Motor_measurement_command_typedef *Motor,
		PIDControllers_Typedef *pid,Motor_pwm_pin_enum_typedef Motor_num,
		Motor_direction_enum_typedef direction);

#ifdef __cplusplus
}
#endif
#endif /* INC_BTS7960_CONTROL_H_ */
