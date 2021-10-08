from scipy.stats import norm
import sys
import os
import pandas as pd
import numpy as np
from scipy import optimize
import getopt

##NJ: 6v6 is useful if you are NOT interested in including the goalie.

def main(argv):

    try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
      print('handball_rapm_6v6.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print('handball_rapm_6v6.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         input_filename = arg
      elif opt in ("-o", "--ofile"):
         output_filename = arg
         
	##NJ: This RAPM code was lifted from somewhere and I can't seem to retrieve where I originally found items
	##	  so please understand I am not the original creator
    # this is the regularization parameter
    l = 2

	#Read it parsed csv and organize data
    df = pd.read_csv(input_filename)
    df['TIME_ELAPSED_SEC'] = pd.to_timedelta('00:' + df['TIME_ELAPSED']).astype('timedelta64[s]').astype(int)
    avg_segment_length = df['TIME_ELAPSED_SEC'].mean()
    df['Result'] = (df['GF'])*df['TIME_ELAPSED_SEC']/avg_segment_length
    cols = [c for c in df.columns if c.startswith('P')]

    # the following code makes sure that the data frame with the lineups assigns IDs starting from 1 to number.of.players-1
    players = list(set(set(df.P1.unique()) | set(df.P2.unique())| set(df.P3.unique())| set(df.P4.unique()) | set(df.P5.unique()) | set(df.P6.unique())))


    df.P1 = df.P1.apply(lambda x: players.index(x)+1)
    df.P2 = df.P2.apply(lambda x: players.index(x)+1)
    df.P3 = df.P3.apply(lambda x: players.index(x)+1)
    df.P4 = df.P4.apply(lambda x: players.index(x)+1)
    df.P5 = df.P5.apply(lambda x: players.index(x)+1)
    df.P6 = df.P6.apply(lambda x: players.index(x)+1)

    def apm_constr(x):
        return np.mean(x)


    def obj(x):
        val_cols = [c for c in df.columns if c.startswith('P')]
        home_pred = df[val_cols[0:6]].apply(lambda i: x[i-1]).sum(axis=1)
        pred_diff = home_pred
        regularizer = l*(x**2).sum()
        err = ((df.Result - pred_diff)**2).sum() + regularizer 
        return err

	#Create an empty array
    x0 = np.zeros(shape=len(players))

	#Generate RAPM for every player in the array
    res = optimize.minimize(obj,x0,constraints=[{'type':'eq', 'fun':apm_constr}], method="SLSQP",
                            options={'maxiter':10000,'disp':True})

	#Output results and save to output file
    print("                Player   RAPM")
    with open(output_filename, 'w') as the_file:
        print("\"player\",\"rapm\"", file=the_file)
    for i in range(len(x0)):
        print("{:>20s}    {:.4f}".format(str(players[i]), res.x[i]))
        with open(output_filename, 'a') as the_file:
            print(str(players[i]) + "," + str(res.x[i]), file=the_file)


if __name__ == "__main__":
   main(sys.argv[1:])
