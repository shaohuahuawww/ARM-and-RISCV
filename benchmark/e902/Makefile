CC      := riscv64-unknown-elf-gcc
OBJDUMP := riscv64-unknown-elf-objdump
OBJCOPY := riscv64-unknown-elf-objcopy
SIZE    := riscv64-unknown-elf-size

OPT        ?= -O2
ITERATIONS ?= 2
RUN_TYPE   ?= PERFORMANCE_RUN
SYSCLK_HZ  ?= 100000000
EXTRA_CFLAGS ?=
TAG        ?= $(patsubst -%,%,$(OPT))

ROOT_DIR     := $(abspath $(CURDIR)/../..)
COMMON_DIR   := ../common/coremark
OPENE902_DIR := $(ROOT_DIR)/opene902
RTL_PATH     := $(OPENE902_DIR)/E902_RTL_FACTORY
SMART_DIR    := $(OPENE902_DIR)/smart_run
SREC2VMEM    := $(SMART_DIR)/tests/bin/Srec2vmem
CRT0_S       := $(SMART_DIR)/tests/lib/crt0.s

BUILD_DIR    := build_$(TAG)
VVP_FILE     := build_sim/xuantie_core_mon.vvp

ARCH_FLAGS   := -march=rv32emc_zicsr_zifencei -mabi=ilp32e
CFLAGS       := $(ARCH_FLAGS) -isystem /usr/include/newlib -Wall -Wextra -ffunction-sections -fdata-sections \
                $(OPT) $(EXTRA_CFLAGS) \
                -I. -I$(COMMON_DIR) \
                -D$(RUN_TYPE)=1 -DITERATIONS=$(ITERATIONS) -DSYSCLK_HZ=$(SYSCLK_HZ) \
                -DFLAGS_STR="\"$(OPT) -march=rv32emc -mabi=ilp32e $(EXTRA_CFLAGS)\""

LDFLAGS      := -T linker.lcf -nostartfiles -nostdlib $(ARCH_FLAGS) \
                -Wl,--gc-sections -Wl,-Map=$(BUILD_DIR)/coremark_e902.map

SRCS := core_portme.c ee_printf.c mem_stubs.c \
        $(COMMON_DIR)/core_main.c \
        $(COMMON_DIR)/core_list_join.c \
        $(COMMON_DIR)/core_matrix.c \
        $(COMMON_DIR)/core_state.c \
        $(COMMON_DIR)/core_util.c \
        $(COMMON_DIR)/cvt.c

OBJS := $(BUILD_DIR)/crt0.o $(patsubst %.c,$(BUILD_DIR)/%.o,$(notdir $(SRCS)))

VPATH := .:$(COMMON_DIR)

.PHONY: all rtl clean run FORCE

all: $(BUILD_DIR)/coremark_e902.elf $(BUILD_DIR)/inst.pat $(BUILD_DIR)/data.pat $(BUILD_DIR)/coremark_e902.obj
	$(SIZE) $(BUILD_DIR)/coremark_e902.elf

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

FORCE:

$(BUILD_DIR)/.cflags: FORCE | $(BUILD_DIR)
	@printf '%s\n' '$(CFLAGS)' | cmp -s - $@ || printf '%s\n' '$(CFLAGS)' > $@

$(OBJS): $(BUILD_DIR)/.cflags

$(BUILD_DIR)/crt0.o: $(CRT0_S) | $(BUILD_DIR)
	$(CC) $(ARCH_FLAGS) -c $< -o $@

$(BUILD_DIR)/%.o: %.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/coremark_e902.elf: $(OBJS) linker.lcf
	$(CC) $(LDFLAGS) $(OBJS) -lgcc -o $@

$(BUILD_DIR)/coremark_e902.obj: $(BUILD_DIR)/coremark_e902.elf
	$(OBJDUMP) -d -Mnumeric $< > $@

$(BUILD_DIR)/inst.pat $(BUILD_DIR)/data.pat: $(BUILD_DIR)/coremark_e902.elf
	$(OBJCOPY) -O srec $< $(BUILD_DIR)/coremark_e902_inst.hex -j .text* -j .rodata* -j .data* -j .sdata* -j .eh_frame*
	$(OBJCOPY) -O srec $< $(BUILD_DIR)/coremark_e902_data.hex -j .bss* -j .sbss* -j .COMMON
	$(OBJCOPY) -O srec $< $(BUILD_DIR)/coremark_e902.hex
	$(SREC2VMEM) $(BUILD_DIR)/coremark_e902_inst.hex $(BUILD_DIR)/inst.pat
	$(SREC2VMEM) $(BUILD_DIR)/coremark_e902_data.hex $(BUILD_DIR)/data.pat
	$(SREC2VMEM) $(BUILD_DIR)/coremark_e902.hex $(BUILD_DIR)/case.pat

rtl: $(VVP_FILE)

$(VVP_FILE): retire_mon.v
	mkdir -p build_sim
	cd $(SMART_DIR)/work && \
	CODE_BASE_PATH=$(RTL_PATH) \
	iverilog -o $(CURDIR)/$(VVP_FILE) -Diverilog=1 -g2012 -DIVERILOG_SIM -DNO_DUMP -DNO_MONITOR \
	  -f $(RTL_PATH)/gen_rtl/filelists/E902_asic_rtl.fl \
	  -c ../logical/filelists/smart.fl \
	  -c ../logical/filelists/tb.fl \
	  $(CURDIR)/retire_mon.v

run: all rtl
	cd $(BUILD_DIR) && vvp ../$(VVP_FILE)

clean:
	rm -rf build_*
