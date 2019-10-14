import os, glob, csv, argparse
#Variable for csv file
csv_file = []
directory = []
#end of variable declaration

#Start of functions
def find_path(path):
    """Finding the directory of the pathname path"""
    os.chdir(path)
    if os.path.exists(path) == True:
        pass

    else:
        return "Path directory doesn't exists"

def csv_save(path, csvfilename):
    """After completing the find_path function, csv_save function will get the files and subdirectories of the path provided
     by the user. Then it will be save as a csv file, name provided by the user."""
    with open(csvfilename + '.csv','w+', newline='') as csvFile:
        headwriter = csv.DictWriter(csvFile, fieldnames = ["Parent Directory","Filename","File Size"])
        headwriter.writeheader()
        writer = csv.writer(csvFile, delimiter=",")
        for r,d,files in os.walk(path):
            for f in files:
                size = os.path.getsize("{}\{}".format(r,f))
                row = [str(r), f, size]
                writer.writerow(row)
    return csv_save

def main():
    """Main function of the program"""
    parser = argparse.ArgumentParser()
    parser.add_argument('path',help = 'Path directory', type = str)
    parser.add_argument('csvfilename',help = 'CSV filename to be saved', type = str)


    args = parser.parse_arg()
    find_path(args.path)
    csv_save(args.path,args.csvfilename)
#end of functions


if __name__== "__main__":
    main()

