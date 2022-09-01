#Birthday Problem: 100% at 367, 99.9% at 70, 50% at 23
import calendar
import os
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def MainLoop(num_people, num_iterations): 
    birthdays = []
    birth_months = []
    birth_days = []
    current_people = 0
    current_iteration = 0
    total_matches = 0
    match_flag = 0
    last_run = 0

    plt.rcParams['toolbar'] = 'None'
    fig = plt.figure(figsize = (9, 3))
    text_runs = plt.text(0, 0, "TOTAL RUNS: 0")
    text_matches = plt.text(12, 0, "TOTAL MATCHES: 0")
    text_percentage = plt.text(25, 0, "CURRENT PERCENTAGE: 0%")
    dynamic_shapes = plt.gca().axes
    
    while current_iteration < num_iterations:    
        while current_people < num_people:
            date = GetRandDate(birth_months, birth_days)     
            if CheckList(birthdays, date):
                if match_flag == 0:
                    total_matches += 1
                    match_flag = 1
            birthdays.append(date)
            current_people += 1
        
        GraphStats(fig, current_iteration, total_matches, text_runs, text_matches, text_percentage)
        first_flag = 0

        if num_iterations >= 500:
            if current_iteration % 50 == 0:
                PlotCalendar(fig, dynamic_shapes, birth_days, birth_months, birthdays, last_run)
            elif current_iteration == num_iterations - 1:
                last_run = 1
                PlotCalendar(fig, dynamic_shapes, birth_days, birth_months, birthdays, last_run)
        else:  
            if num_iterations >= 25 and current_iteration % 25 == 0:
                PlotCalendar(fig, dynamic_shapes, birth_days, birth_months, birthdays, last_run)
            elif current_iteration == num_iterations - 1:
                last_run = 1
                PlotCalendar(fig, dynamic_shapes, birth_days, birth_months, birthdays, last_run)

        birth_days.clear()
        birth_months.clear()
        birthdays.clear()
        match_flag = 0
        current_people = 0
        current_iteration += 1
        
 
def CheckList(birthdays, date):
    if date in birthdays:
        return True
    else:
        return False


def DateFormat(month, day):
    str_month = str(month)
    str_day = str(day)
    
    if month < 10:
        str_month = '0' + str_month
    if day < 10:
        str_day = '0' + str_day
        
    return str_month + str_day


def GetRandDate(birth_months, birth_days):
    month = random.randrange(1, 12, 1)
    birth_months.append(month)
    
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        day = random.randrange(1, 31, 1)
        birth_days.append(day)
        return DateFormat(month, day)
     
    elif month == 4 or month == 6 or month == 9 or month == 11:
        day = random.randrange(1, 30, 1)
        birth_days.append(day)
        return DateFormat(month, day)

    else:
        day = random.randrange(1, 29, 1)
        birth_days.append(day)
        return DateFormat(month, day)


def GraphStats(fig, current_iteration, total_matches, text_runs, text_matches, text_percentage):
    text_runs.set_text("TOTAL RUNS: " + str(current_iteration + 1))
    text_matches.set_text("TOTAL MATCHES: " + str(total_matches))
    text_percentage.set_text("CURRENT PERCENTAGE: " + str(round(((total_matches / (current_iteration + 1)) * 100), 2)) + "%")
    fig.canvas.draw() 

    
def PlotCalendar(fig, dynamic_shapes, birth_days, birth_months, birthdays, last_run):
    InitialDraw(dynamic_shapes)
    GraphUpdate(birth_days, birth_months, dynamic_shapes, birthdays)
    plt.pause(2)
    
    if last_run == 1:
        return
    
    GraphRemove(birth_days, birth_months, dynamic_shapes)
    fig.canvas.draw()    

    
def InitialDraw(dynamic_shapes):
    dynamic_shapes.add_patch(Rectangle((30, 2), width = 0.8, height = 0.8, color = 'gray', alpha = 0.5))
    dynamic_shapes.add_patch(Rectangle((31, 2), width = 0.8, height = 0.8, color = 'gray', alpha = 0.5))
    dynamic_shapes.add_patch(Rectangle((31, 4), width = 0.8, height = 0.8, color = 'gray', alpha = 0.5))
    dynamic_shapes.add_patch(Rectangle((31, 6), width = 0.8, height = 0.8, color = 'gray', alpha = 0.5))
    dynamic_shapes.add_patch(Rectangle((31, 9), width = 0.8, height = 0.8, color = 'gray', alpha = 0.5))
    dynamic_shapes.add_patch(Rectangle((31, 11), width = 0.8, height = 0.8, color = 'gray', alpha = 0.5))
        
    plt.yticks(np.arange(1, 13) + 0.5, list(calendar.month_abbr)[1:])
    plt.xticks(np.arange(1, 32) + 0.5, np.arange(1, 32))
    plt.xlim(1, 32)
    plt.ylim(1, 13)
    plt.gca().invert_yaxis()

    for spine in plt.gca().spines.values():
        spine.set_visible(False)
        
    plt.tick_params(top = False, bottom = False, left = False, right = False)
    plt.show(block = False)


def GraphUpdate(birth_days, birth_months, dynamic_shapes, birthdays):
    match_set = set([x for x in birthdays if birthdays.count(x) > 1])
    match_flag = 0

    for d, m in zip(birth_days, birth_months):
        plt.pause(0.1)
        for date in match_set:
            if int(date[0:2]) == m and int(date[2:4]) == d:
                dynamic_shapes.add_patch(Rectangle((d, m), width = 0.8, height = 0.8, color = 'green'))
                match_flag = 1
                break

        if match_flag == 0:
            dynamic_shapes.add_patch(Rectangle((d, m), width = 0.8, height = 0.8, color = 'red'))
            
        match_flag = 0

        
def GraphRemove(birth_days, birth_months, dynamic_shapes):
    for patches in reversed(dynamic_shapes.patches):
        patches.remove()
        if len(dynamic_shapes.patches) == 6:
            return

        
def main():
    num_people = int(input("Enter number of people: "))
    num_iterations = int(input("Enter number of runs: "))
    MainLoop(num_people, num_iterations)
    os.system("pause")


if __name__ == "__main__":
    main()