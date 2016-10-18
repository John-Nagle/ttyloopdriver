#
#   KiCAD BOM to DigiKey BOM conversion
#
#   John Nagle
#   October, 2016
#   License: GPL
#
#   Output is a tab-delimited file.
#
#   
#
import re
import sys
import xml.etree.ElementTree
#
#   usage
#
def usage(msg) :
    print("Error: %s\n" % (msg,))
    print("Usage: python3 kicadbomtodigikey.py [options] FILENAME.xml")
    print("Output will go into FILENAME.tabs")
    sys.exit(1)
#
#   Main program
#
def main() :
    if len(sys.argv) < 2 :                      # no args
        usage("File argument missing,")
    infname = sys.argv[1]                       # input file
    try : 
        (outfname, suffix) = infname.rsplit(".",1)  # remove suffix
    except ValueError :
        usage("Filename did not have a suffix.")
    if suffix.lower() != "xml" :                # must be XML
        usage("Input must be a .xml file.")
    outfname = outfname + "." + "csv"          # output becomes comma separated
    print('Converting "%s" to "%s".' % (infname, outfname))
    cv = Converter(True)
    cv.convert(infname, outfname)
    print("Output file generated.")
 
#
#   converter -- converts file
#    
class Converter(object) :
    FIXEDFIELDS = ["REF","FOOTPRINT","VALUE"]   # fields we always want

    def __init__(self, verbose = False) :
        self.verbose = verbose                  # debug info
        self.tree = None                        # no tree yet
        self.fieldset = set(self.FIXEDFIELDS)   # set of all field names found
        self.fieldlist = None                   # list of column headings
        pass
        
    def handlecomp1(self, comp) :
        """
        Handle one component entry, pass 1 - find all field names
        """
        for field in comp.iter("field") :       # for all "field" items
            name = field.get("name")            # get all "name" names
            name = name.upper()
            self.fieldset.add(name)
            
    def handlecomp2(self, comp) :
        """
        Handle one component entry, pass 2 - Collect and output fields
        """
        fieldvals = dict()
        try :
            ref = comp.attrib.get("ref")
            footprint = comp.find("footprint").text
            value = comp.find("value").text
        except ValueError as message :
            usage("Required field missing from %s" % (comp.attrib))
        fieldvals["REF"] = ref
        fieldvals["FOOTPRINT"] = footprint
        fieldvals["VALUE"] = value
        if self.verbose :
            print("%s" % (fieldvals,))
        #   Get user-defined fields    
        for field in comp.iter("field") :
            name = field.get("name")
            name = name.upper()
            fieldvals[name] = field.text
        if self.verbose :
            print("%s" % (fieldvals,))
        s = self.formatline(fieldvals)
        return(s)
            
    def formatline(self, fieldvals) :
        """
        Assemble output line
        """
        s = ''                              # empty line
        first = True                        # first time
        for fname in self.fieldlist :       # for all fields
            if fname in fieldvals :
                val = fieldvals[fname]      # get value
            else :
                val = ""                    # empty string otherwise
            val = re.sub(r',',' ',val)      # remove commas
            val = re.sub(r'\s+',' ', val)   # remove tabs or newlines
            val = val.strip()               # remove excess whitespace
            if not first :                  # if s is not empty
                s += ","                    # add comma
            first = False
            s += val                        # add value
        return(s)
                  
    def convert(self, infname, outfname) :
        self.tree = xml.etree.ElementTree.parse(infname)
        root = self.tree.getroot()              # root element
        #   Pass 1 - inventory fields
        for comp in root.iter("comp") :
            self.handlecomp1(comp)
        if self.verbose :
            print("Field names found: %s" % (self.fieldset))
        self.fieldlist = list(self.fieldset)
        self.fieldlist.sort()                   # sort in place
        #   Worked, OK to output file
        heading = ",".join(self.fieldlist)     # heading line
        outf = open(outfname,"w")               # open output file
        if self.verbose :
            print("Column headings: %s" % (self.fieldlist))
        outf.write(heading + "\n")
        #   Pass 2 - output columns
        for comp in root.iter("comp") : 
            s = self.handlecomp2(comp)
            outf.write(s + "\n")                # print to file
        outf.close()                            # done
            

if __name__ == "__main__" :
    main()    

