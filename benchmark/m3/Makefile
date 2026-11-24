CC      := arm-none-eabi-gcc
OBJDUMP := arm-none-eabi-objdump
OBJCOPY := arm-none-eabi-objcopy
SIZE    := arm-none-eabi-size

OPT        ?= -O2
ITERATIONS ?= 0
RUN_TYPE   ?= PERFORMANCE_RUN
SYSCLK_HZ  ?= 25000000
EXTRA_CFLAGS ?=
TAG        ?= $(patsubst -%,%,$(OPT))

COMMON_DIR := ../common/coremark
BUILD_DIR  := build_$(TAG)

CFLAGS := -mcpu=cortex-m3 -mthumb -Wall -Wextra -ffunction-sections -fdata-sections \
          $(OPT) $(EXTRA_CFLAGS) \
          -I. -I$(COMMON_DIR) \
          -D$(RUN_TYPE)=1 -DITERATIONS=$(ITERATIONS) -DSYSCLK_HZ=$(SYSCLK_HZ) \
          -DFLAGS_STR="\"$(OPT) -mcpu=cortex-m3 -mthumb $(EXTRA_CFLAGS)\""

LDFLAGS := -mcpu=cortex-m3 -mthumb -T mps2_an385.ld -nostartfiles \
           -Wl,--gc-sections -Wl,-Map=$(BUILD_DIR)/coremark_m3.map

SRCS := startup.c core_portme.c ee_printf.c \
        $(COMMON_DIR)/core_main.c \
        $(COMMON_DIR)/core_list_join.c \
        $(COMMON_DIR)/core_matrix.c \
        $(COMMON_DIR)/core_state.c \
        $(COMMON_DIR)/core_util.c \
        $(COMMON_DIR)/cvt.c

OBJS := $(patsubst %.c,$(BUILD_DIR)/%.o,$(notdir $(SRCS)))

VPATH := .:$(COMMON_DIR)

.PHONY: all clean run calib run-calib FORCE

all: $(BUILD_DIR)/coremark_m3.elf $(BUILD_DIR)/coremark_m3.bin $(BUILD_DIR)/coremark_m3.obj
	$(SIZE) $(BUILD_DIR)/coremark_m3.elf

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

FORCE:

$(BUILD_DIR)/.cflags: FORCE | $(BUILD_DIR)
	@printf '%s\n' '$(CFLAGS)' | cmp -s - $@ || printf '%s\n' '$(CFLAGS)' > $@

$(OBJS): $(BUILD_DIR)/.cflags

$(BUILD_DIR)/%.o: %.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/coremark_m3.elf: $(OBJS) mps2_an385.ld
	$(CC) $(LDFLAGS) $(OBJS) -lc -lgcc -o $@

$(BUILD_DIR)/coremark_m3.bin: $(BUILD_DIR)/coremark_m3.elf
	$(OBJCOPY) -O binary $< $@

$(BUILD_DIR)/coremark_m3.obj: $(BUILD_DIR)/coremark_m3.elf
	$(OBJDUMP) -d -S $< > $@

run: all
	qemu-system-arm -M mps2-an385 -nographic -semihosting-config enable=on,target=native -kernel $(BUILD_DIR)/coremark_m3.elf

calib: build_calib/calib_icount.elf

build_calib:
	mkdir -p build_calib

build_calib/%.o: %.c | build_calib
	$(CC) -mcpu=cortex-m3 -mthumb -O2 -Wall -Wextra -ffunction-sections -fdata-sections -I. -I$(COMMON_DIR) -DSYSCLK_HZ=$(SYSCLK_HZ) -c $< -o $@

build_calib/calib_icount.elf: build_calib/startup.o build_calib/calib_icount.o build_calib/ee_printf.o mps2_an385.ld | build_calib
	$(CC) -mcpu=cortex-m3 -mthumb -T mps2_an385.ld -nostartfiles -Wl,--gc-sections build_calib/startup.o build_calib/calib_icount.o build_calib/ee_printf.o -lc -lgcc -o $@

run-calib: calib
	qemu-system-arm -M mps2-an385 -nographic -icount shift=0 -semihosting-config enable=on,target=native -kernel build_calib/calib_icount.elf
	qemu-system-arm -M mps2-an385 -nographic -icount shift=1 -semihosting-config enable=on,target=native -kernel build_calib/calib_icount.elf

clean:
	rm -rf build_*
