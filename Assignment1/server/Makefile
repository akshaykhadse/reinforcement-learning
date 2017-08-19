
CC = g++
COMPILE = $(CC) $(INCLUDES) ${FLAGS} $(LIBS)

SRC_DIR = .
DST_DIR = .

#Target
TARGET = bandit-environment

#Includes
INCLUDES= -I/usr/include

#Libs
LIBS = -L/usr/lib

#Flags
OSFLAGS = -Dlinux
CFLAGS = -O3 -Wall
FLAGS = ${OSFLAGS} ${CFLAGS}

#Linker flags
LDFLAGS = -lgsl -lgslcblas

#Sources
SRCS =	bandit.cpp bandit-environment.cpp

#Objects
OBJS = $(SRCS:.cpp=.o)

#Rules 	

all:: 	$(TARGET) 

.cpp.o:
	$(COMPILE) -c -o $@ $(@F:%.o=%.cpp)

bandit-environment: $(OBJS)
	$(COMPILE) -o $@ $(OBJS) ${LDFLAGS}


clean:
	rm -f $(TARGET) $(OBJS) *~

