
CC = g++
COMPILE = $(CC) $(INCLUDES) ${FLAGS} $(LIBS)

SRC_DIR = .
DST_DIR = .

#Target
TARGET = bandit-agent

#Includes
INCLUDES= -I/usr/include

#Libs
LIBS = -L/usr/lib

#Flags
OSFLAGS = -Dlinux
CFLAGS = -O3 -Wall
FLAGS = ${OSFLAGS} ${CFLAGS} -std=c++11

#Linker flags
LDFLAGS = -lgsl -lgslcblas

#Sources
SRCS =	bandit-agent.cpp

#Objects
OBJS = $(SRCS:.cpp=.o)

#Rules 	

all:: 	$(TARGET) 

.cpp.o:
	$(COMPILE)  -c -o $@ $(@F:%.o=%.cpp)

bandit-agent: $(OBJS)
	$(COMPILE)  -o $@ $(OBJS) ${LDFLAGS}


clean:
	rm -f $(TARGET) $(OBJS) *~
