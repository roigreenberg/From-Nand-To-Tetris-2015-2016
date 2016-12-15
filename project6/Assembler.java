import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.regex.*;

public class Assembler {
    public static void findSymbols(File input, SymbolTable st)
    {
        Parser p = new Parser(input);
        String s = new String();
        int index = 0;
        while (p.hasMoreCommands())
        {
            p.advance();
            switch (p.commandType()){
                case A_COMMAND:
                    index++;
                    break;
                case C_COMMAND:
                    index++;
                    break;

                case L_COMMAND:
                    s = p.symbol();
                    st.addEntry(s, index);
                    break;
            }


        }
    }
    public static void asmToHack(File input, SymbolTable st)
    {
        Parser p = new Parser(input);
        String fileName = input.getPath().split("\\.")[0];
        Code b = new Code();

        String s = new String();
        char[] c = new char[16];
        int varIndex = 16;
        File outputFile = new File(fileName+".hack");
        if (!outputFile.exists()) {
            try {
                outputFile.createNewFile();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        FileWriter fw = null;
        try {
            fw = new FileWriter(outputFile.getAbsoluteFile());
        } catch (IOException e) {
            e.printStackTrace();
        }
        BufferedWriter bw = new BufferedWriter(fw);

        while (p.hasMoreCommands())
        {
            p.advance();
            Arrays.fill(c, '0');
            switch (p.commandType()){
                case A_COMMAND:
                    s = p.symbol();
                    if (isInteger(s))
                    {
                        s = Integer.toBinaryString(Integer.parseInt(s));
                        fillChar(c, s, 16 - s.length());
                    } else {
                        if (!st.contains(s))
                        {
                            st.addEntry(s, varIndex++);
                        }
                        s = Integer.toBinaryString(st.getAddress(s));
                        fillChar(c, s, 16 - s.length());                    }
                    break;
                case L_COMMAND:
                    continue;

                case C_COMMAND:
                    s = b.jump(p.jump());
                    fillChar(c, s, 13);
                    s = b.dest(p.dest());
                    fillChar(c, s, 10);
                    s = b.comp(p.comp());
                    fillChar(c, s, 1);
                    c[0] = '1';
            }
            try {
                bw.write(c);
                bw.newLine();
            } catch (IOException e) {
                e.printStackTrace();
            }

        }
        try {
            bw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public static boolean isInteger(String s) {
        boolean isValidInteger = false;
        try
        {
            Integer.parseInt(s);

            // s is a valid integer

            isValidInteger = true;
        }
        catch (NumberFormatException ex)
        {
            // s is not an integer
        }

        return isValidInteger;
    }

    public static void fillChar(char[] dst, String src, int startIndex)
    {
        for (int i = 0; i < src.length() && i < 16; i++)
        {
            dst[startIndex + i] = src.charAt(i);
        }
    }

    public static void main(String[] args) {

        File input = new File(args[0]);
        if (input.isFile())
        {

            if (input.getPath().split("\\.")[1].equals("asm"))
            {
                SymbolTable st = new SymbolTable();
                findSymbols(input, st);
                asmToHack(input, st);
            }

        }
        else if(input.isDirectory())
        {
            for (File file : input.listFiles())
            {
                if (file.getPath().split("\\.")[1].equals("asm"))
                {
                    SymbolTable st = new SymbolTable();
                    findSymbols(file, st);
                    asmToHack(file, st);

                }
            }
        }
    }
}
