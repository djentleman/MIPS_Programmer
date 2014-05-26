import programmer
import assembler



def getLine(lineNo):
	return raw_input("[" + str(lineNo) + "] >> ")

def getCode():
	print "Please Enter Assembly Code - [max 8 lines]"
	print "type 'h' for help menu"
	print "type 'x' to exit"
	print "\n\n"
	lineNo = 0
	code = ""
	while 1:
		if lineNo == 8:
			print "Max Number Of Lines Reached..."
			break
		lineData = getLine(lineNo)
		if lineData == "h":
			# show help text
			pass
		elif lineData == "x":

			break

		code += lineData + "\n"
		lineNo += 1

	print "\n\n"
	print code
	print "\n"
	return code










def main():
	p = programmer.Programmer()

	while 1:
		# get code from the user
		code = getCode()
		print "Assembling Code..."
		machine_code = assembler.assemble(code)

		print "Assembled Code: \n"
		for i in range(0, len(machine_code), 2):
			print '{:08b}'.format(machine_code[i]) + " " + '{:08b}'.format(machine_code[i + 1])
		print ""

		writeIM = raw_input("Write Code To Instruction Memory? [y/n]")
		if writeIM.upper() == "Y":
			print "Writing To Instruction Memory...\n"
			p.writeBytes(machine_code)
			print "Codeload Successful!"
		exit = raw_input("Continue? [y/n]")
		if exit.upper() == "N":
			return


if __name__ == "__main__":
	main()