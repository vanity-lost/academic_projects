.c.o:
	gcc -g -c $?

all: proxy 

# compile proxy program
proxy: proxy.o utils.o
	gcc -g -o proxy proxy.o utils.o

clean:
	rm -rf *.o proxy 
