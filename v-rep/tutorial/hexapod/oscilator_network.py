# -*- coding: utf-8 -*-
"""
@author: K.Brejchova
"""

import numpy as np
import pylab as pl
import oscilator_constants as const
from random import uniform
from random import randint

debug = const.debug

INIT_GAIT = const.QUADRUPED_GAIT_WEIGHTS
#INIT_GAIT = const.TRIPOD_GAIT_WEIGHTS

INIT_NEURON_STATE = 0.1
INIT_NEURON_RAND = 0.2

class Neuron:
	def __init__(self, init, unit_index):
		init = self.count_init(unit_index)
		self.last_state = init
		self.current_state = init
		if debug: print("neuron init: " + str(init))

	def add_new_record(self,state):
		self.last_state = self.current_state
		self.current_state = state

	def count_init(self, unit_index):
		init = INIT_NEURON_STATE * randint(-1, 1) + uniform(-INIT_NEURON_RAND, INIT_NEURON_RAND)
		return init

	def reset_state(self, unit_index):
		init = self.count_init(unit_index)
		self.last_state = init
		self.current_state = init

	def get_last_state(self):
		return self.last_state

class Oscilator:
	def __init__(self, unit_index):
		self.unit_index = unit_index
		self.last_inhib = [0.9, 0.9]
		self.type_of_gait = INIT_GAIT
		init = self.count_init(unit_index)
		self.neurons = [Neuron(init, unit_index), Neuron(init, unit_index)]
		self.last_state = 0

	def count_init(self, unit_index):
		neuron_base = 0.9
		init = (unit_index % 2) * (-2) * neuron_base + neuron_base
		init = INIT_NEURON_STATE + unit_index * uniform(0, 0.5)
		return init

	def sigmoid(self, x):
		res = np.arcsin(np.tanh(x))	
		return res

	def self_inhibit_delta(self, neuron_index):
		delta = - self.last_inhib[neuron_index]
		delta += max(self.neurons[neuron_index].get_last_state(), 0)
		delta /= const.T_a
		delta *= (1./const.frequency)
		return delta

	def self_inhibit(self, neuron_index):
		new_value = self.last_inhib[neuron_index] + self.self_inhibit_delta(neuron_index)
		self.last_inhib[neuron_index] = new_value
		if debug: print(self.last_inhib)
		return new_value

	def get_influenced_by_other_CPGs(self, neuron_index, last_state_values):
		value = 0
		for j in range(6):
			value += self.type_of_gait[self.unit_index][j]*max(0, last_state_values[j][neuron_index])
		return value

	def count_current_neuron_delta(self, neuron_index, last_state_values, feedback=0):
		other_neuron_index = (neuron_index + 1) % 2
		#########
		delta = -self.neurons[neuron_index].get_last_state()
		delta += const.w_fe * max(self.neurons[other_neuron_index].get_last_state(), 0)
		delta += -(const.beta[neuron_index] * self.self_inhibit(neuron_index))
		delta += const.s[neuron_index]
		delta += self.get_influenced_by_other_CPGs(neuron_index, last_state_values)
		delta += feedback
		#########
		delta /= const.T_r
		delta *= (1./const.frequency)
		if debug:print("delta: " + str(delta))
		return delta

	def count_current_neuron_state(self, neuron_index, last_state_values):
		delta = self.count_current_neuron_delta(neuron_index, last_state_values)
		new_state = self.neurons[neuron_index].get_last_state() + delta
		new_state = self.sigmoid(new_state)
		self.neurons[neuron_index].add_new_record(new_state)
		return(new_state)

	def oscilate(self, last_state_values):
		new_value = -self.count_current_neuron_state(0, last_state_values)
		new_value += self.count_current_neuron_state(1, last_state_values)
		new_value = self.sigmoid(new_value)
		self.last_state = new_value


	def change_gait(self, new_weights):
		for i in range(2):
			self.neurons[i].reset_state(self.unit_index)
		self.type_of_gait = new_weights


class OscilatorNetwork:
	def __init__(self):
		self.period = None
		self.amplitude = None
		self.new_cycle_started = [False,False,False,False,False,False]
		self.CPGunits = list()
		for i in range(0, 6):
			self.CPGunits.append(Oscilator(i))

	def oscilate_all_CPGs(self):
		last_values = self.get_last_ext_and_flex()
		last_CPG_values = []
		
		for index in range(0, 6):
			last_CPG_values.append(self.CPGunits[index].last_state)
			self.CPGunits[index].oscilate(last_values)
		
		for i in range(0, 6):
			if last_CPG_values[i] < 0 and self.CPGunits[i].last_state > 0:
				self.new_cycle_started[i] = True
			else:
				self.new_cycle_started[i] = False
		return self.new_cycle_started

	def get_last_values(self):
		values = list()
		for index in range(6):
			values.append(self.CPGunits[index].last_state)
		values = np.array(values)
		return values

	def get_last_ext_and_flex(self):
		values = list()
		for index in range(6):
			values.append([self.CPGunits[index].neurons[0].current_state, self.CPGunits[index].neurons[1].current_state])
		return values

	def set_period_and_amplitude(self):
		iterations = const.frequency * 100
		time_unit = 1./const.frequency
		period = 0
		max_value = 0
		last_state = self.CPGunits[0].last_state
		counting_started = False
		for i in range(iterations):
			self.oscilate_all_CPGs()
			new_state = self.CPGunits[0].last_state
			if max_value < np.abs(new_state):
				max_value = np.abs(new_state)
			if new_state * last_state < 0:
				if counting_started:
					period += time_unit
					break
				counting_started = True
			if counting_started:
				period += time_unit
			last_state = new_state
		self.period = period * 2
		self.amplitude = max_value
		if debug: print("period of oscilation is: " + str(self.period) + "amplitude of signal is: " + str(self.amplitude))

	def change_gait(self, new_weights):
		for i in range(6):
			self.CPGunits[i].change_gait(new_weights)


# main
if __name__ == "__main__":
	osc = OscilatorNetwork()
	data = list()
	for i in range(6):
		data.append(list())

	iterations = 120

	for i in range(iterations * const.frequency):
		osc.oscilate_all_CPGs()
		if i == 70 * const.frequency:
			osc.change_gait(const.TRIPOD_GAIT_WEIGHTS)
		for i in range(6):
			data[i].append(osc.get_last_values()[i])


	x = np.arange(0, iterations, step=1./const.frequency)
	#print(data[0])
	pl.plot(x, data[0], '-r', label='leg 1')
	pl.plot(x, data[2], '-g', label='leg 3')
	pl.plot(x, data[4], '-c', label='leg 5')
	pl.plot(x, data[1], '-b', label='leg 2')
	pl.plot(x, data[3], '-y', label='leg 4')
	pl.plot(x, data[5], '-m', label='leg 6')
	
	pl.xlabel('Sample')
	pl.ylabel('Amplitude')
	pl.title('Output of Central Pattern Generator Network')
	
	pl.legend(loc='lower left')
	pl.show()


