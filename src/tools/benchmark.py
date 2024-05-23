# importing packages
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from simple_chalk import chalk

import re
import csv


def calculateBenchmark(current_dir, tloop, tper):

    print(chalk.bold(f"\nGenerating data graphics for performance and loop time (benchmaking)"), f"........" )

    """
    with open(current_dir  + "/output.log", "r") as f:

        pattern = "Step.*?\n(.*?)Loop"
        string = f.read()
        
        extracted_data = []
        for total_data in re.findall(pattern, string, flags=re.DOTALL):
            for line in total_data.splitlines():
                extracted_data.append(line.split())

    with open(current_dir + "/simulation/properties_data.csv", "w") as f:
        titles = "Step" + "," + "PotEng" + "," + "KinEng" + "," + "TotEng" + "," + "Temp" + "," + "Press" + "," + "Density" + "\n"
        f.write(titles)
        writeData = csv.writer(f)
        writeData.writerows(extracted_data)

    """

    data = pd.read_csv(current_dir + "/performance/performance_data.csv")

    tperformance = data.loc[:, ['Performance'] ]
    time_loop = data.loc[:, ['Loop'] ]
    cores = data.loc[:, ['Cores'] ]

    #tperA = data["TotEng"].mean()
    #tloopA = data["Press"].mean()

    fig, axes = plt.subplots(1, 2, figsize=(15, 8))
    fig.suptitle('Physical Properties from Atomistic Simulations')

    if tloop:
        f1 = sns.lineplot(ax=axes[0], data=time_loop, palette="flare")
        axes[0].set_title("Loop Time")
        f1.set(xlabel='Tasks per node', ylabel='Loop Time(sec)')

    if tper:
        f2 = sns.lineplot(ax=axes[1], data=tperformance, palette="crest")
        axes[1].set_title("Performance")
        f2.set(xlabel='Tasks per node', ylabel='Performance(tau/day)')


    plt.show()
