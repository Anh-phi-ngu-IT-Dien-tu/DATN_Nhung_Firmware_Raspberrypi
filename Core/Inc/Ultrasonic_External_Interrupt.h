/*
 * Ultrasonic_External_Interrupt.h
 *
 *  Created on: Jan 19, 2025
 *      Author: GIGABYTE
 */

#ifndef INC_ULTRASONIC_EXTERNAL_INTERRUPT_H_
#define INC_ULTRASONIC_EXTERNAL_INTERRUPT_H_
#ifdef __cplusplus
 extern "C" {
#endif

#include "main.h"
#include "stdio.h"
#include "stdint.h"

#define Trigger_Common_GPIO GPIOA
#define Trigger1_Pin GPIO_PIN_2
#define Trigger2_Pin GPIO_PIN_3
#define Trigger3_Pin GPIO_PIN_4
#define Trigger4_Pin GPIO_PIN_5
#define Buzzer_GPIO GPIOA
#define Buzzer_pin GPIO_PIN_1

#define alpha 0.996
#define beta  0.003992


#define STOP '0'
#define NO_STOP '1'
 typedef struct
 {
 	uint64_t Val1;
 	uint64_t Val2;
 	int64_t Difference ;
 	float Distance;
 	float Distancek1;
 	float Filtered_Distance;
 	float Filtered_Distancek1;
 }Ultrasonic_Measurement_TypeDef;


 void Trig_Ultrasonic1();
 void Trig_Ultrasonic2();
 void Trig_Ultrasonic3();
 void Trig_Ultrasonic4();
 void Read_Pulse(GPIO_TypeDef *GPIOx,uint16_t GPIO_Pin,Ultrasonic_Measurement_TypeDef *Ultra,
		 uint8_t *overfloat,void (*Trig)());

 void Signal_Smoothing(Ultrasonic_Measurement_TypeDef *Ultra);

#ifdef __cplusplus
}
#endif
#endif /* INC_ULTRASONIC_EXTERNAL_INTERRUPT_H_ */
