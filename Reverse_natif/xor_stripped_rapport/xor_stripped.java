import ghidra.app.script.GhidraScript;

public class xor_stripped extends GhidraScript {
    @Override
    public void run() throws Exception {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 15; i++) {
            int b = getByte(toAddr(0x00102038 + i));
            sb.append((char) ((b ^ (0x5a + i)) & 0xff));
        }
        println(sb.toString());
    }
}
