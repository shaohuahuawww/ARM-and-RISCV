#include <stdint.h>

extern void ee_printf(const char *fmt, ...);

/* CMSDK UART0 (MPS2+ AN385) */
#define UART0_DATA  (*(volatile uint32_t *)0x40004000U)
#define UART0_STATE (*(volatile uint32_t *)0x40004004U)
#define UART0_CTRL  (*(volatile uint32_t *)0x40004008U)
#define UART0_BAUD  (*(volatile uint32_t *)0x40004010U)

/* Arm Cortex-M3 SysTick */
#define SYST_CSR (*(volatile uint32_t *)0xE000E010U)
#define SYST_RVR (*(volatile uint32_t *)0xE000E014U)
#define SYST_CVR (*(volatile uint32_t *)0xE000E018U)

#define SYSTICK_RELOAD 0x00FFFFFFU
#ifndef SYSCLK_HZ
#define SYSCLK_HZ 25000000U
#endif

static volatile uint64_t g_systick_overflows = 0;

void SysTick_Handler(void)
{
    g_systick_overflows++;
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

static uint64_t systick_now_ticks(void)
{
    uint64_t ovf1, ovf2;
    uint32_t cvr;
    do {
        ovf1 = g_systick_overflows;
        cvr  = SYST_CVR & 0x00FFFFFFU;
        ovf2 = g_systick_overflows;
    } while (ovf1 != ovf2);
    return ovf1 * ((uint64_t)SYSTICK_RELOAD + 1ULL) + ((uint64_t)SYSTICK_RELOAD - (uint64_t)cvr);
}

int main(void)
{
    UART0_BAUD = 217U;
    UART0_CTRL = 1U;

    SYST_CSR            = 0U;
    SYST_RVR            = SYSTICK_RELOAD;
    SYST_CVR            = 0U;
    g_systick_overflows = 0ULL;
    SYST_CSR            = 0x7U;
    /* Wait until SysTick performs its initial reload from SYSTICK_RELOAD */
    while ((SYST_CVR & 0x00FFFFFFU) == 0U) {}

    uint32_t cnt = 500000U; /* 500,000 * (subs + bne) = 1,000,000 instructions */
    uint64_t t0  = systick_now_ticks();
    __asm__ volatile(
        "1:\n\t"
        "subs %0, #1\n\t"
        "bne 1b\n\t"
        : "+r"(cnt)
        :
        : "cc");
    uint64_t t1 = systick_now_ticks();
    uint64_t dt = t1 - t0;

    ee_printf("CAL_LOOP_ITERS=500000 CAL_LOOP_INSNS=1000000 CAL_DT=%lu SYSCLK_HZ=%u\n",
              (unsigned long)dt, (unsigned int)SYSCLK_HZ);
    return 0;
}
