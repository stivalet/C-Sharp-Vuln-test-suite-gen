import sys
import getopt
import time
from Flaws_generators.Generator import Generator


def main(argv):
    # List of flaws
    flaws = ["XSS", "IDOR", "Injection", "URF", "SM", "SDE"]
    flaw_list = []

    # Gets options & arguments
    try:
        opts, args = getopt.getopt(argv, "c:f:h", ["cwe=", "flaws=", "help"])
    except getopt.GetoptError:
        print('Invalid argument')
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--flaws"):  	# Select flaws
            flaw_list = arg.split(',')

        elif opt in ("-c", "--cwe"):	 # Select CWEs
            g.cwe_list = arg.split(',')

        elif opt in ("-h", "--help"):  	# Show usage
            usage()
            return 0
        else:				# Default
            usage()
            return 0

    for flaw in flaw_list:
        if flaw not in flaws:
            usage()
            return 0

    date = time.strftime("%m-%d-%Y_%Hh%Mm%S")

    # if len(flaw_list) == 0 or len(cwe_list) > 0:   # Select all flaws
    #     flaw_list = flaws
    # for flaw in flaw_list:
    #     pass

    # initialization(flaw_list)
    g = Generator(date)
    g.generate()


# TODO:90 update at the end of project
def usage():
    flaw = "-f flaws to generate (flaw1,flaw2,flaw3,...):\n\t\
                IDOR :\tInsecure Direct Object Reference\n\t\
                Injection :\tInjection (SQL,LDAP,XPATH)\n\t\
                SDE :\tSensitive Data Exposure\n\t\
                SM :\tSecurity Misconfiguration\n\t\
                URF :\tURL Redirects and Forwards\n\t\
                XSS :\tCross-site Scripting"
    cweparam = "-c generate particular CWE:\n\t\
                    78 :\tCommand OS Injection\n\t\
                    79 :\tXSS\n\t\
                    89 :\tSQL Injection\n\t\
                    90 :\tLDAP Injection\n\t\
                    91 :\tXPath Injection\n\t\
                    95 :\tCode Injection\n\t\
                    98 :\tFile Injection\n\t\
                    209 :\tInformation Exposure Through an Error Message\n\t\
                    311 :\tMissing Encryption of Sensitive Data\n\t\
                    327 :\tUse of a Broken or Risky Cryptographic Algorithm\n\t\
                    601 :\tURL Redirection to Untrusted Site\n\t\
                    862 :\tInsecure Direct Object References"
    example = "$py core.py -f Injection \t// generate test cases with Injection flaws\n\
               $py core.py -c 79 \t\t// generate test cases with cross site scripting."
    print("usage: [-f flaw | -c cwe ] [arg]\nOptions and arguments:\n", flaw, "\n", cweparam, "\n", example)


if __name__ == "__main__":
    main(sys.argv[1:])
