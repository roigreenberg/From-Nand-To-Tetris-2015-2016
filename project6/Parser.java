/**
 * Created by inbaravni on 3/29/16.
 */


import java.nio.*;
import java.nio.file.*;
import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class Parser {

    private File inputFile;
    private BufferedReader bufReader;
    private boolean toAdvance = true;
    private String currentLine = "";
    private String nextLine = "";
    private Boolean MoreCommands;
    public enum Command {A_COMMAND, C_COMMAND, L_COMMAND};
    private Pattern cCommandPattern = Pattern.compile("(([^=/]*)=)?([^/=;]*)(;([^/=;]*))?(//.*)?");
    private Matcher matcher;

    // Constructor
    // opens the input file/stream and gets ready to parse it.
    Parser(File inputFile) {

        try {
            this.inputFile = inputFile;
            FileReader fileReader = new FileReader(inputFile.getAbsolutePath());
            this.bufReader = new BufferedReader(fileReader);
            if (this.bufReader == null)
            {
                System.out.println("No file");
            }
        } catch (IOException ioexc) {
            //throw new IOException("Problem reading the file");
        }
    }


    // are there more commands in the input?
    Boolean hasMoreCommands() {

        if (toAdvance) {
            toAdvance = false;
            try {
                while ((nextLine = this.bufReader.readLine()).trim().isEmpty() || nextLine.trim().charAt(0) == '/') {
                }
                if (nextLine != null) {
                    this.MoreCommands = true;
                    return true;
                }

                this.MoreCommands = false;
                return false;

            } catch  (Exception e) {
                this.MoreCommands = false;
                return false;
            }
        } else {
            return this.MoreCommands;
        }
    }

    // the next command from the input and makes it the current
    // command. Should be called only if hasMoreCommands() is true.
    void advance() {

        if (this.hasMoreCommands()) {
            currentLine = nextLine.replaceAll("\\s", "");
        }
        toAdvance = true;
    }

    // Returns the type of the current command
    Command commandType() {

        switch (currentLine.charAt(0)) {
            // A_COMMAND
            case '@':
                return Command.A_COMMAND;

            // L_COMMAND
            case '(':
                return Command.L_COMMAND;

            // C_COMMAND
            default:
                return Command.C_COMMAND;
        }
    }

    // Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx).
    String symbol() {


        switch (commandType()) {

            case A_COMMAND:
                return currentLine.split("@")[1];

            case L_COMMAND:
                return currentLine.split("[\\(\\)]")[1];

            default:
                return null;
        }
    }


    // Returns the dest mnemonic in the current C-command
    String dest() {

        matcher = cCommandPattern.matcher(currentLine);
        matcher.find();
        return matcher.group(2);
    }


    // Returns the comp mnemonic in the current C-command
    String comp() {

        matcher = cCommandPattern.matcher(currentLine);
        matcher.find();
        return matcher.group(3);
    }

    // Returns the jump mnemonic in the current C-command
    String jump() {

        matcher = cCommandPattern.matcher(currentLine);
        matcher.find();
        return matcher.group(5);
    }

}
