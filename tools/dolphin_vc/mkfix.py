import shutil
root = '/root/ootmm/packages/generator/src/'

def edit(path, pairs):
    s = open(root + path).read()
    for a, b in pairs:
        assert a in s, (path, a)
        s = s.replace(a, b, 1)
    open(root + path, 'w').write(s)

edit('common/switch.c', [
 ('#if defined(GAME_OOT)\n# define FOREIGN_OFF    0x80000\n', '#if defined(GAME_OOT)\n# define FOREIGN_OFF    0x80000\n# define FOREIGN_THREAD_TAIL 0x80097e10\n'),
 ('#else\n# define FOREIGN_OFF    0x400\n', '#else\n# define FOREIGN_OFF    0x400\n# define FOREIGN_THREAD_TAIL 0x80006330\n'),
 ('if ((tmp & 2) && (tmp & 1) && !', 'if ((tmp & 1) && !'),
 ('NORETURN void comboGameSwitch2(void);', '''/*
 * Wii Virtual Console reads the addresses of libultra's scheduler variables from OoT's exception
 * handler once, then uses them for every exception. Both games keep these variables in one block
 * (vc_libultra.S), which is reset here for the next game, with its own thread queue tail.
 */
static void resetSchedulerBlock(void)
{
    volatile u32* block = (volatile u32*)0x80000200;

    block[0] = FOREIGN_THREAD_TAIL; /* __osRunQueue */
    block[1] = FOREIGN_THREAD_TAIL; /* __osActiveQueue */
    block[2] = 0;                   /* __osRunningThread */
    block[3] = 0;                   /* __osFaultedThread */
    block[4] = 0x003fff01;          /* __OSGlobalIntMask */
#pragma GCC unroll 32
    for (int i = 0; i < 32; ++i)
        block[8 + i] = 0;           /* __osEventStateTab */
}

/*
 * Virtual Console also replaces five libultra thread functions with calls into the emulator, but only in
 * OoT's RAM, the first time. The next game's copies are loaded unchanged from the ROM, so copy the
 * replacement words to them. Other emulators and the console leave send_mesg as MIPS code.
 */
typedef struct
{
    u32 oot;
    u32 mm;
    u32 count;
}
VcPatch;

static const VcPatch kVcPatches[] = {
    { 0x80002964, 0x8008905c, 3 }, /* send_mesg */
    { 0x80002a58, 0x80089150, 1 }, /* __osEnqueueAndYield */
    { 0x80002b4c, 0x80089244, 3 }, /* __osEnqueueThread */
    { 0x80002b94, 0x8008928c, 3 }, /* __osPopThread */
    { 0x80002ba4, 0x800892a4, 1 }, /* __osDispatchThread */
};

static void copyVcPatches(void)
{
    const VcPatch* p;
    const volatile u32* src;
    volatile u32* dst;

    for (u32 i = 0; i < ARRAY_COUNT(kVcPatches); ++i)
    {
        p = &kVcPatches[i];
#if defined(GAME_OOT)
        src = (const volatile u32*)(p->oot | 0xa0000000);
        dst = (volatile u32*)(p->mm | 0xa0000000);
#else
        src = (const volatile u32*)(p->mm | 0xa0000000);
        dst = (volatile u32*)(p->oot | 0xa0000000);
#endif
        /* VC library call opcode (0x7c000000 | function index) */
        if ((src[0] & 0xffffff00) != 0x7c000000)
            return;
        for (u32 j = 0; j < p->count; ++j)
            dst[j] = src[j];
    }
}

NORETURN void comboGameSwitch2(void);'''),
 ('    IO_WRITE(PI_STATUS_REG, PI_STATUS_RESET | PI_STATUS_CLR_INTR);\n', '''    IO_WRITE(PI_STATUS_REG, PI_STATUS_RESET | PI_STATUS_CLR_INTR);

    /*
     * The next game decompresses its code over code this game ran. Virtual Console replaces
     * osInvalICache with a call that drops its translated code for the range, but only on one
     * side of its function tree's root, so invalidate in small pieces. This code runs from KSEG1,
     * which that call leaves alone.
     */
    for (u32 addr = 0x80000000; addr < 0x80800000; addr += 0x2000)
        osInvalICache((void*)addr, 0x2000);
'''),
 ('    Context_Export();\n', '    Context_Export();\n    copyVcPatches();\n    resetSchedulerBlock();\n'),
 ('NORETURN void comboGameSwitch2(void);', 'void osInvalICache(void* addr, s32 size);\nNORETURN void comboGameSwitch2(void);'),
])
edit('common/switch.S', [('la sp,0xa0800000', 'la sp,0x80800000')])

boot_oot = '''
/* Main_ClearMemory: also set up the shared scheduler block before the first thread is created */
PATCH_START 0x80000460
  lui t6,0x8000
  addiu t7,t6,0x6330
  sw t7,0x200(t6)
  sw t7,0x204(t6)
  lui t7,0x3f
  ori t7,t7,0xff01
  sw t7,0x210(t6)
  lw t6,0x318(t6)
  lui t7,1
  addiu t7,t7,-0x4ec0
  subu a1,t6,t7
  lui a0,0x8001
  j 0x80002e80
   addiu a0,a0,-0x4ec0
PATCH_END
'''
s = open('/mnt/c/t/vc/vc_libultra_oot.S').read() + boot_oot
open(root + 'oot/vc_libultra.S', 'w').write(s)
shutil.copy('/mnt/c/t/vc/vc_libultra_mm.S', root + 'mm/vc_libultra.S')
