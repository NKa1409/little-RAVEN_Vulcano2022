import math
import time
import matplotlib
import pandas
import tkinter.filedialog
import datetime
import sys


def df_column_to_list(df, column):
    try:
        liste = df[column].tolist()
        return liste
    except:
        pass
    try:
        liste = df[df.columns[column]].tolist()
        return liste
    except:
        pass
    if len(df.columns) == 1:
        try:
            liste = df[df.columns[0]].tolist()
            return liste
        except:
            return None


def plot_graph_with_2_subplots_2_data_in_upper_one_data_in_lower(x, y1, y1err, x2, y2, y2err, x3, y3, y3err, title="Title", first_data_name="first_data", second_data_name="second_data", third_data_name="third_data", x_axis_name="x-axis", y2_axis_name="y2-axis", y1_1_axis_name="y11-axis", y1_2_axis_name="y12-axis"):
    import matplotlib.pyplot as plt
    plt.style.use("seaborn-talk")
    plt.ion()
    fig, ax = plt.subplots(2, 1)

    co2plot = ax[0].plot(x, y1, color="red", linestyle="-", linewidth=1, label=first_data_name)
    upper_error2 = []
    lower_error2 = []
    for iteration in range(0, len(y1), 1):
        upper_error2.append(y1[iteration] + y1err[iteration])
        lower_error2.append(y1[iteration] - y1err[iteration])
    ax[0].fill_between(x, lower_error2, upper_error2, alpha=0.1, color="red")
    ax[0].set_ylim(180, 1250)
    fig.autofmt_xdate()

    sec_y_ax = ax[0].twinx()
    so2plot = sec_y_ax.plot(x2, y2, color="black", linestyle="-", linewidth=1, label=second_data_name)
    upper_error2 = []
    lower_error2 = []
    for iteration in range(0, len(y2), 1):
        upper_error2.append(y2[iteration] + y2err[iteration])
        lower_error2.append(y2[iteration] - y2err[iteration])
    sec_y_ax.fill_between(x2, lower_error2, upper_error2, alpha=0.1, color="black")

    lines_in_ax0 = co2plot + so2plot
    labs = [l.get_label() for l in lines_in_ax0]
    ax[0].legend(lines_in_ax0, labs, loc=0)

    ax[0].set_ylabel(y1_1_axis_name)
    sec_y_ax.set_ylabel(y1_2_axis_name)

    ax[0].set_xticks(x[::100])
    #ax[0].set_xticklabels(x[::100], rotation=45)



    ax[1].scatter(x3, y3, color="black", label=third_data_name, marker="x", s=1)
    upper_error2 = []
    lower_error2 = []
    for iteration in range(0, len(y3), 1):
        try:
            upper_error2.append(y3[iteration] + y3err[iteration])
            lower_error2.append(y3[iteration] - y3err[iteration])
        except TypeError:
            upper_error2.append(0)
            lower_error2.append(0)
    ax[1].fill_between(x3, lower_error2, upper_error2, alpha=0.1, color="black")
    ax[1].set_xticks(x3[::100])
    #ax[1].set_ylim(-20, 20)
    #ax[1].set_xticklabels(x[::100], rotation=45)

    #ax[1].set_xlabel("timestamp")
    ax[1].set_ylabel(y2_axis_name)
    ax[1].set_xlabel(x_axis_name)
    ax[1].set_ylim(0, 100)
    plt.grid(False)
    ax[0].set_title(title, loc="left")
    filename = str(datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')) + ".jpg"
    plt.savefig(filename)
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.show()
    time.sleep(1)


def plot_graph_three_in_one_plot(x, y1, y1err, y2, y2err, y3, y3err, title="Title", first_data_name="first_data", second_data_name="second_data", third_data_name="third_data", x_axis_name="x-axis", y_axis_name="y-axis"):
    import matplotlib.pyplot as plt
    plt.style.use("seaborn-talk")

    plt.plot(x, y1, color="red", linestyle="-", linewidth=1, label=first_data_name)
    upper_error1 = []
    lower_error1 = []
    for iteration in range(0, len(y1), 1):
        upper_error1.append(y1[iteration] + y1err[iteration])
        lower_error1.append(y1[iteration] - y1err[iteration])
    plt.fill_between(x, upper_error1, lower_error1, alpha=0.15, facecolor="red", edgecolor="red")
    plt.xticks(x[::100])

    plt.plot(x, y2, color="black", linestyle="-", linewidth=1, label=second_data_name)
    upper_error2 = []
    lower_error2 = []
    for iteration in range(0, len(y2), 1):
        upper_error2.append(y2[iteration] + y2err[iteration])
        lower_error2.append(y2[iteration] - y2err[iteration])
    plt.fill_between(x, upper_error2, lower_error2, alpha=0.15, facecolor="black", edgecolor="black")
    # ax[1].set_xticklabels(x[::100], rotation=45)

    plt.plot(x, y3, color="blue", linestyle="-", linewidth=1, label=third_data_name)
    upper_error3 = []
    lower_error3 = []
    for iteration in range(0, len(y3), 1):
        upper_error3.append(y3[iteration] + y3err[iteration])
        lower_error3.append(y3[iteration] - y3err[iteration])
    plt.fill_between(x, upper_error3, lower_error3, alpha=0.15, facecolor="blue", edgecolor="blue")

    # ax[1].set_xlabel("timestamp")
    plt.ylabel(y_axis_name)
    plt.xlabel(x_axis_name)
    plt.legend()
    plt.grid(False)
    plt.title(title, loc="left")
    filename = str(datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')) + ".jpg"
    plt.savefig(filename)
    plt.show()


def plot_graph(x, y1, y1err, y2, y2err):
    import matplotlib.pyplot as plt
    plt.style.use("seaborn-talk")
    plt.ion()
    fig, ax = plt.subplots(2, 1)

    ax[0].plot(x, y1, color="red", linestyle="-", linewidth=1, label="SO2")
    upper_error1 = []
    lower_error1 = []
    for iteration in range(0, len(y1), 1):
        upper_error1.append(y1[iteration] + y1err[iteration])
        lower_error1.append(y1[iteration] - y1err[iteration])
    ax[0].fill_between(x, upper_error1, lower_error1, alpha=0.15, facecolor="red", edgecolor="red")
    ax[0].set_xticks(x[::100])
    #ax[0].set_xticklabels(x[::100], rotation=45)


    ax[0].set_ylabel("SO2 / ppm")
    ax[1].plot(x, y2, color="black", linestyle="-", linewidth=1, label="CO2")
    upper_error2 = []
    lower_error2 = []
    for iteration in range(0, len(y2), 1):
        upper_error2.append(y2[iteration] + y2err[iteration])
        lower_error2.append(y2[iteration] - y2err[iteration])
    ax[1].fill_between(x, upper_error2, lower_error2, alpha=0.15, facecolor="black", edgecolor="black")
    ax[1].set_xticks(x[::100])
    #ax[1].set_xticklabels(x[::100], rotation=45)

    #ax[1].set_xlabel("timestamp")
    ax[1].set_ylabel("CO2 / ppm")
    plt.grid(False)
    ax[0].set_title("SO2 / CO2 - 11.04.22 18:17-18:36", loc="left")
    filename = str(datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')) + ".jpg"
    plt.savefig(filename)
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.show()



csv_file = "Validation flight.txt"
df = pandas.read_table(csv_file, sep=",", header=0, decimal=".", error_bad_lines=True)

timelist = df_column_to_list(df, "time")
for element in range(0, len(timelist), 1):
    timelist[element] = datetime.datetime.strptime(timelist[element], "%H:%M:%S")
    timelist[element] = datetime.datetime.strftime(timelist[element], "%H:%M:%S")

co2_smooth = df_column_to_list(df, "CO2 / ppm_smooth_9_3")
co2_stat_error = df_column_to_list(df, "CO2 / ppm_smooth_9_3_staticerror_0.00364_4.4")
co2_rt_corr = df_column_to_list(df, "CO2 / ppm_smooth_9_3_rt_corrected_40")
co2_rt_corr_shifted = df_column_to_list(df, "CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11")
co2_rt_corr_shifted_smooth = df_column_to_list(df, "CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_smooth_9_3")
co2_rt_corr_error = df_column_to_list(df, "CO2 / ppm_smooth_9_3_staticerror_0.00364_4.4_with_complete_rt_error")
so2_smooth = df_column_to_list(df, "SO2 / ppm_smooth_9_3")
so2_stat_error = df_column_to_list(df, "SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06")
so2_rt_corr = df_column_to_list(df, "SO2 / ppm_smooth_9_3_rt_corrected_8")
so2_rt_corr_smooth = df_column_to_list(df, "SO2 / ppm_smooth_9_3_rt_corrected_8_smooth_9_3")
so2_rt_corr_error = df_column_to_list(df, "SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06_with_complete_rt_error")

co2_smartgas_smooth = df_column_to_list(df, "CO2 (smartGAS) / ppm_smooth_9_3")
co2_smartgas_error = df_column_to_list(df, "CO2 (smartGAS) / ppm_smooth_9_3_staticerror_0.075_2.12")

ratio_rt_smooth__rt_smooth = df_column_to_list(df, "ratio_CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_smooth_9_3_SO2 / ppm_smooth_9_3_rt_corrected_8_smooth_9_3")
ratio_rt__rt = df_column_to_list(df, "ratio_CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_SO2 / ppm_smooth_9_3_rt_corrected_8")
ratio_rt__smooth = df_column_to_list(df, "ratio_CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_SO2 / ppm_smooth_9_3")
ratio_rt_smooth__smooth = df_column_to_list(df, "ratio_CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_smooth_9_3_SO2 / ppm_smooth_9_3")
ratio_sg_smooth__smooth = df_column_to_list(df, "ratio_CO2 (smartGAS) / ppm_smooth_9_3_SO2 / ppm_smooth_9_3")
ratio_sg_smooth__rt_smooth = df_column_to_list(df, "ratio_CO2 (smartGAS) / ppm_smooth_9_3_SO2 / ppm_smooth_9_3_rt_corrected_8")

ratio_error_rt_smooth__rt_smooth = df_column_to_list(df, "ratio_error_CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_smooth_9_3_CO2 / ppm_smooth_9_3_staticerror_0.00364_4.4_with_complete_rt_error_SO2 / ppm_smooth_9_3_rt_corrected_8_smooth_9_3_SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06_with_complete_rt_error_420")
ratio_error_rt__rt = df_column_to_list(df, "ratio_error_CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_CO2 / ppm_smooth_9_3_staticerror_0.00364_4.4_with_complete_rt_error_SO2 / ppm_smooth_9_3_rt_corrected_8_SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06_with_complete_rt_error_420")
ratio_error_rt__smooth = df_column_to_list(df, "ratio_error_CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_CO2 / ppm_smooth_9_3_staticerror_0.00364_4.4_with_complete_rt_error_SO2 / ppm_smooth_9_3_SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06_420")
ratio_error_rt_smooth__smooth = df_column_to_list(df, "ratio_error_CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_smooth_9_3_CO2 / ppm_smooth_9_3_staticerror_0.00364_4.4_with_complete_rt_error_SO2 / ppm_smooth_9_3_SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06_420")
ratio_error_sg_smooth__smooth = df_column_to_list(df, "ratio_error_CO2 (smartGAS) / ppm_smooth_9_3_CO2 (smartGAS) / ppm_smooth_9_3_staticerror_0.075_2.12_SO2 / ppm_smooth_9_3_SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06_420")
ratio_error_sg_smooth__rt_smooth = df_column_to_list(df, "ratio_error_CO2 (smartGAS) / ppm_smooth_9_3_CO2 (smartGAS) / ppm_smooth_9_3_staticerror_0.075_2.12_SO2 / ppm_smooth_9_3_rt_corrected_8_SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06_with_complete_rt_error_420")

for index in range(0, len(ratio_rt_smooth__rt_smooth), 1):
    if co2_rt_corr_shifted_smooth[index]-420 <= co2_rt_corr_error[index] or so2_rt_corr_smooth[index] <= so2_rt_corr_error[index] or ratio_rt_smooth__rt_smooth[index] <= ratio_error_rt_smooth__rt_smooth[index] or ratio_error_rt_smooth__rt_smooth[index] > 30:
        ratio_rt_smooth__rt_smooth[index] = None
    else:
        pass
corrected_ratio_col_name1 = "ratio_CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_smooth_9_3_SO2 / ppm_smooth_9_3_rt_corrected_8_smooth_9_3" + "_corrected"
df[corrected_ratio_col_name1] = ratio_rt_smooth__rt_smooth


for index in range(0, len(ratio_rt__rt), 1):
    if co2_rt_corr_shifted[index]-420 <= co2_rt_corr_error[index] or so2_rt_corr[index] <= so2_rt_corr_error[index] or ratio_rt__rt[index] <= ratio_error_rt__rt[index] or ratio_error_rt__rt[index] > 30:
        ratio_rt__rt[index] = None
    else:
        pass
corrected_ratio_col_name2 = "ratio_CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_SO2 / ppm_smooth_9_3_rt_corrected_8" + "_corrected"
df[corrected_ratio_col_name2] = ratio_rt__rt

for index in range(0, len(ratio_rt__smooth), 1):
    if co2_rt_corr_shifted[index]-420 <= co2_rt_corr_error[index] or so2_smooth[index] <= so2_stat_error[index] or ratio_rt__smooth[index] <= ratio_error_rt__smooth[index] or ratio_error_rt__smooth[index] > 30:
        ratio_rt__smooth[index] = None
    else:
        pass
corrected_ratio_col_name3 = "ratio_CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_SO2 / ppm_smooth_9_3" + "_corrected"
df[corrected_ratio_col_name3] = ratio_rt__smooth

for index in range(0, len(ratio_rt_smooth__smooth), 1):
    if co2_rt_corr_shifted_smooth[index]-420 <= co2_rt_corr_error[index] or so2_smooth[index] <= so2_stat_error[index] or ratio_rt_smooth__smooth[index] <= ratio_error_rt_smooth__smooth[index] or ratio_error_rt_smooth__smooth[index] > 30:
        ratio_rt_smooth__smooth[index] = None
    else:
        pass
corrected_ratio_col_name4 = "ratio_CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_smooth_9_3_SO2 / ppm_smooth_9_3" + "_ratioscorrected"
df[corrected_ratio_col_name4] = ratio_rt_smooth__smooth

for index in range(0, len(ratio_sg_smooth__smooth), 1):
    if co2_smartgas_smooth[index]-420 <= co2_smartgas_error[index] or so2_smooth[index] <= so2_stat_error[index] or ratio_sg_smooth__smooth[index] <= ratio_error_sg_smooth__smooth[index] or ratio_error_sg_smooth__smooth[index] > 30:
        ratio_sg_smooth__smooth[index] = None
    else:
        pass
corrected_ratio_col_name5 = "ratio_CO2 (smartGAS) / ppm_smooth_9_3_SO2 / ppm_smooth_9_3" + "_ratioscorrected"
df[corrected_ratio_col_name5] = ratio_sg_smooth__smooth

for index in range(0, len(ratio_sg_smooth__rt_smooth), 1):
    if co2_smartgas_smooth[index]-420 <= co2_smartgas_error[index] or so2_smooth[index] <= so2_stat_error[index] or ratio_sg_smooth__rt_smooth[index] <= ratio_error_sg_smooth__rt_smooth[index] or ratio_error_sg_smooth__rt_smooth[index] > 30:
        ratio_sg_smooth__rt_smooth[index] = None
    else:
        pass
corrected_ratio_col_name6 = "ratio_CO2 (smartGAS) / ppm_smooth_9_3_SO2 / ppm_smooth_9_3_rt_corrected_8" + "_ratioscorrected"
df[corrected_ratio_col_name6] = ratio_sg_smooth__rt_smooth
df.to_csv(csv_file, index_label=False)



#plot_graph_three_in_one_plot(timelist, co2_smooth, co2_stat_error, co2_rt_corr_shifted_smooth, co2_rt_corr_error, co2_smartgas_smooth, co2_smartgas_error, title="Validation flight", first_data_name="CO2 (S300)", second_data_name="CO2 r.c. smooth", third_data_name="CO2 smartGAS smooth", x_axis_name="time", y_axis_name="CO2 / ppm")
#plot_graph_three_in_one_plot(timelist, so2_smooth, so2_stat_error, so2_rt_corr, so2_rt_corr_error, so2_rt_corr_smooth, so2_rt_corr_error, title="Validation flight", first_data_name="SO2 (AS)", second_data_name="SO2 response corrected", third_data_name="SO2 r.c. smooth", x_axis_name="time", y_axis_name="SO2 / ppm")

#plot_graph_with_2_subplots_2_data_in_upper_one_data_in_lower(timelist, co2_rt_corr_shifted_smooth, co2_rt_corr_error, timelist, so2_rt_corr_smooth, so2_rt_corr_error, timelist, ratio_rt_smooth__rt_smooth, ratio_error_rt_smooth__rt_smooth, title="Validation flight", first_data_name="CO2 r.c. smooth", second_data_name="SO2 (AS) r.c. smooth", third_data_name="CO2/SO2 ratio", x_axis_name="time", y1_1_axis_name="CO2 / ppm", y1_2_axis_name="SO2 / ppm", y2_axis_name="CO2/SO2")
#plot_graph_with_2_subplots_2_data_in_upper_one_data_in_lower(timelist, co2_rt_corr_shifted, co2_rt_corr_error, timelist, so2_rt_corr, so2_rt_corr_error, timelist, ratio_rt__rt, ratio_error_rt__rt, title="Validation flight", first_data_name="CO2 r.c.", second_data_name="SO2 (AS) r.c.", third_data_name="CO2/SO2 ratio", x_axis_name="time", y1_1_axis_name="CO2 / ppm", y1_2_axis_name="SO2 / ppm", y2_axis_name="CO2/SO2")
#plot_graph_with_2_subplots_2_data_in_upper_one_data_in_lower(timelist, co2_rt_corr_shifted, co2_rt_corr_error, timelist, so2_smooth, so2_stat_error, timelist, ratio_rt__smooth, ratio_error_rt__smooth, title="Validation flight", first_data_name="CO2 r.c.", second_data_name="SO2 (AS) smooth", third_data_name="CO2/SO2 ratio", x_axis_name="time", y1_1_axis_name="CO2 / ppm", y1_2_axis_name="SO2 / ppm", y2_axis_name="CO2/SO2")
plot_graph_with_2_subplots_2_data_in_upper_one_data_in_lower(timelist, co2_smartgas_smooth, co2_smartgas_error, timelist, so2_smooth, so2_stat_error, timelist, ratio_sg_smooth__smooth, ratio_error_sg_smooth__smooth, title="Validation flight", first_data_name="CO2 smartGAS", second_data_name="SO2 (AS) smooth", third_data_name="CO2/SO2 ratio", x_axis_name="time", y1_1_axis_name="CO2 / ppm", y1_2_axis_name="SO2 / ppm", y2_axis_name="CO2/SO2")
plot_graph_with_2_subplots_2_data_in_upper_one_data_in_lower(timelist, co2_smartgas_smooth, co2_smartgas_error, timelist, so2_rt_corr_smooth, so2_rt_corr_error, timelist, ratio_sg_smooth__rt_smooth, ratio_error_sg_smooth__rt_smooth, title="Validation flight", first_data_name="CO2 smartGAS", second_data_name="SO2 (AS) r.c. smooth", third_data_name="CO2/SO2 ratio", x_axis_name="time", y1_1_axis_name="CO2 / ppm", y1_2_axis_name="SO2 / ppm", y2_axis_name="CO2/SO2")
