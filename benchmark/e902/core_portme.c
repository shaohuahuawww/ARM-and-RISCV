#include "coremark.h"
#include "core_portme.h"
#include <stdint.h>

#if VALIDATION_RUN
volatile ee_s32 seed1_volatile = 0x3415;
volatile ee_s32 seed2_volatile = 0x3415;
volatile ee_s32 seed3_volatile = 0x66;
#endif
#if PERFORMANCE_RUN
volatile ee_s32 seed1_volatile = 0x0;
volatile ee_s32 seed2_volatile = 0x0;
volatile ee_s32 seed3_volatile = 0x66;
#endif
#if PROFILE_RUN
volatile ee_s32 seed1_volatile = 0x8;
volatile ee_s32 seed2_volatile = 0x8;
volatile ee_s32 seed3_volatile = 0x8;
#endif
volatile ee_s32 seed4_volatile = ITERATIONS;
volatile ee_s32 seed5_volatile = 0;

/* OpenE902 smart_run testbench virtual console & cycle/retire monitor registers */
#define TB_CONSOLE_ADDR ((volatile uint32_t *)0x6000fff8U)
#define TB_MON_CTRL     ((volatile uint32_t *)0x6000fff4U)

#ifndef SYSCLK_HZ
#define SYSCLK_HZ 100000000U
#endif

void uart_putc(char c)
{
    *TB_CONSOLE_ADDR = (uint32_t)(uint8_t)c;
}

static uint64_t read_mcycle64(void)
{
    uint32_t hi1, lo, hi2;
    do {
        __asm__ volatile("csrr %0, mcycleh" : "=r"(hi1));
        __asm__ volatile("csrr %0, mcycle"  : "=r"(lo));
        __asm__ volatile("csrr %0, mcycleh" : "=r"(hi2));
    } while (hi1 != hi2);
    return ((uint64_t)hi1 << 32) | (uint64_t)lo;
}

CORETIMETYPE barebones_clock(void)
{
    return read_mcycle64();
}

#define GETMYTIME(_t)              (*_t = barebones_clock())
#define MYTIMEDIFF(fin, ini)       ((fin) - (ini))
#define TIMER_RES_DIVIDER          1
#define SAMPLE_TIME_IMPLEMENTATION 1
#define EE_TICKS_PER_SEC           (SYSCLK_HZ / TIMER_RES_DIVIDER)

static CORETIMETYPE start_time_val, stop_time_val;

void start_time(void)
{
    *TB_MON_CTRL = 1U;
    GETMYTIME(&start_time_val);
}

void stop_time(void)
{
    GETMYTIME(&stop_time_val);
    *TB_MON_CTRL = 2U;
}

CORE_TICKS get_time(void)
{
    return (CORE_TICKS)(MYTIMEDIFF(stop_time_val, start_time_val));
}

secs_ret time_in_secs(CORE_TICKS ticks)
{
    return (secs_ret)(ticks / (CORE_TICKS)EE_TICKS_PER_SEC);
}

ee_u32 default_num_contexts = 1;

void portable_init(core_portable *p, int *argc, char *argv[])
{
    (void)argc;
    (void)argv;
    if (sizeof(ee_ptr_int) != sizeof(ee_u8 *)) {
        ee_printf("ERROR! Please define ee_ptr_int to a type that holds a pointer!\n");
    }
    if (sizeof(ee_u32) != 4) {
        ee_printf("ERROR! Please define ee_u32 to a 32b unsigned type!\n");
    }
    p->portable_id = 1;
}

void portable_fini(core_portable *p)
{
    uint64_t cycles = (uint64_t)get_time();
    uint32_t cyc_per_iter = (uint32_t)(cycles / (uint64_t)(ITERATIONS > 0 ? ITERATIONS : 1));
    /* CoreMark/MHz * 10000 = 1000000 * 10000 / cyc_per_iter */
    uint32_t cm_per_mhz_x10000 = (uint32_t)(10000000000ULL / (uint64_t)cyc_per_iter);
    ee_printf("[E902-PORT] Total mcycle: %u, Cycles/Iter: %u, CoreMark/MHz: %u.%04u\n",
              (unsigned int)cycles,
              (unsigned int)cyc_per_iter,
              (unsigned int)(cm_per_mhz_x10000 / 10000U),
              (unsigned int)(cm_per_mhz_x10000 % 10000U));
    p->portable_id = 0;
}
