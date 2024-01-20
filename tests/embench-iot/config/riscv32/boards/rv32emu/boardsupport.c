/* Copyright HighTec EDV-Systeme GmbH 2023

   This file is part of Embench.

   SPDX-License-Identifier: GPL-3.0-or-later OR Apache-2.0 */
#include <stdio.h>
#include <time.h>

static int begin_cycle, end_cycle;
static clock_t begin, end;

#define read_csr(reg) ({ unsigned int __tmp; \
    asm volatile ("csrr %0, " #reg : "=r"(__tmp)); \
    __tmp; })

void __attribute__((noinline)) __attribute__((externally_visible))
start_trigger()
{
    begin = clock();
    begin_cycle = read_csr(cycle);
}

void __attribute__((noinline)) __attribute__((externally_visible))
stop_trigger()
{
    end_cycle = read_csr(cycle);
    end = clock();
    printf("rv32emu timer delta: %f\n", (float)(end - begin) / CLOCKS_PER_SEC);
    printf("rv32emu cycle delta: %d\n", end_cycle - begin_cycle);
}

void __attribute__((noinline))
initialise_board()
{
}
