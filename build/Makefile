all: main

main: ../c/src/main.cpp
	g++ -DNDEBUG -g3 -O2 -Wall -Wextra -o plugin ../c/src/main.cpp 

clean: 
	rm ./plugin
