import os
import yaml
from pathlib import Path

#TODO: change file names management for default names + user custom names (with parser like run.py)
profile_fifo_name = "./profile-dt-mas-fifo"
messages_fifo_name = "./messages-dt-mas-fifo"

TEST_FOLDER = "./tests/"

def directory_files (dirct: Path) -> list:
    Lf = []
    if dirct.is_dir():
        for d in dirct.iterdir():
            Lf.extend(directory_files(d))
    else:
        Lf.append(dirct.name)
    return Lf

def start_simulation(messages_path, profile_path):
    print("Sending...")
    file = open(profile_path, "rb")
    profile = file.read()
    file.close()
    if not os.path.exists(profile_fifo_name):
        try:
            os.mkfifo(profile_fifo_name)
        except OSError:
            print("Failed profile fifo creation")
        else:
            pass
    out_p =  os.open(profile_fifo_name, os.O_WRONLY)
    
    os.write(out_p, profile)
    os.close(out_p)
    
    file = open(messages_path, "rb")
    messages = file.read()
    file.close()
    if not os.path.exists(messages_fifo_name):
        try:
            os.mkfifo(messages_fifo_name)
        except OSError:
            print("Failed messages fifo creation")
        else:
            pass
    out_m = os.open(messages_fifo_name, os.O_WRONLY)
    #while True:
    os.write(out_m, messages)
    os.close(out_m)
    print("Files sent and received")
    print()
    

if __name__ == "__main__":
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(
        description="Run the digital twin",
        formatter_class = ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-a",
        "-all",
        type = bool,
        default = True,
        help = "Run all the tests found in test folder"
    )
    parser.add_argument(
        "-f",
        "--folder",
        type = Path,
        default = TEST_FOLDER,
        help = "Test folder path"
    )
    parser.add_argument(
        "-t",
        "--test",
        type = str,
        default = None,
        help = "Specific test to be run, overrides -a. Only give the first part of the test path. Eg. safe.yaml -> -t safe"
    )

    # Parse arguments
    args = parser.parse_args()

    # If -t is not set, run all tests
    if args.test == None:
        #Open every test file and run simulation
        print("Doing ALL the tests")
        print()
        files = directory_files(args.folder)
        for curr_file in files:
            if (not ("_profile.yaml" in curr_file)):
                mess_path = args.folder.joinpath(curr_file)
                profile_file = curr_file.split(".yaml")[0] + "_profile.yaml"
                profile_path = args.folder.joinpath(profile_file)
                print("Messages file : ",end="")
                print(mess_path)
                print("Profile file : ",end="")
                print(profile_path)
                start_simulation(mess_path,profile_path)

        #start_simulation()
    else:
        #start_simulation(args.test+".yaml",args.test+"_profile.yaml")
        mess_path = args.folder.joinpath(args.test+".yaml")
        profile_path = args.folder.joinpath(args.test+"_profile.yaml")
        print("Messages file : ",end="")
        print(mess_path)
        print("Profile file : ",end="")
        print(profile_path)
        if not os.path.exists(mess_path):
            raise Exception("Test files do not exist in test folder")
        start_simulation(mess_path,profile_path)
        #print("folder : "+ args.folder+"path : "+args.test+".yaml"+" "+args.test+"_profile.yaml")
