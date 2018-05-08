# Builds THOR executable

sm:=61 # Streaming Multiprocessor version
arch := -arch sm_$(sm)

path_hd  := $(shell pwd)/src/headers
path_src := $(shell pwd)/src
obj   := esp.o grid.o esp_initial.o planet.o thor_driver.o profx_driver.o esp_output.o
headers := $(path_hd)/define.h $(path_hd)/grid.h $(path_hd)/planet.h $(path_hd)/esp.h \
           $(path_hd)/dyn/thor_fastmodes.h $(path_hd)/dyn/thor_adv_cor.h $(path_hd)/dyn/thor_auxiliary.h \
           $(path_hd)/dyn/thor_vertical_int.h $(path_hd)/dyn/thor_slowmodes.h $(path_hd)/dyn/thor_diff.h \
           $(path_hd)/dyn/thor_div.h $(path_hd)/phy/profx_auxiliary.h $(path_hd)/phy/profx_held_suarez.h
flag := -g -G

# define where to find sources 
vpath %.cu src src/grid src/initial src/thor src/profx src/output

h5libs := $(shell h5cc -show -shlib | awk -v ORS=" " '{ for ( n=1; n<=NF; n++ ) if ($$n ~ "^-lh") print $$n  }')
h5libdir := $(shell h5cc -show -shlib | awk -v ORS=" " '{ for ( n=1; n<=NF; n++ ) if ($$n ~ "^-L") print $$n  }')
h5include := $(shell h5cc -show -shlib | awk -v ORS=" " '{ for ( n=1; n<=NF; n++ ) if ($$n ~ "^-I") print $$n  }')
$(info h5libs="$(h5libs)")
$(info h5libdir="$(h5libdir)")
$(info h5include="$(h5include)")

includehdf = $(h5include)
# Path where the hdf5 lib was installed,
# should contain `include` and `lib`
# hdf_dir := <hdf5 directory>
#
# h5lib = -L$(hdf_dir)/lib -lhdf5
# includehdf = -I$(hdf_dir)/include

OBJDIR = obj
BINDIR = bin
.PHONY: all clean

all: $(BINDIR)/esp

# build *.cu CUDA objects
$(OBJDIR)/%.o: %.cu|$(OBJDIR) 
	@echo creating $@
	nvcc $(arch) $(h5include) $(h5libdir) -dc -o $@ $< $(flag)

# create object directory if missing
$(OBJDIR) $(BINDIR):
	mkdir $@

# link *.o objects
$(BINDIR)/esp: $(addprefix $(OBJDIR)/,$(obj)) $(headers)
	@echo creating $@
	nvcc $(arch) $(h5libdir) $(h5libs) -o $(BINDIR)/esp $(addprefix $(OBJDIR)/,$(obj)) $(flag)


.phony: clean, ar
clean:
	rm bin/esp $(addprefix $(OBJDIR)/,$(obj))

