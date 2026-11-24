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

/* CMSDK UART0 (MPS2+ AN385) */
#define UART0_DATA  (*(volatile uint32_t *)0x40004000U)
#define UART0_STATE (*(volatile uint32_t *)0x40004004U)
#define UART0_CTRL  (*(volatile uint32_t *)0x40004008U)
#define UART0_BAUD  (*(volatile uint32_t *)0x40004010U)

/* Arm Cortex-M3 SysTick */
#define SYST_CSR    (*(volatile uint32_t *)0xE000E010U)
#define SYST_RVR    (*(volatile uint32_t *)0xE000E014U)
#define SYST_CVR    (*(volatile uint32_t *)0xE000E018U)

/* MPS2 AN385 QEMU default system clock is 25 MHz (unless overridden in -icount) */
#ifndef SYSCLK_HZ
#define SYSCLK_HZ 25000000U
#endif

#define SYSTICK_RELOAD 0x00FFFFFFU /* 24-bit full reload (16,777,216 cycles) */

static volatile uint64_t g_systick_overflows = 0;

void SysTick_Handler(void)
{
    g_systick_overflows++;
}

static void uart_init(void)
{
    UART0_BAUD = 217U; /* ~115200 baud @ 25 MHz */
    UART0_CTRL = 1U;   /* TX Enable */
}

void uart_putc(char c)
{
    if (c == '\n') {
        while (UART0_STATE & 1U) {}
        UART0_DATA = (uint32_t)'\r';
    }
    while (UART0_STATE & 1U) {}
    UART0_DATA = (uint32_t)(uint8_t)c;
}

static void systick_init(void)
{
    SYST_CSR = 0U;
    SYST_RVR = SYSTICK_RELOAD;
    SYST_CVR = 0U;
    g_systick_overflows = 0ULL;
    /* Enable SysTick, SysTick IRQ, Processor Clock */
    SYST_CSR = 0x7U;
}

static uint64_t systick_now_ticks(void)
{
    uint64_t ovf1, ovf2;
    uint32_t cvr;
    do {
        ovf1 = g_systick_overflows;
        cvr  = SYST_CVR & 0x00FFFFFFU;
        ovf2 = g_systick_overflows;
    } while (ovf1 != ovf2);
    /* SysTick counts down from SYSTICK_RELOAD to 0 */
    return ovf1 * ((uint64_t)SYSTICK_RELOAD + 1ULL) + ((uint64_t)SYSTICK_RELOAD - (uint64_t)cvr);
}

CORETIMETYPE barebones_clock(void)
{
    return systick_now_ticks();
}

#define GETMYTIME(_t)              (*_t = barebones_clock())
#define MYTIMEDIFF(fin, ini)       ((fin) - (ini))
#define TIMER_RES_DIVIDER          1
#define SAMPLE_TIME_IMPLEMENTATION 1
#define EE_TICKS_PER_SEC           (SYSCLK_HZ / TIMER_RES_DIVIDER)

static CORETIMETYPE start_time_val, stop_time_val;

void start_time(void)
{
    GETMYTIME(&start_time_val);
}

void stop_time(void)
{
    GETMYTIME(&stop_time_val);
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
    uart_init();
    systick_init();

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
    uint64_t ticks = (uint64_t)get_time();
    uint32_t hi = (uint32_t)(ticks >> 32);
    uint32_t lo = (uint32_t)(ticks & 0xFFFFFFFFU);
    ee_printf("[M3-PORT] Total ticks (64b): 0x%08x%08x (%u low32), SYSCLK_HZ=%u\n",
              hi, lo, lo, (unsigned int)SYSCLK_HZ);
    p->portable_id = 0;
}
