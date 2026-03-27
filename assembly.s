.cpu cortex-a9
.fpu vfpv3-d16
.global _start
.data
    .align 3
    result_0: .double 0.0
    .align 3
    result_1: .double 0.0
    .align 3
    result_2: .double 0.0
    .align 3
    result_3: .double 0.0
    .align 3
    result_4: .double 0.0
    .align 3
    result_5: .double 0.0
    .align 3
    result_6: .double 0.0
    .align 3
    result_7: .double 0.0
    .align 3
    result_8: .double 0.0
    .align 3
    result_9: .double 0.0
    .align 3
    result_10: .double 0.0
    .align 3
    result_11: .double 0.0
    .align 3
    val_0: .double 3.14
    .align 3
    val_1: .double 2.0
    .align 3
    val_2: .double 10
    .align 3
    val_3: .double 5
    .align 3
    val_4: .double 2.5
    .align 3
    val_5: .double 4.0
    .align 3
    val_6: .double 9.0
    .align 3
    val_7: .double 3.0
    .align 3
    val_8: .double 10
    .align 3
    val_9: .double 3
    .align 3
    val_10: .double 10
    .align 3
    val_11: .double 3
    .align 3
    val_12: .double 2.0
    .align 3
    val_13: .double 8
    .align 3
    val_14: .double 100.0
    .align 3
    var_SOMA: .double 0.0
    .align 3
    val_15: .double 1.5
    .align 3
    val_16: .double 2.0
    .align 3
    val_17: .double 3.0
    .align 3
    val_18: .double 4.0
    .align 3
    val_19: .double 3.0
    .align 3
    val_20: .double 4.0
    .align 3
    val_21: .double 2.0
    .align 3
    val_22: .double 5.0

.text
_start:
    @ Habilitar VFP
    VMRS r0, FPEXC
    ORR  r0, r0, #0x40000000
    VMSR FPEXC, r0

    @ Carregar 3.14
    LDR  r0, =val_0
    VLDR d0, [r0]
    VPUSH {d0}
    @ Carregar 2.0
    LDR  r0, =val_1
    VLDR d0, [r0]
    VPUSH {d0}
    @ OP +
    VPOP  {d1}
    VPOP  {d0}
    VADD.F64 d2, d0, d1
    VPUSH {d2}
    VPOP  {d0}
    LDR   r1, =result_0
    VSTR  d0, [r1]
    @ Exibir resultado via JTAG UART (1 casa decimal)
    VMOV.F64 d3, d0
    LDR   r5, =0xFF201000
    VCMP.F64 d3, #0
    VMRS  APSR_nzcv, FPSCR
    BGE   _uart_pos_0
    MOV   r0, #0x2D
    STR   r0, [r5]
    VNEG.F64 d3, d3
_uart_pos_0:
    VCVT.S32.F64 s4, d3
    VMOV  r4, s4
    CMP   r4, #0
    BNE   _uart_conv_0
    MOV   r0, #0x30
    STR   r0, [r5]
    B     _uart_dot_0
_uart_conv_0:
    MOV   r6, #0
    LDR   r9, =0xCCCCCCCD
_uart_loop_0:
    CMP   r4, #0
    BEQ   _uart_print_0
    UMULL r0, r1, r4, r9
    LSR   r1, r1, #3
    MOV   r0, #10
    MUL   r2, r1, r0
    SUB   r2, r4, r2
    MOV   r4, r1
    ADD   r2, r2, #0x30
    PUSH  {r2}
    ADD   r6, r6, #1
    B     _uart_loop_0
_uart_print_0:
    CMP   r6, #0
    BEQ   _uart_dot_0
    POP   {r0}
    STR   r0, [r5]
    SUB   r6, r6, #1
    B     _uart_print_0
_uart_dot_0:
    MOV   r0, #0x2E
    STR   r0, [r5]
    VCVT.F64.S32 d1, s4
    VSUB.F64 d1, d3, d1
    MOV   r0, #10
    VMOV  s8, r0
    VCVT.F64.S32 d4, s8
    VMUL.F64 d1, d1, d4
    VCVT.S32.F64 s4, d1
    VMOV  r0, s4
    ADD   r0, r0, #0x30
    STR   r0, [r5]
    MOV   r0, #0x0A
    STR   r0, [r5]
    @ Carregar 10
    LDR  r0, =val_2
    VLDR d0, [r0]
    VPUSH {d0}
    @ Carregar 5
    LDR  r0, =val_3
    VLDR d0, [r0]
    VPUSH {d0}
    @ OP -
    VPOP  {d1}
    VPOP  {d0}
    VSUB.F64 d2, d0, d1
    VPUSH {d2}
    VPOP  {d0}
    LDR   r1, =result_1
    VSTR  d0, [r1]
    @ Exibir resultado via JTAG UART (1 casa decimal)
    VMOV.F64 d3, d0
    LDR   r5, =0xFF201000
    VCMP.F64 d3, #0
    VMRS  APSR_nzcv, FPSCR
    BGE   _uart_pos_1
    MOV   r0, #0x2D
    STR   r0, [r5]
    VNEG.F64 d3, d3
_uart_pos_1:
    VCVT.S32.F64 s4, d3
    VMOV  r4, s4
    CMP   r4, #0
    BNE   _uart_conv_1
    MOV   r0, #0x30
    STR   r0, [r5]
    B     _uart_dot_1
_uart_conv_1:
    MOV   r6, #0
    LDR   r9, =0xCCCCCCCD
_uart_loop_1:
    CMP   r4, #0
    BEQ   _uart_print_1
    UMULL r0, r1, r4, r9
    LSR   r1, r1, #3
    MOV   r0, #10
    MUL   r2, r1, r0
    SUB   r2, r4, r2
    MOV   r4, r1
    ADD   r2, r2, #0x30
    PUSH  {r2}
    ADD   r6, r6, #1
    B     _uart_loop_1
_uart_print_1:
    CMP   r6, #0
    BEQ   _uart_dot_1
    POP   {r0}
    STR   r0, [r5]
    SUB   r6, r6, #1
    B     _uart_print_1
_uart_dot_1:
    MOV   r0, #0x2E
    STR   r0, [r5]
    VCVT.F64.S32 d1, s4
    VSUB.F64 d1, d3, d1
    MOV   r0, #10
    VMOV  s8, r0
    VCVT.F64.S32 d4, s8
    VMUL.F64 d1, d1, d4
    VCVT.S32.F64 s4, d1
    VMOV  r0, s4
    ADD   r0, r0, #0x30
    STR   r0, [r5]
    MOV   r0, #0x0A
    STR   r0, [r5]
    @ Carregar 2.5
    LDR  r0, =val_4
    VLDR d0, [r0]
    VPUSH {d0}
    @ Carregar 4.0
    LDR  r0, =val_5
    VLDR d0, [r0]
    VPUSH {d0}
    @ OP *
    VPOP  {d1}
    VPOP  {d0}
    VMUL.F64 d2, d0, d1
    VPUSH {d2}
    VPOP  {d0}
    LDR   r1, =result_2
    VSTR  d0, [r1]
    @ Exibir resultado via JTAG UART (1 casa decimal)
    VMOV.F64 d3, d0
    LDR   r5, =0xFF201000
    VCMP.F64 d3, #0
    VMRS  APSR_nzcv, FPSCR
    BGE   _uart_pos_2
    MOV   r0, #0x2D
    STR   r0, [r5]
    VNEG.F64 d3, d3
_uart_pos_2:
    VCVT.S32.F64 s4, d3
    VMOV  r4, s4
    CMP   r4, #0
    BNE   _uart_conv_2
    MOV   r0, #0x30
    STR   r0, [r5]
    B     _uart_dot_2
_uart_conv_2:
    MOV   r6, #0
    LDR   r9, =0xCCCCCCCD
_uart_loop_2:
    CMP   r4, #0
    BEQ   _uart_print_2
    UMULL r0, r1, r4, r9
    LSR   r1, r1, #3
    MOV   r0, #10
    MUL   r2, r1, r0
    SUB   r2, r4, r2
    MOV   r4, r1
    ADD   r2, r2, #0x30
    PUSH  {r2}
    ADD   r6, r6, #1
    B     _uart_loop_2
_uart_print_2:
    CMP   r6, #0
    BEQ   _uart_dot_2
    POP   {r0}
    STR   r0, [r5]
    SUB   r6, r6, #1
    B     _uart_print_2
_uart_dot_2:
    MOV   r0, #0x2E
    STR   r0, [r5]
    VCVT.F64.S32 d1, s4
    VSUB.F64 d1, d3, d1
    MOV   r0, #10
    VMOV  s8, r0
    VCVT.F64.S32 d4, s8
    VMUL.F64 d1, d1, d4
    VCVT.S32.F64 s4, d1
    VMOV  r0, s4
    ADD   r0, r0, #0x30
    STR   r0, [r5]
    MOV   r0, #0x0A
    STR   r0, [r5]
    @ Carregar 9.0
    LDR  r0, =val_6
    VLDR d0, [r0]
    VPUSH {d0}
    @ Carregar 3.0
    LDR  r0, =val_7
    VLDR d0, [r0]
    VPUSH {d0}
    @ OP /
    VPOP  {d1}
    VPOP  {d0}
    VDIV.F64 d2, d0, d1
    VPUSH {d2}
    VPOP  {d0}
    LDR   r1, =result_3
    VSTR  d0, [r1]
    @ Exibir resultado via JTAG UART (1 casa decimal)
    VMOV.F64 d3, d0
    LDR   r5, =0xFF201000
    VCMP.F64 d3, #0
    VMRS  APSR_nzcv, FPSCR
    BGE   _uart_pos_3
    MOV   r0, #0x2D
    STR   r0, [r5]
    VNEG.F64 d3, d3
_uart_pos_3:
    VCVT.S32.F64 s4, d3
    VMOV  r4, s4
    CMP   r4, #0
    BNE   _uart_conv_3
    MOV   r0, #0x30
    STR   r0, [r5]
    B     _uart_dot_3
_uart_conv_3:
    MOV   r6, #0
    LDR   r9, =0xCCCCCCCD
_uart_loop_3:
    CMP   r4, #0
    BEQ   _uart_print_3
    UMULL r0, r1, r4, r9
    LSR   r1, r1, #3
    MOV   r0, #10
    MUL   r2, r1, r0
    SUB   r2, r4, r2
    MOV   r4, r1
    ADD   r2, r2, #0x30
    PUSH  {r2}
    ADD   r6, r6, #1
    B     _uart_loop_3
_uart_print_3:
    CMP   r6, #0
    BEQ   _uart_dot_3
    POP   {r0}
    STR   r0, [r5]
    SUB   r6, r6, #1
    B     _uart_print_3
_uart_dot_3:
    MOV   r0, #0x2E
    STR   r0, [r5]
    VCVT.F64.S32 d1, s4
    VSUB.F64 d1, d3, d1
    MOV   r0, #10
    VMOV  s8, r0
    VCVT.F64.S32 d4, s8
    VMUL.F64 d1, d1, d4
    VCVT.S32.F64 s4, d1
    VMOV  r0, s4
    ADD   r0, r0, #0x30
    STR   r0, [r5]
    MOV   r0, #0x0A
    STR   r0, [r5]
    @ Carregar 10
    LDR  r0, =val_8
    VLDR d0, [r0]
    VPUSH {d0}
    @ Carregar 3
    LDR  r0, =val_9
    VLDR d0, [r0]
    VPUSH {d0}
    @ OP //
    VPOP  {d1}
    VPOP  {d0}
    VDIV.F64 d2, d0, d1
    VCVT.S32.F64 s4, d2
    VCVT.F64.S32 d2, s4
    VPUSH {d2}
    VPOP  {d0}
    LDR   r1, =result_4
    VSTR  d0, [r1]
    @ Exibir resultado via JTAG UART (1 casa decimal)
    VMOV.F64 d3, d0
    LDR   r5, =0xFF201000
    VCMP.F64 d3, #0
    VMRS  APSR_nzcv, FPSCR
    BGE   _uart_pos_4
    MOV   r0, #0x2D
    STR   r0, [r5]
    VNEG.F64 d3, d3
_uart_pos_4:
    VCVT.S32.F64 s4, d3
    VMOV  r4, s4
    CMP   r4, #0
    BNE   _uart_conv_4
    MOV   r0, #0x30
    STR   r0, [r5]
    B     _uart_dot_4
_uart_conv_4:
    MOV   r6, #0
    LDR   r9, =0xCCCCCCCD
_uart_loop_4:
    CMP   r4, #0
    BEQ   _uart_print_4
    UMULL r0, r1, r4, r9
    LSR   r1, r1, #3
    MOV   r0, #10
    MUL   r2, r1, r0
    SUB   r2, r4, r2
    MOV   r4, r1
    ADD   r2, r2, #0x30
    PUSH  {r2}
    ADD   r6, r6, #1
    B     _uart_loop_4
_uart_print_4:
    CMP   r6, #0
    BEQ   _uart_dot_4
    POP   {r0}
    STR   r0, [r5]
    SUB   r6, r6, #1
    B     _uart_print_4
_uart_dot_4:
    MOV   r0, #0x2E
    STR   r0, [r5]
    VCVT.F64.S32 d1, s4
    VSUB.F64 d1, d3, d1
    MOV   r0, #10
    VMOV  s8, r0
    VCVT.F64.S32 d4, s8
    VMUL.F64 d1, d1, d4
    VCVT.S32.F64 s4, d1
    VMOV  r0, s4
    ADD   r0, r0, #0x30
    STR   r0, [r5]
    MOV   r0, #0x0A
    STR   r0, [r5]
    @ Carregar 10
    LDR  r0, =val_10
    VLDR d0, [r0]
    VPUSH {d0}
    @ Carregar 3
    LDR  r0, =val_11
    VLDR d0, [r0]
    VPUSH {d0}
    @ OP %
    VPOP  {d1}
    VPOP  {d0}
    VDIV.F64 d2, d0, d1
    VCVT.S32.F64 s4, d2
    VCVT.F64.S32 d2, s4
    VMUL.F64 d2, d2, d1
    VSUB.F64 d2, d0, d2
    VPUSH {d2}
    VPOP  {d0}
    LDR   r1, =result_5
    VSTR  d0, [r1]
    @ Exibir resultado via JTAG UART (1 casa decimal)
    VMOV.F64 d3, d0
    LDR   r5, =0xFF201000
    VCMP.F64 d3, #0
    VMRS  APSR_nzcv, FPSCR
    BGE   _uart_pos_5
    MOV   r0, #0x2D
    STR   r0, [r5]
    VNEG.F64 d3, d3
_uart_pos_5:
    VCVT.S32.F64 s4, d3
    VMOV  r4, s4
    CMP   r4, #0
    BNE   _uart_conv_5
    MOV   r0, #0x30
    STR   r0, [r5]
    B     _uart_dot_5
_uart_conv_5:
    MOV   r6, #0
    LDR   r9, =0xCCCCCCCD
_uart_loop_5:
    CMP   r4, #0
    BEQ   _uart_print_5
    UMULL r0, r1, r4, r9
    LSR   r1, r1, #3
    MOV   r0, #10
    MUL   r2, r1, r0
    SUB   r2, r4, r2
    MOV   r4, r1
    ADD   r2, r2, #0x30
    PUSH  {r2}
    ADD   r6, r6, #1
    B     _uart_loop_5
_uart_print_5:
    CMP   r6, #0
    BEQ   _uart_dot_5
    POP   {r0}
    STR   r0, [r5]
    SUB   r6, r6, #1
    B     _uart_print_5
_uart_dot_5:
    MOV   r0, #0x2E
    STR   r0, [r5]
    VCVT.F64.S32 d1, s4
    VSUB.F64 d1, d3, d1
    MOV   r0, #10
    VMOV  s8, r0
    VCVT.F64.S32 d4, s8
    VMUL.F64 d1, d1, d4
    VCVT.S32.F64 s4, d1
    VMOV  r0, s4
    ADD   r0, r0, #0x30
    STR   r0, [r5]
    MOV   r0, #0x0A
    STR   r0, [r5]
    @ Carregar 2.0
    LDR  r0, =val_12
    VLDR d0, [r0]
    VPUSH {d0}
    @ Carregar 8
    LDR  r0, =val_13
    VLDR d0, [r0]
    VPUSH {d0}
    @ OP ^
    VPOP  {d1}
    VPOP  {d0}
    VCVT.S32.F64 s2, d1
    VMOV  r0, s2
    VMOV.F64 d2, d0
    SUBS  r0, r0, #1
    BEQ   pow_done_0
pow_loop_0:
    VMUL.F64 d2, d2, d0
    SUBS  r0, r0, #1
    BNE   pow_loop_0
pow_done_0:
    VPUSH {d2}
    VPOP  {d0}
    LDR   r1, =result_6
    VSTR  d0, [r1]
    @ Exibir resultado via JTAG UART (1 casa decimal)
    VMOV.F64 d3, d0
    LDR   r5, =0xFF201000
    VCMP.F64 d3, #0
    VMRS  APSR_nzcv, FPSCR
    BGE   _uart_pos_6
    MOV   r0, #0x2D
    STR   r0, [r5]
    VNEG.F64 d3, d3
_uart_pos_6:
    VCVT.S32.F64 s4, d3
    VMOV  r4, s4
    CMP   r4, #0
    BNE   _uart_conv_6
    MOV   r0, #0x30
    STR   r0, [r5]
    B     _uart_dot_6
_uart_conv_6:
    MOV   r6, #0
    LDR   r9, =0xCCCCCCCD
_uart_loop_6:
    CMP   r4, #0
    BEQ   _uart_print_6
    UMULL r0, r1, r4, r9
    LSR   r1, r1, #3
    MOV   r0, #10
    MUL   r2, r1, r0
    SUB   r2, r4, r2
    MOV   r4, r1
    ADD   r2, r2, #0x30
    PUSH  {r2}
    ADD   r6, r6, #1
    B     _uart_loop_6
_uart_print_6:
    CMP   r6, #0
    BEQ   _uart_dot_6
    POP   {r0}
    STR   r0, [r5]
    SUB   r6, r6, #1
    B     _uart_print_6
_uart_dot_6:
    MOV   r0, #0x2E
    STR   r0, [r5]
    VCVT.F64.S32 d1, s4
    VSUB.F64 d1, d3, d1
    MOV   r0, #10
    VMOV  s8, r0
    VCVT.F64.S32 d4, s8
    VMUL.F64 d1, d1, d4
    VCVT.S32.F64 s4, d1
    VMOV  r0, s4
    ADD   r0, r0, #0x30
    STR   r0, [r5]
    MOV   r0, #0x0A
    STR   r0, [r5]
    @ Carregar 100.0
    LDR  r0, =val_14
    VLDR d0, [r0]
    VPUSH {d0}
    @ Carregar SOMA
    LDR   r1, =var_SOMA
    VLDR  d0, [r1]
    VPUSH {d0}
    LDR   r1, =result_7
    VSTR  d0, [r1]
    @ Exibir resultado via JTAG UART (1 casa decimal)
    VMOV.F64 d3, d0
    LDR   r5, =0xFF201000
    VCMP.F64 d3, #0
    VMRS  APSR_nzcv, FPSCR
    BGE   _uart_pos_7
    MOV   r0, #0x2D
    STR   r0, [r5]
    VNEG.F64 d3, d3
_uart_pos_7:
    VCVT.S32.F64 s4, d3
    VMOV  r4, s4
    CMP   r4, #0
    BNE   _uart_conv_7
    MOV   r0, #0x30
    STR   r0, [r5]
    B     _uart_dot_7
_uart_conv_7:
    MOV   r6, #0
    LDR   r9, =0xCCCCCCCD
_uart_loop_7:
    CMP   r4, #0
    BEQ   _uart_print_7
    UMULL r0, r1, r4, r9
    LSR   r1, r1, #3
    MOV   r0, #10
    MUL   r2, r1, r0
    SUB   r2, r4, r2
    MOV   r4, r1
    ADD   r2, r2, #0x30
    PUSH  {r2}
    ADD   r6, r6, #1
    B     _uart_loop_7
_uart_print_7:
    CMP   r6, #0
    BEQ   _uart_dot_7
    POP   {r0}
    STR   r0, [r5]
    SUB   r6, r6, #1
    B     _uart_print_7
_uart_dot_7:
    MOV   r0, #0x2E
    STR   r0, [r5]
    VCVT.F64.S32 d1, s4
    VSUB.F64 d1, d3, d1
    MOV   r0, #10
    VMOV  s8, r0
    VCVT.F64.S32 d4, s8
    VMUL.F64 d1, d1, d4
    VCVT.S32.F64 s4, d1
    VMOV  r0, s4
    ADD   r0, r0, #0x30
    STR   r0, [r5]
    MOV   r0, #0x0A
    STR   r0, [r5]
    @ Carregar SOMA
    LDR   r1, =var_SOMA
    VLDR  d0, [r1]
    VPUSH {d0}
    VPOP  {d0}
    LDR   r1, =result_8
    VSTR  d0, [r1]
    @ Exibir resultado via JTAG UART (1 casa decimal)
    VMOV.F64 d3, d0
    LDR   r5, =0xFF201000
    VCMP.F64 d3, #0
    VMRS  APSR_nzcv, FPSCR
    BGE   _uart_pos_8
    MOV   r0, #0x2D
    STR   r0, [r5]
    VNEG.F64 d3, d3
_uart_pos_8:
    VCVT.S32.F64 s4, d3
    VMOV  r4, s4
    CMP   r4, #0
    BNE   _uart_conv_8
    MOV   r0, #0x30
    STR   r0, [r5]
    B     _uart_dot_8
_uart_conv_8:
    MOV   r6, #0
    LDR   r9, =0xCCCCCCCD
_uart_loop_8:
    CMP   r4, #0
    BEQ   _uart_print_8
    UMULL r0, r1, r4, r9
    LSR   r1, r1, #3
    MOV   r0, #10
    MUL   r2, r1, r0
    SUB   r2, r4, r2
    MOV   r4, r1
    ADD   r2, r2, #0x30
    PUSH  {r2}
    ADD   r6, r6, #1
    B     _uart_loop_8
_uart_print_8:
    CMP   r6, #0
    BEQ   _uart_dot_8
    POP   {r0}
    STR   r0, [r5]
    SUB   r6, r6, #1
    B     _uart_print_8
_uart_dot_8:
    MOV   r0, #0x2E
    STR   r0, [r5]
    VCVT.F64.S32 d1, s4
    VSUB.F64 d1, d3, d1
    MOV   r0, #10
    VMOV  s8, r0
    VCVT.F64.S32 d4, s8
    VMUL.F64 d1, d1, d4
    VCVT.S32.F64 s4, d1
    VMOV  r0, s4
    ADD   r0, r0, #0x30
    STR   r0, [r5]
    MOV   r0, #0x0A
    STR   r0, [r5]
    @ (1 RES)
    LDR   r1, =result_8
    VLDR  d0, [r1]
    VPUSH {d0}
    VPOP  {d0}
    LDR   r1, =result_9
    VSTR  d0, [r1]
    @ Exibir resultado via JTAG UART (1 casa decimal)
    VMOV.F64 d3, d0
    LDR   r5, =0xFF201000
    VCMP.F64 d3, #0
    VMRS  APSR_nzcv, FPSCR
    BGE   _uart_pos_9
    MOV   r0, #0x2D
    STR   r0, [r5]
    VNEG.F64 d3, d3
_uart_pos_9:
    VCVT.S32.F64 s4, d3
    VMOV  r4, s4
    CMP   r4, #0
    BNE   _uart_conv_9
    MOV   r0, #0x30
    STR   r0, [r5]
    B     _uart_dot_9
_uart_conv_9:
    MOV   r6, #0
    LDR   r9, =0xCCCCCCCD
_uart_loop_9:
    CMP   r4, #0
    BEQ   _uart_print_9
    UMULL r0, r1, r4, r9
    LSR   r1, r1, #3
    MOV   r0, #10
    MUL   r2, r1, r0
    SUB   r2, r4, r2
    MOV   r4, r1
    ADD   r2, r2, #0x30
    PUSH  {r2}
    ADD   r6, r6, #1
    B     _uart_loop_9
_uart_print_9:
    CMP   r6, #0
    BEQ   _uart_dot_9
    POP   {r0}
    STR   r0, [r5]
    SUB   r6, r6, #1
    B     _uart_print_9
_uart_dot_9:
    MOV   r0, #0x2E
    STR   r0, [r5]
    VCVT.F64.S32 d1, s4
    VSUB.F64 d1, d3, d1
    MOV   r0, #10
    VMOV  s8, r0
    VCVT.F64.S32 d4, s8
    VMUL.F64 d1, d1, d4
    VCVT.S32.F64 s4, d1
    VMOV  r0, s4
    ADD   r0, r0, #0x30
    STR   r0, [r5]
    MOV   r0, #0x0A
    STR   r0, [r5]
    @ Carregar 1.5
    LDR  r0, =val_15
    VLDR d0, [r0]
    VPUSH {d0}
    @ Carregar 2.0
    LDR  r0, =val_16
    VLDR d0, [r0]
    VPUSH {d0}
    @ OP *
    VPOP  {d1}
    VPOP  {d0}
    VMUL.F64 d2, d0, d1
    VPUSH {d2}
    @ Carregar 3.0
    LDR  r0, =val_17
    VLDR d0, [r0]
    VPUSH {d0}
    @ Carregar 4.0
    LDR  r0, =val_18
    VLDR d0, [r0]
    VPUSH {d0}
    @ OP *
    VPOP  {d1}
    VPOP  {d0}
    VMUL.F64 d2, d0, d1
    VPUSH {d2}
    @ OP /
    VPOP  {d1}
    VPOP  {d0}
    VDIV.F64 d2, d0, d1
    VPUSH {d2}
    VPOP  {d0}
    LDR   r1, =result_10
    VSTR  d0, [r1]
    @ Exibir resultado via JTAG UART (1 casa decimal)
    VMOV.F64 d3, d0
    LDR   r5, =0xFF201000
    VCMP.F64 d3, #0
    VMRS  APSR_nzcv, FPSCR
    BGE   _uart_pos_10
    MOV   r0, #0x2D
    STR   r0, [r5]
    VNEG.F64 d3, d3
_uart_pos_10:
    VCVT.S32.F64 s4, d3
    VMOV  r4, s4
    CMP   r4, #0
    BNE   _uart_conv_10
    MOV   r0, #0x30
    STR   r0, [r5]
    B     _uart_dot_10
_uart_conv_10:
    MOV   r6, #0
    LDR   r9, =0xCCCCCCCD
_uart_loop_10:
    CMP   r4, #0
    BEQ   _uart_print_10
    UMULL r0, r1, r4, r9
    LSR   r1, r1, #3
    MOV   r0, #10
    MUL   r2, r1, r0
    SUB   r2, r4, r2
    MOV   r4, r1
    ADD   r2, r2, #0x30
    PUSH  {r2}
    ADD   r6, r6, #1
    B     _uart_loop_10
_uart_print_10:
    CMP   r6, #0
    BEQ   _uart_dot_10
    POP   {r0}
    STR   r0, [r5]
    SUB   r6, r6, #1
    B     _uart_print_10
_uart_dot_10:
    MOV   r0, #0x2E
    STR   r0, [r5]
    VCVT.F64.S32 d1, s4
    VSUB.F64 d1, d3, d1
    MOV   r0, #10
    VMOV  s8, r0
    VCVT.F64.S32 d4, s8
    VMUL.F64 d1, d1, d4
    VCVT.S32.F64 s4, d1
    VMOV  r0, s4
    ADD   r0, r0, #0x30
    STR   r0, [r5]
    MOV   r0, #0x0A
    STR   r0, [r5]
    @ Carregar 3.0
    LDR  r0, =val_19
    VLDR d0, [r0]
    VPUSH {d0}
    @ Carregar 4.0
    LDR  r0, =val_20
    VLDR d0, [r0]
    VPUSH {d0}
    @ OP +
    VPOP  {d1}
    VPOP  {d0}
    VADD.F64 d2, d0, d1
    VPUSH {d2}
    @ Carregar 2.0
    LDR  r0, =val_21
    VLDR d0, [r0]
    VPUSH {d0}
    @ Carregar 5.0
    LDR  r0, =val_22
    VLDR d0, [r0]
    VPUSH {d0}
    @ OP *
    VPOP  {d1}
    VPOP  {d0}
    VMUL.F64 d2, d0, d1
    VPUSH {d2}
    @ OP -
    VPOP  {d1}
    VPOP  {d0}
    VSUB.F64 d2, d0, d1
    VPUSH {d2}
    VPOP  {d0}
    LDR   r1, =result_11
    VSTR  d0, [r1]
    @ Exibir resultado via JTAG UART (1 casa decimal)
    VMOV.F64 d3, d0
    LDR   r5, =0xFF201000
    VCMP.F64 d3, #0
    VMRS  APSR_nzcv, FPSCR
    BGE   _uart_pos_11
    MOV   r0, #0x2D
    STR   r0, [r5]
    VNEG.F64 d3, d3
_uart_pos_11:
    VCVT.S32.F64 s4, d3
    VMOV  r4, s4
    CMP   r4, #0
    BNE   _uart_conv_11
    MOV   r0, #0x30
    STR   r0, [r5]
    B     _uart_dot_11
_uart_conv_11:
    MOV   r6, #0
    LDR   r9, =0xCCCCCCCD
_uart_loop_11:
    CMP   r4, #0
    BEQ   _uart_print_11
    UMULL r0, r1, r4, r9
    LSR   r1, r1, #3
    MOV   r0, #10
    MUL   r2, r1, r0
    SUB   r2, r4, r2
    MOV   r4, r1
    ADD   r2, r2, #0x30
    PUSH  {r2}
    ADD   r6, r6, #1
    B     _uart_loop_11
_uart_print_11:
    CMP   r6, #0
    BEQ   _uart_dot_11
    POP   {r0}
    STR   r0, [r5]
    SUB   r6, r6, #1
    B     _uart_print_11
_uart_dot_11:
    MOV   r0, #0x2E
    STR   r0, [r5]
    VCVT.F64.S32 d1, s4
    VSUB.F64 d1, d3, d1
    MOV   r0, #10
    VMOV  s8, r0
    VCVT.F64.S32 d4, s8
    VMUL.F64 d1, d1, d4
    VCVT.S32.F64 s4, d1
    VMOV  r0, s4
    ADD   r0, r0, #0x30
    STR   r0, [r5]
    MOV   r0, #0x0A
    STR   r0, [r5]

_end:
    B _end