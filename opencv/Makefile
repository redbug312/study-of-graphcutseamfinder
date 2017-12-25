.PHONY: build start debug

INC_LIBS = ~/opencv-2.4.13.5/include
LD_LIBS = ~/opencv-2.4.13.5/build/lib
CPP_FLAGS = -Wall -g3 -lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_stitching

build: a.cpp
	# g++ -I$(INC_LIBS) -Wl,-rpath=$(LD_LIBS) -L$(LD_LIBS) $^ $(CPP_FLAGS)
	g++ $^ $(CPP_FLAGS)

start: build
	./a.out

debug: build
	gdb a.out
