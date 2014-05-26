"""""""""""""""""""""""""""""
	  IMPORTANT
	 RUN AS ROOT
"""""""""""""""""""""""""""""
import RPi.GPIO as GPIO
import time

import random # TESTING PURPOSES

class Programmer:
	def __init__(self):
		self.BIT_ADDRESS_A = 16
		self.BIT_ADDRESS_B = 18
		self.BIT_ADDRESS_C = 19

		self.DATA_BIT = 15

		self.ENABLE_A = 7
		self.ENABLE_B = 8

		self.BYTE_ADDRESS_A = 10
		self.BYTE_ADDRESS_B = 11
		self.BYTE_ADDRESS_C = 12

		self.currentByte = 0 # integer between 0 and 15

		boardSetup()
		self.initPins()

	def initPins(self):
		pins = [self.BIT_ADDRESS_A, self.BIT_ADDRESS_B,  self.BIT_ADDRESS_C,
				self.DATA_BIT, self.ENABLE_A, self.ENABLE_B, self.BYTE_ADDRESS_A,
				self.BYTE_ADDRESS_B, self.BYTE_ADDRESS_C]
		for pin in pins:
			setupPin(pin)

		# set initial pin values

		# addresses and data don't matter initially
		# default setting is low (i think) but write low to the pins anyway just in case

		# the enable bits need to be set low

		setLow(self.ENABLE_A);
		setLow(self.ENABLE_B);

	def writeBit(self, bit_data, bit_address):
		# assume byte addressing has been handled by this point

		# decode bit_address, it will be a number between 0 and 7

		# start at LSB, BIT_ADDRESS_C
		pins = [self.BIT_ADDRESS_C, self.BIT_ADDRESS_B, self.BIT_ADDRESS_A]
		for i in range(len(pins)):
			GPIO.output(pins[i], int(bit_address / (2 ** i)) % 2)

		# now the address is set, the data needs to be set

		GPIO.output(self.DATA_BIT, bit_data)

		# finally, to actually write the data, the ENABLE bit needs to be set
		enable = self.ENABLE_A
		if self.currentByte > 7:
			enable = self.ENABLE_B

		setHigh(enable)
		print "Bit: " + str(bit_data)
		time.sleep(0.5)
		setLow(enable)
		time.sleep(0.5)


	def setByte(self,  byte_address):
		# sets the byte_addresses

		#  chop off MSB, MSB is handled with the enable bits during the writeBit function
		byteLSBs = byte_address % 8 

		pins = [self.BYTE_ADDRESS_C, self.BYTE_ADDRESS_B, self.BYTE_ADDRESS_A]
		for i in range(len(pins)):
			GPIO.output(pins[i], int(byteLSBs / (2 ** i)) % 2)

		# update cached data
		self.currentByte = byte_address

	def incrementByte(self):
		self.currentByte+=1
		if self.currentByte > 15:
			# overflow
			self.currentByte = 0
		self.setByte(self.currentByte)

	def writeByte(self, byte_data):
		# assume the addressing has been handled prior to this function being called
		# this function simply writes a byte to whatever byte is currently being addressed
		for i in range(8):
			bit = int(byte_data / (2 ** i)) % 2
			self.writeBit(bit, i)

	def writeBytes(self, bytes):
		self.setByte(0)
		for byte in bytes:
			print "Byte: " + str(self.currentByte)
			self.writeByte(byte)
			self.incrementByte()






def boardSetup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

def setupPin(pin):
	GPIO.setup(pin, GPIO.OUT)

def setHigh(pin):
	GPIO.output(pin, True)

def setLow(pin):
	GPIO.output(pin, False)

def main():
	boardSetup()
	p = Programmer()
	bytes = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
	p.writeBytes(bytes)


if __name__ == "__main__":
	main()
