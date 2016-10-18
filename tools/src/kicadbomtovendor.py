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
import argparse
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
    #   Get command line arguments
    parser = argparse.ArgumentParser(description="KiCAD XML bill of materials converter to .CSV format")
    parser.add_argument("--verbose", default=False, action="store_true", help="set verbose mode")
    parser.add_argument("--select", action="append", help="COLUMN=VALUE to select")
    parser.add_argument("files", action="append", help="XML file")
    args = parser.parse_args()                          # parse command line
    print(args)
    verbose = args.verbose
    selects = {}                                        # dict of (k, set(v))
    #   Accumulate select keys
    print("Selects: " + repr(args.select))
    if args.select is not None :
        for select in args.select :
            parts = select.split("=")                       # split at "="
            if len(parts) != 2 :                            # must be COLUMN=VALUE
                print('"--select COLUMN=VALUE" required.')
                parser.print_help()
                exit(1)
            k = parts[0].strip().upper()
            v = parts[1].strip().upper()                    # save selects as upper case
            if k not in selects :
                selects[k] = set()                          # need set for this key
            selects[k].add(v)                               # add value to set for this key
        print("Selection rules: ")
        for (k, sset) in selects.items() :
            print('  Select if %s is in %s.' % (k, list(sset)))
    #   Process all files on command line
    for infname in args.files :
        print(infname)
        try : 
            (outfname, suffix) = infname.rsplit(".",1)  # remove suffix
        except ValueError :
            print("Input must be a .xml file.")
            parser.print_help()
            exit(1)
        if suffix.lower() != "xml" :                    # must be XML
            print("Input must be a .xml file.")
            parser.print_help()
            exit(1)
        outfname = outfname + "." + "csv"               # output becomes comma separated
        print('Converting "%s" to "%s".' % (infname, outfname))
        cv = Converter(selects, verbose)
        cv.convert(infname, outfname)
        print('Output file "%s" generated.' % (outfname,))
 
#
#   converter -- converts file
#    
class Converter(object) :
    FIXEDFIELDS = ["REF","FOOTPRINT","VALUE"]           # fields we always want

    def __init__(self, selects, verbose = False) :
        self.selects = selects                          # selection list
        self.verbose = verbose                          # debug info
        self.tree = None                                # no tree yet
        self.fieldset = set(self.FIXEDFIELDS)           # set of all field names found
        self.fieldlist = None                           # list of column headings
        
    def cleanstr(self, s) :
        """
        Clean up a string to avoid CSV format problems
        """
        return(re.sub(r'\s+|,',' ', s).strip()) # remove tabs, newlines, and commas
                
    def handlecomp1(self, comp) :
        """
        Handle one component entry, pass 1 - find all field names
        """
        for field in comp.iter("field") :               # for all "field" items
            name = field.get("name")                    # get all "name" names
            name = name.upper()
            self.fieldset.add(name)
            
    def selectitem(self, fieldvals) :
        """
        Given a set of field values, decide if we want to keep this one
        """
        for k in self.selects :                         # for all select rules
            if k not in fieldvals :                     # if not found, fail, unless missing allowed
                return("" in self.selects[k])           # if "--select FOO=" allow
            if fieldvals[k] in self.selects[k] :        # if find
                return(True)
        return(True)                                    # no select failed            
            
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
        if self.selectitem(fieldvals) :
            s = self.formatline(fieldvals)
            return(s)
        return("")
            
    def formatline(self, fieldvals) :
        """
        Assemble output line
        """
        s = ''                              # empty line
        outfields = []                      # output fields
        for fname in self.fieldlist :       # for all fields
            if fname in fieldvals :
                val = fieldvals[fname]      # get value
            else :
                val = ""                    # empty string otherwise
            outfields.append(self.cleanstr(val))     # remove things not desirable in CSV files
        return(",".join(outfields))
                  
    def convert(self, infname, outfname) :
        """
        Convert one file
        """
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

