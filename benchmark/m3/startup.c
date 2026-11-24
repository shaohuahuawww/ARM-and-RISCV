#include <stdint.h>

extern uint32_t _sidata;
extern uint32_t _sdata;
extern uint32_t _edata;
extern uint32_t _sbss;
extern uint32_t _ebss;
extern uint32_t __StackTop;

extern int main(void);
extern void SysTick_Handler(void);
extern void ee_printf(const char *fmt, ...);

void Reset_Handler(void);
void Default_Handler(void);
void HardFault_Handler(void);

static void qemu_semihost_exit(int code)
{
    register uint32_t r0 __asm__("r0") = 0x18; /* SYS_EXIT */
    /* On AArch32, SYS_EXIT takes the reason code directly in r1 */
    register uint32_t r1 __asm__("r1") = (code == 0) ? 0x20026U : 0x20024U;
    __asm__ volatile("bkpt 0xAB" : : "r"(r0), "r"(r1) : "memory");
    while (1) {
        __asm__ volatile("wfi");
    }
}

void Reset_Handler(void)
{
    uint32_t *src = &_sidata;
    uint32_t *dst = &_sdata;
    while (dst < &_edata) {
        *dst++ = *src++;
    }

    dst = &_sbss;
    while (dst < &_ebss) {
        *dst++ = 0;
    }

    int ret = main();
    qemu_semihost_exit(ret);
}

void HardFault_Handler(void)
{
    ee_printf("FATAL: Cortex-M3 HardFault!\n");
    qemu_semihost_exit(1);
}

void Default_Handler(void)
{
    while (1) {
        __asm__ volatile("wfi");
    }
}

__attribute__((section(".isr_vector"), used))
void (*const g_pfnVectors[])(void) = {
    (void (*)(void))(&__StackTop), /* Initial Stack Pointer */
    Reset_Handler,                 /* Reset */
    Default_Handler,               /* NMI */
    HardFault_Handler,             /* HardFault */
    Default_Handler,               /* MemManage */
    Default_Handler,               /* BusFault */
    Default_Handler,               /* UsageFault */
    0, 0, 0, 0,                    /* Reserved */
    Default_Handler,               /* SVCall */
    Default_Handler,               /* Debug Monitor */
    0,                             /* Reserved */
    Default_Handler,               /* PendSV */
    SysTick_Handler                /* SysTick */
};
