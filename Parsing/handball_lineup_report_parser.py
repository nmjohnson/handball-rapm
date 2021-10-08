import getopt
import glob
import os
import pdfplumber
import tabula
import re
import sys

def main(argv):

    try:
      opts, args = getopt.getopt(argv,"hi:o:",["idir=","ofile="])
    except getopt.GetoptError:
      print('handball_lineup_report_parser.py -i <inputdirectory> -o <outputfile>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print('handball_lineup_report_parser.py -i <inputdirectory> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--idir"):
         input_directory = arg
      elif opt in ("-o", "--ofile"):
         output_filename = arg

    print("Processing PDF files in this folder: " + input_directory)

    with open(output_filename, 'a') as the_file:
        print("\"GAME_ID\",\"GAME_DATE\",\"GAME_TIME\",\"TEAM\",\"OPPONENT\",\"P1\",\"P2\",\"P3\",\"P4\",\"P5\",\"P6\",\"P7\",\"TIME_ELAPSED\",\"GF\",\"GA\"", file=the_file)
                    
    for filename in list(glob.glob(input_directory + '\*.PDF')):
        print(filename)
        file = filename
        filename = filename[filename.rfind("\\")+1:]

        all_pages = ''
        with pdfplumber.open(file) as pdf:
            for i in range(0,len(pdf.pages)):
                all_pages = all_pages + pdf.pages[i].extract_text()
            
            
        all_pages_text_array = all_pages.split('\n')

        game_date = all_pages_text_array[3]
        game_time = all_pages_text_array[4][all_pages_text_array[4].find('Time: ')+6:]
        tm1 = all_pages_text_array[7][:all_pages_text_array[7].find('-')-4].strip()
        tm2 = all_pages_text_array[7][all_pages_text_array[7].find('-')+4:].strip()
        tm1_processed = False
        actively_process_tm1 = False
        actively_process_tm2 = False
        
        for i in range(8,len(all_pages_text_array)):
            if 'Lineup effiency' in all_pages_text_array[i] and tm1_processed == False:
                actively_process_tm1 = True
            elif 'Score development' not in all_pages_text_array[i] and actively_process_tm1 == True and 'Report Created' not in all_pages_text_array[i]:
                res = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", all_pages_text_array[i])
                res_ws = ' '.join(res.split())
                col = res_ws.split(' ')
                col2 = [ x for x in col if x.isdigit() ]
                with open(output_filename, 'a') as the_file:
                    print("\"" + filename + "\",\"" + game_date + "\",\"" + game_time + "\",\"" + tm1 + "\",\"" + tm2 + "\",\"" + tm1 + "-" + col2[0] + "\",\"" + tm1 + "-" + col2[1] \
                      + "\",\"" + tm1 + "-" + col2[2] + "\",\"" + tm1 + "-" + col2[3] + "\",\"" + tm1 + "-" + col2[4]  \
                      + "\",\"" + tm1 + "-" + col2[5] + "\",\"" + tm1 + "-" + col2[6] + "\",\"" + col[len(col)-3] + "\",\"" + col[len(col)-2] + "\",\"" + col[len(col)-1] + "\"", file=the_file)
            elif ('Score development' in all_pages_text_array[i] or'Report Created' in all_pages_text_array[i]) and actively_process_tm1 == True:
                actively_process_tm1 = False
                tm1_processed = True
            elif 'Lineup effiency' in all_pages_text_array[i] and tm1_processed == True:
                actively_process_tm2 = True
            elif 'Score development' not in all_pages_text_array[i] and actively_process_tm2 == True and 'Report Created' not in all_pages_text_array[i]:
                res = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", all_pages_text_array[i])
                res_ws = ' '.join(res.split())
                col = res_ws.split(' ')
                with open(output_filename, 'a') as the_file:
                    print("\"" + filename + "\",\"" + game_date + "\",\"" + game_time + "\",\"" + tm2 + "\",\"" + tm1 + "\",\"" + tm2 + "-" + col2[0] + "\",\"" + tm2 + "-" + col2[1] \
                      + "\",\"" + tm2 + "-" + col2[2] + "\",\"" + tm2 + "-" + col2[3] + "\",\"" + tm2 + "-" + col2[4]  \
                      + "\",\"" + tm2 + "-" + col2[5] + "\",\"" + tm2 + "-" + col2[6] + "\",\"" + col[len(col)-3] + "\",\"" + col[len(col)-2] + "\",\"" + col[len(col)-1] + "\"", file=the_file)
            elif ('Score development' in all_pages_text_array[i] or'Report Created' in all_pages_text_array[i]) and actively_process_tm2 == True:
                actively_process_tm2 = False
    print("Processing complete.")

if __name__ == "__main__":
   main(sys.argv[1:])
