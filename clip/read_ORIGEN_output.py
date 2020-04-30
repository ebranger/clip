import re
import math

def read_ORIGEN_gamma_spectrum(output_filename, cooling_time_string):
    """
    Function for reading a gamma spectrum from an ORIGEN output file.
    """
    
    #Too long text may cause problems, so check for it.
    if len(cooling_time_string) >= 10:
        print("The cooling time could not be found in the input, the header text \"" + cooling_time_string + "\" is too long.")
        return 0,0
    
    found_spectrum = False
    bin_count = [0]
    bin_edges = [0]
    
    f = open(output_filename, 'r')
    ORIGEN = f.read()
    
    if len(ORIGEN) < 1:
        #Did not read anything, or read an empty file. Return empty arrays
        print("Failed to open ORIGEN output file " + output_filename)
        return bin_edges, bin_count
    
    #get the gamma spectra form the output
    #The header we are looking for starts with this string, and ends with a total row, the data we want is in between.
    spectrumpattern = re.compile("gamma spectra, photons\/sec\/basis(.*?)\s*totals", re.DOTALL)
    
    if re.search(spectrumpattern, ORIGEN):
        spectrum_list = re.findall(spectrumpattern, ORIGEN)
    else:
        #Failed to find any gamma spectrum, return empty arrays
        print("Failed to find a gamma spectrum in ORIGEN output file " + output_filename)
        return bin_edges, bin_count

    for spectrum in spectrum_list:
        spectrum_textlines = spectrum.splitlines()
        
        #Get the spectrum table header, search for cooling_time_string in the header
        headers = spectrum_textlines[3]
        
        #after removing the 23 first characters, each column header should start with a space, followed
        #by possibly more spaces for right-alignmnet, and then the cooling time string.
        #Each such header is 10 characters long. 
        header_columns = headers[23:]
        
        #Column headers are padded with spaces at the beginning to be 10 characters wide.
        header_string =  cooling_time_string.strip()
        while len(header_string ) < 10:
            header_string = ' ' + header_string
        
        if header_columns.find(header_string) != -1:
            column = math.ceil(header_columns.find(header_string)/10)
            found_spectrum = True
            
            #allocate memory
            bin_count = [0] * (len(spectrum_textlines)-4)
            bin_edges = [0] * (len(spectrum_textlines)-3)
            
            #Table should start at row 4.
            for i in range(4,len(spectrum_textlines)):
                #read the gamma spectrum
                line = spectrum_textlines[i].strip()
                split_line = line.split(" ")

                #The split lines should have the following format:
                # <line number> <low bin edge> <hyphen> <high bin edge> 
                #<first cooling time bin count> <second cooling time bin count> <third...>
                bin_count[i-4] = float(split_line[column + 3]) 
                bin_edges[i-4] = float(split_line[1])
                
            #Final upper bin edge.
            bin_edges[len(spectrum_textlines)-4] = float(split_line[3])
    
    if found_spectrum == False:
        #Did not find the requested spectra in the file, return empty arrays.
        print("Unable to find a gamma spectrum with cooling time " + cooling_time_string + 
              " in ORIGEN output file " + output_filename)

        bin_count = [0]
        bin_edges = [0]
        return bin_edges, bin_count
    else:
        #Found the requested gamma spectrum, return it. 
        #If several are found, this will return the last one, which is typically the one of interest. 
        return bin_edges, bin_count

def read_ORIGEN_isotope_contents(output_filename, cooling_time_string, isotope_list):
    """
    Read the isotope contents from an ORIGEN output file. 
    If multiple cooling times with the given string exists, return the last 
    printed value. This is typically the only case consedered which is cooling after discharge.
    """
    
    #Too long text may cause problems, so check for it.
    if len(cooling_time_string) >= 10:
        print("The cooling time could not be found in the input, the header text \"" + cooling_time_string + "\" is too long.")
        return [0] * len(isotope_list)
    
    isotope_contents = [0] * len(isotope_list)
    
    f = open(output_filename, 'r')
    ORIGEN = f.read()
    
    if len(ORIGEN) < 1:
        #Did not read anything, or read an empty file. Return empty arrays
        print("Failed to open ORIGEN output file " + output_filename)
        return [0] * len(isotope_list)
    
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    isotope_searchlist = [''] * (len(isotope_list))

    #Get a searchable string, the ORIGEN output has spaces between the isotopes and the number of nucleons
    #if the number of nucleons has fewer than three digits
    for i in range(0,len(isotope_list)):
        m = r.match(isotope_list[i])
        if len(m.group(2)) == 1:
            isotope_searchlist[i] = (m.group(1)).lower() + "  " + m.group(2)
        elif len(m.group(2)) == 2:
            isotope_searchlist[i] = (m.group(1)).lower() + " " + m.group(2)
        else:
            isotope_searchlist[i] = (isotope_list[i]).lower()

    line = 0
    
    ORIGEN_lines = ORIGEN.splitlines()
    
    reading_a_table = False
    header = ""
    column = 0
    
    while line < len(ORIGEN_lines):
        
        #Start of a table with isotopes
        #Note: this header is valid for ORIGEN 6.1
        if ORIGEN_lines[line].startswith("               charge") or ORIGEN_lines[line].startswith("              initial "):
            header = ORIGEN_lines[line]
            header_columns = header[22:]
            
            #Column headers are padded with spaces at the beginning to be 10 characters wide.
            header_string =  cooling_time_string.strip()
            while len(header_string ) < 10:
                header_string = ' ' + header_string
        
            #FInd if the selected cooling time is in this table, and start readig if it does.
            if header_columns.find(header_string) != -1:
                line = line + 1
                reading_a_table = True
                column = math.ceil(header_columns.find(header_string)/10) + 1
             
        if reading_a_table == True:
            #Check that the table did not end on this row
            if ORIGEN_lines[line].startswith("   total "):
                reading_a_table = False
            else:
                #Parse the row.
                textline = ORIGEN_lines[line]
                isotope = textline[:13]
                isotope = isotope.strip()
                
                #Are we interested in this isotope?
                if isotope in isotope_searchlist:
                    textline = textline[13:]
                    split_line = textline.split(" ")
                    isotope_contents[isotope_searchlist.index(isotope)] = float(split_line[column])
                    
        line = line + 1
        
    for i in range(0,len(isotope_list)):
        if isotope_contents[i] == 0:
            print("Warning: did not find any isotopic contents for " + isotope_list[i] + " in the ORIGEN ouptut file.")
            print("Please check whether this isotope is listed correctly")

    return isotope_contents
