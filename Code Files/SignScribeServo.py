def letterSwitch(wordBacklog):
	sleep(2)
	stop = ["stop","sign", "scribe"]
	while True:
		sleep(0.05)
		if not wordBacklog == [] and not set(stop).issubset(set(wordBacklog)):
			for letter in wordBacklog[0]: 
				#disect first word into letters
				match letter:
					case 'a':
						#smth
						print("a")
					case 'b':
						#smth
						print("b")
					case 'c':
						print("c")
					case 'd':
						print("d")
					case 'e':
						#smth
						print("e")
					case 'f':
						#smth
						print("f")
					case 'g':
						#smth
						print("g")
					case 'h':
						#smth
						print("h")
					case 'i':
						#smth
						print("i")
					case 'j':
						#smth
						print("j")
					case 'k':
						#smth
						print("k")
					case 'l':
						#smth
						print("l")
					case 'm':
						#smth
						print("m")
					case 'n':
						#smth
						print("n")
					case 'o':
						#smth
						print("o")
					case 'p':
						#smth
						print("p")
					case 'q':
						#smth
						print("q")
					case 'r':
						#smth
						print("r")
					case 's':
						#smth
						print("s")
					case 't':
						#smth
						print("t")
					case 'u':
						#smth
						print("u")
					case 'v':
						#smth
						print("v")
					case 'w':
						#smth
						print("w")
					case 'x':
						#smth
						print("x")
					case 'y':
						#smth
						print("y")
					case 'z':
						#smth
						print("z")
					case _:
						#smth
						print("'")
			print(" ")
				
			#deprecate the same first workword here
			wordBacklog.remove(wordBacklog[0])
