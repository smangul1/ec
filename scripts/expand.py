import sys


with open(sys.argv[1]) as f:
    a = f.readlines()


a = map(lambda x: x.strip().split(), a)


print "sample\terror"


adict = {}
for line in a:
    name = line[0]
    rest = line[1:]
    adict[name] = rest
    

for key in ["sim_rl_50_cov_1","sim_rl_75_cov_1","sim_rl_100_cov_1","sim_rl_50_cov_2","sim_rl_75_cov_2","sim_rl_100_cov_2","sim_rl_50_cov_4","sim_rl_75_cov_4","sim_rl_100_cov_4","sim_rl_50_cov_8","sim_rl_75_cov_8","sim_rl_100_cov_8","sim_rl_50_cov_16","sim_rl_75_cov_16","sim_rl_100_cov_16","sim_rl_50_cov_32","sim_rl_75_cov_32","sim_rl_100_cov_32","sim_rl_50_cov_64","sim_rl_75_cov_64","sim_rl_100_cov_64","sim_rl_50_cov_128","sim_rl_75_cov_128","sim_rl_100_cov_128"]:
    line = adict.get(key, [])
    for element in line:
        try:
            number, count = element.split(":")
        except Exception:
            print "Something wrong in ", sys.argv[1], key
        for i in range(int(count)):
            if int(number) <= 3:
                print "%s\t%s" % (key, number)
            else:
                print "%s\t>3" % key

