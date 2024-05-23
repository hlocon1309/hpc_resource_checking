# importing packages
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from simple_chalk import chalk

import re
import csv


def calculateProperties(current_dir, temp, press, eng):

    print(chalk.bold(f"\nGenerating data graphics for properties"), f"........" )

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

    data = pd.read_csv(current_dir + "/simulation/properties_data.csv")

    temperature = data.loc[:, ['Temp'] ]
    pressure = data.loc[:, ['Press'] ]
    energy = data.loc[:, ['TotEng'] ]

    teA = data["TotEng"].mean()
    pressA = data["Press"].mean()
    tempA = data["Temp"].mean()

    fig, axes = plt.subplots(1, 3, figsize=(15, 8))
    fig.suptitle('Physical Properties from Atomistic Simulations')

    if temp:
        f1 = sns.lineplot(ax=axes[0], data=temperature) ## palette="flare"
        axes[0].set_title("Temperature\nAvg = {0:.4f}".format(tempA))
        f1.set(xlabel='# of Steps', ylabel='Temperature(Lennad-Jones units)')

    if press:
        f2 = sns.lineplot(ax=axes[1], data=pressure) ## palette="crest"
        axes[1].set_title("Pressure\nAvg = {0:.4f}".format(pressA))
        f2.set(xlabel='# of Steps', ylabel='Pressure(Lennad-Jones units)')

    if eng:
        f3 = sns.lineplot(ax=axes[2], data=energy)
        axes[2].set_title("Total Energy\nAvg = {0:.4f}".format(teA))
        f3.set(xlabel='# of Steps', ylabel='Total Energy(Lennad-Jones units)')

    plt.show()



