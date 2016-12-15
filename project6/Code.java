import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by inbaravni on 3/29/16.
 */
public class Code {

    private Pattern destPattern = Pattern.compile("(A)?(M)?(D)?");
    private Matcher codeMatcher;
    private char[] destBit = new char[3];
    private Map<String, String> compMap = new HashMap<String, String>();
    private Map<String, String> jumpMap = new HashMap<String, String>();

    Code(){
        // init the jumpMap
        jumpMap.put(null, "000");
        jumpMap.put("JGT", "001");
        jumpMap.put("JEQ", "010");
        jumpMap.put("JGE", "011");
        jumpMap.put("JLT", "100");
        jumpMap.put("JNE", "101");
        jumpMap.put("JLE", "110");
        jumpMap.put("JMP", "111");

        // init the compMap
        compMap.put("0", "110101010");
        compMap.put("1", "110111111");
        compMap.put("-1", "110111010");
        compMap.put("D", "110001100");
        compMap.put("A", "110110000");
        compMap.put("!D", "110001101");
        compMap.put("!A", "110110001");
        compMap.put("-D", "110001111");
        compMap.put("-A", "110110011");
        compMap.put("D+1", "110011111");
        compMap.put("A+1", "110110111");
        compMap.put("D-1", "110001110");
        compMap.put("A-1", "110110010");
        compMap.put("D+A", "110000010");
        compMap.put("D-A", "110010011");
        compMap.put("A-D", "110000111");
        compMap.put("D&A", "110000000");
        compMap.put("D|A", "110010101");
        compMap.put("M", "111110000");
        compMap.put("!M", "111110001");
        compMap.put("-M", "111110011");
        compMap.put("M+1", "111110111");
        compMap.put("M-1", "111110010");
        compMap.put("D+M", "111000010");
        compMap.put("D-M", "111010011");
        compMap.put("M-D", "111000111");
        compMap.put("D&M", "111000000");
        compMap.put("D|M", "111010101");
        compMap.put("D<<", "010110000");
        compMap.put("D>>", "010010000");
        compMap.put("A<<", "010100000");
        compMap.put("A>>", "010000000");
        compMap.put("M<<", "011100000");
        compMap.put("M>>", "011000000");

    }

    // Returns the binary code of the dest mnemonic.
    String dest(String mnemonic) {
        Arrays.fill(destBit, '0');
        if (mnemonic == null)
            return new String(destBit);
        codeMatcher = destPattern.matcher(mnemonic);
        codeMatcher.find();


            if (codeMatcher.group(1) != null)
                destBit[0] = '1';
            if (codeMatcher.group(2) != null)
                destBit[2] = '1';
            if (codeMatcher.group(3) != null)
                destBit[1] = '1';

        return new String(destBit);
    }


    // Returns the binary code of the jump mnemonic.
    String jump(String mnemonic) {

        return jumpMap.get(mnemonic);
    }

    // Returns the binary code of the comp mnemonic.
    String comp(String mnemonic) {

        return compMap.get(mnemonic);
    }
}
