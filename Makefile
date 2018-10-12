CC=g++

runner.o: 
	$(CC) -std=c++11 Runner.cpp -o Runner.o

clean:
	rm -r Runner.o 
