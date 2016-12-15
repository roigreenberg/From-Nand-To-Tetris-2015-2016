import java.util.HashMap;
import java.util.Map;

/**
 * Created by roigreenberg on 3/29/16.
 */
public class SymbolTable {
    private Map<String, Integer> symbolTable = new HashMap<String, Integer>();

    SymbolTable()
    {
        symbolTable.put("SP", 0);
        symbolTable.put("LCL", 1);
        symbolTable.put("ARG", 2);
        symbolTable.put("THIS", 3);
        symbolTable.put("THAT", 4);
        symbolTable.put("SCREEN", 16384);
        symbolTable.put("KBD", 24576);
        for (int i = 0; i < 16; i++)
        {
            symbolTable.put("R"+ i, i);

        }
    }
    void addEntry(String symbol, int address)
    {
        symbolTable.put(symbol, address);
    }

    boolean contains(String symbol)
    {
        return symbolTable.containsKey(symbol);
    }

    int getAddress(String symbol)
    {
        return symbolTable.get(symbol);
    }

}
