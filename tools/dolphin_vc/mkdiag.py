root = '/root/ootmm/packages/generator/src/'

def edit(path, pairs):
    s = open(root + path).read()
    for a, b in pairs:
        assert a in s, (path, a)
        s = s.replace(a, b, 1)
    open(root + path, 'w').write(s)

edit('common/switch.c', [
 ('#include <combo/context.h>\n', '''#include <combo/context.h>

#define DIAG_MARK(n) (*(volatile u32*)0xa00003f0 = 0x44494147, *(volatile u32*)0xa00003f4 = (n))

void Diag_Mark(u32 n)
{
    DIAG_MARK(n);
}
'''),
 ('    gComboCtx.entrance = entrance;', '    DIAG_MARK(1);\n    gComboCtx.entrance = entrance;'),
 ('    System_DisableInterrupts();\n    waitSubsystems();\n', '    DIAG_MARK(2);\n    System_DisableInterrupts();\n    waitSubsystems();\n    DIAG_MARK(3);\n'),
 ('NORETURN void comboGameSwitch3(void)\n{\n', 'NORETURN void comboGameSwitch3(void)\n{\n    DIAG_MARK(4);\n'),
 ('    resetSchedulerBlock();\n', '    resetSchedulerBlock();\n    DIAG_MARK(6);\n'),
])
edit('oot/play/play.c', [
 ('void Play_MainWrapper(PlayState* play)\n{\n', '''void Play_MainWrapper(PlayState* play)
{
    static u32 sDiagFrames;
    void Diag_Mark(u32);

    Diag_Mark(0x100 + (sDiagFrames & 0xff));
    if (++sDiagFrames == 400)
        comboGameSwitch(NULL, ENTR_MM_CLOCK_TOWN_FROM_CLOCK_TOWER);

'''),
])
edit('mm/play/play.c', [
 ('void Play_MainWrapper(PlayState* play)\n{\n    Player* link;\n', '''void Play_MainWrapper(PlayState* play)
{
    Player* link;
    static u32 sDiagFrames;
    void Diag_Mark(u32);

    Diag_Mark(0x200 + (sDiagFrames & 0xff));
    if (++sDiagFrames == 300)
        comboGameSwitch(NULL, ENTR_OOT_WARP_SONG_TEMPLE);
'''),
])
#edit('mm/scene.c', [('void Object_AfterInitContext(void)\n', '__attribute__((optimize("no-optimize-sibling-calls", "no-delayed-branch")))\nvoid Object_AfterInitContext(void)\n')])

import os
if os.environ.get('DIAG_FLAGS', '1') == '1':
    p = '/root/ootmm/packages/generator/CMakeLists.txt'
    s = open(p).read()
    s = s.replace('set(CMAKE_C_FLAGS "${FLAGS} -D_LANGUAGE_C=1")', 'set(CMAKE_C_FLAGS "${FLAGS} -fno-optimize-sibling-calls -D_LANGUAGE_C=1")', 1)
    open(p, 'w').write(s)
