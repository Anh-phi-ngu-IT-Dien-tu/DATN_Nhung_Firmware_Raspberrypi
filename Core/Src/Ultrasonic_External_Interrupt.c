/*
 * Ultrasonic_External_Interrupt.c
 *
 *  Created on: Jan 19, 2025
 *      Author: GIGABYTE
 */
#include "main.h"

#include "Ultrasonic_External_Interrupt.h"

void Trig_Ultrasonic1()
{
	HAL_GPIO_WritePin(Trigger_Common_GPIO, Trigger1_Pin, 0);
	HAL_GPIO_WritePin(Trigger_Common_GPIO, Trigger1_Pin, 1);
	__HAL_TIM_SET_COUNTER(&htim2,0);
	while (__HAL_TIM_GET_COUNTER (&htim2) < 10);
	HAL_GPIO_WritePin(Trigger_Common_GPIO, Trigger1_Pin, 0);

}

void Trig_Ultrasonic2()
{
	HAL_GPIO_WritePin(Trigger_Common_GPIO, Trigger2_Pin, 0);
	HAL_GPIO_WritePin(Trigger_Common_GPIO, Trigger2_Pin, 1);
	__HAL_TIM_SET_COUNTER(&htim2,0);
	while (__HAL_TIM_GET_COUNTER (&htim2) < 10);
	HAL_GPIO_WritePin(Trigger_Common_GPIO, Trigger2_Pin, 0);
}

void Trig_Ultrasonic3()
{
	HAL_GPIO_WritePin(Trigger_Common_GPIO, Trigger3_Pin, 0);
	HAL_GPIO_WritePin(Trigger_Common_GPIO, Trigger3_Pin, 1);
	__HAL_TIM_SET_COUNTER(&htim2,0);
	while (__HAL_TIM_GET_COUNTER (&htim2) < 10);
	HAL_GPIO_WritePin(Trigger_Common_GPIO, Trigger3_Pin, 0);
}

void Trig_Ultrasonic4()
{
	HAL_GPIO_WritePin(Trigger_Common_GPIO, Trigger4_Pin, 0);

	HAL_GPIO_WritePin(Trigger_Common_GPIO, Trigger4_Pin, 1);
	__HAL_TIM_SET_COUNTER(&htim2,0);
	while (__HAL_TIM_GET_COUNTER (&htim2) < 10);
	HAL_GPIO_WritePin(Trigger_Common_GPIO, Trigger4_Pin, 0);
}

void Read_Pulse(GPIO_TypeDef *GPIOx,uint16_t GPIO_Pin,Ultrasonic_Measurement_TypeDef *Ultra,uint8_t *overfloat,void (*Trig)())
{
	if(HAL_GPIO_ReadPin(GPIOx, GPIO_Pin)==GPIO_PIN_SET)
	{
		Ultra->Val1=0;
		__HAL_TIM_SET_COUNTER(&htim1,0);
		*overfloat=0;
	}
	else if(HAL_GPIO_ReadPin(GPIOx, GPIO_Pin)==GPIO_PIN_RESET)
	{
		Ultra->Val2=__HAL_TIM_GET_COUNTER(&htim1);
		Ultra->Difference=(int64_t)Ultra->Val2-(int64_t)Ultra->Val1+65536*(*overfloat);
		Ultra->Distance=((float)Ultra->Difference)*0.034/2;
		Trig();
	}
}

void Signal_Smoothing(Ultrasonic_Measurement_TypeDef *Ultra)
{
	Ultra->Filtered_Distance=alpha*Ultra->Filtered_Distancek1+beta*Ultra->Distancek1;
	Ultra->Distancek1=Ultra->Distance;
	Ultra->Filtered_Distancek1=Ultra->Filtered_Distance;
}

