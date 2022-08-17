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


def add_static_error(csv_filename, col_name, std_dev, error_of_slope):
    df = pandas.read_table(csv_filename, sep=",", header=0, decimal=".", error_bad_lines=True)
    values = df_column_to_list(df, col_name)
    error = []
    for element in values:
        error.append((element * error_of_slope) + (3 * std_dev))
    error_col_name = col_name + "_staticerror_" + str(error_of_slope) + "_" + str(std_dev)
    df[error_col_name] = error
    df.to_csv(csv_filename, index_label=False)


def add_rt_corr_error(csv_filename, static_error_col_name, orig_values_col_name, duration_col_name):
    df = pandas.read_table(csv_filename, sep=",", header=0, decimal=".", error_bad_lines=True)
    static_error = df_column_to_list(df, static_error_col_name)
    values = df_column_to_list(df, orig_values_col_name)
    duration = df_column_to_list(df, duration_col_name)
    variable_error = []
    for index in range(0, len(values), 1):
        try:
            variable_error.append(static_error[index] + abs((3 * ((values[index+1]-values[index])/(duration[index+1]-duration[index])))))
        except:
            variable_error.append(0)
    var_error_col_name = static_error_col_name + "_with_complete_rt_error"
    df[var_error_col_name] = variable_error
    df.to_csv(csv_filename, index_label=False)


def add_rt_correction(csv_filename, values_col_name, duration_col_name, response_time):
    df = pandas.read_table(csv_filename, sep=",", header=0, decimal=".", error_bad_lines=True)
    values = df_column_to_list(df, values_col_name)
    duration = df_column_to_list(df, duration_col_name)
    rt_corr_values = []
    for index in range(0, len(values), 1):
        try:
            rt_corr_values.append(values[index] + (((values[index+1]-values[index])/(duration[index+1]-duration[index]))*response_time))
        except:
            rt_corr_values.append(0)
    rt_val_colname = values_col_name + "_rt_corrected_" + str(response_time)
    df[rt_val_colname] = rt_corr_values
    df.to_csv(csv_filename, index_label=False)


def add_sav_gol_filter(csv_filename, col_name, window, polyorder=3, derivative=0):
    from scipy.signal import savgol_filter
    import numpy as np
    df = pandas.read_table(csv_filename, sep=",", header=0, decimal=".", error_bad_lines=True)
    x = df_column_to_list(df, col_name)
    func_x = tuple(x)
    func_x = list(func_x)
    func_x = np.array(func_x)
    filtered_x = savgol_filter(func_x, window, polyorder, derivative)
    filtered_x = list(filtered_x)
    smooth_col_name = col_name + "_smooth_" + str(window) + "_" + str(polyorder)
    df[smooth_col_name] = filtered_x
    df.to_csv(csv_filename, index_label=False)


def add_shifted_values(csv_filename, col_name, duration_col_name, seconds_to_shift):
    df = pandas.read_table(csv_filename, sep=",", header=0, decimal=".", error_bad_lines=True)
    values = df_column_to_list(df, col_name)
    duration = df_column_to_list(df, duration_col_name)
    shifted_values = []
    for index in range(0, len(values), 1):
        delta_index = 0
        while True:
            try:
                delta_seconds = round((duration[index] - duration[index-delta_index]), 0)
                if delta_seconds == seconds_to_shift or delta_seconds > int(round((seconds_to_shift-((duration[1]-duration[0])/2)), 0)):
                    break
                elif (delta_seconds < round((seconds_to_shift-((duration[1]-duration[0])/2)), 0)) or (delta_seconds == round((seconds_to_shift-((duration[1]-duration[0])/2)), 0)):
                    delta_index = delta_index + 1
                else:
                    print("error")
            except:
                delta_index = - 1
                break
        if delta_index == -1:
            shifted_values.append(0)
        else:
            try:
                shifted_values.append(values[index + delta_index])
            except IndexError:
                shifted_values.append(0)
    shifted_val_col_name = col_name + "_shifted_" + str(seconds_to_shift)
    df[shifted_val_col_name] = shifted_values
    df.to_csv(csv_filename, index_label=False)


def add_ratio(csv_filename, co2_values_col_name, so2_values_col_name, ambient_co2):
    df = pandas.read_table(csv_filename, sep=",", header=0, decimal=".", error_bad_lines=True)
    co2 = df_column_to_list(df, co2_values_col_name)
    so2 = df_column_to_list(df, so2_values_col_name)
    ratio = []
    for index in range(0, len(co2), 1):
        try:
            ratio.append((co2[index] - ambient_co2) / so2[index])
        except ZeroDivisionError:
            ratio.append(0)
    ratio_col_name = "ratio_" + str(co2_values_col_name) + "_" + str(so2_values_col_name)
    df[ratio_col_name] = ratio
    df.to_csv(csv_filename, index_label=False)


def add_ratio_error(csv_filename, co2_values_col_name, co2_err_col_name, so2_values_col_name, so2_err_col_name, ambient_co2):
    df = pandas.read_table(csv_filename, sep=",", header=0, decimal=".", error_bad_lines=True)
    co2 = df_column_to_list(df, co2_values_col_name)
    co2_err = df_column_to_list(df, co2_err_col_name)
    so2 = df_column_to_list(df, so2_values_col_name)
    so2_err = df_column_to_list(df, so2_err_col_name)
    ratio_err = []
    for index in range(0, len(co2), 1):
        try:
            ratio_err.append(math.sqrt( ((co2_err[index]/so2[index])**2) + (( ((co2[index])/((so2[index])**2)) * so2_err[index] )**2) ))
        except ZeroDivisionError:
            ratio_err.append(0)
        except TypeError:
            ratio_err.append(0)
    ratio_err_col_name = "ratio_error_" + str(co2_values_col_name) + "_" + str(co2_err_col_name) + "_" + str(so2_values_col_name) + "_" + str(so2_err_col_name) + "_" + str(ambient_co2)
    df[ratio_err_col_name] = ratio_err
    df.to_csv(csv_filename, index_label=False)






csv_file = "Validation flight.txt"

add_sav_gol_filter(csv_file, "CO2 / ppm", window=9)
add_sav_gol_filter(csv_file, "SO2 / ppm", window=9)
add_rt_correction(csv_file, "CO2 / ppm_smooth_9_3", "duration / s", 40)
add_rt_correction(csv_file, "SO2 / ppm_smooth_9_3", "duration / s", 8)
add_shifted_values(csv_file, "CO2 / ppm_smooth_9_3_rt_corrected_40", "duration / s", 11)


# error of slope CO2: before: 1.100 after: 1.096 --> (1.100-1.096)/1.098 = 0.00364
# error of slope SO2: before: 0.122 after: 0.126 --> (0.126-0.122)/0.124 = 0.0323
# std_dev: calculated with excel at times of only background concentration (outside plume)
# Std_dev:        CO2; SO2
# 1. measurement: 6.3; 0.26
# 2. measurement: 8.15; 0.25
# validation flight: 4.4; 0.06
# validation flight smartGAS sensors: 2.12; 9.7
add_static_error(csv_file, "CO2 / ppm_smooth_9_3", std_dev=4.4, error_of_slope=0.00364)
add_static_error(csv_file, "SO2 / ppm_smooth_9_3", std_dev=0.06, error_of_slope=0.0323)
add_rt_corr_error(csv_file, "CO2 / ppm_smooth_9_3_staticerror_0.00364_4.4", "CO2 / ppm_smooth_9_3", "duration / s")
add_rt_corr_error(csv_file, "SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06", "SO2 / ppm_smooth_9_3", "duration / s")
add_sav_gol_filter(csv_file, "CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11", window=9)
add_sav_gol_filter(csv_file, "SO2 / ppm_smooth_9_3_rt_corrected_8", window=9)

add_sav_gol_filter(csv_file, "CO2 (smartGAS) / ppm", window=9)
add_sav_gol_filter(csv_file, "SO2 (smartGAS) / ppm", window=9)
add_static_error(csv_file, "CO2 (smartGAS) / ppm_smooth_9_3", std_dev=2.12, error_of_slope=0.075)
add_static_error(csv_file, "SO2 (smartGAS) / ppm_smooth_9_3", std_dev=9.7, error_of_slope=0)

ambient_co2 = 420

add_ratio(csv_file, "CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11", "SO2 / ppm_smooth_9_3_rt_corrected_8", ambient_co2)
add_ratio_error(csv_file, "CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11", "CO2 / ppm_smooth_9_3_staticerror_0.00364_4.4_with_complete_rt_error",
                "SO2 / ppm_smooth_9_3_rt_corrected_8", "SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06_with_complete_rt_error", ambient_co2)

add_ratio(csv_file, "CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_smooth_9_3", "SO2 / ppm_smooth_9_3_rt_corrected_8_smooth_9_3", ambient_co2)
add_ratio_error(csv_file, "CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_smooth_9_3", "CO2 / ppm_smooth_9_3_staticerror_0.00364_4.4_with_complete_rt_error",
                "SO2 / ppm_smooth_9_3_rt_corrected_8_smooth_9_3", "SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06_with_complete_rt_error", ambient_co2)


add_ratio(csv_file, "CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11", "SO2 / ppm_smooth_9_3", ambient_co2)
add_ratio_error(csv_file, "CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11", "CO2 / ppm_smooth_9_3_staticerror_0.00364_4.4_with_complete_rt_error",
                "SO2 / ppm_smooth_9_3", "SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06", ambient_co2)

add_ratio(csv_file, "CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_smooth_9_3", "SO2 / ppm_smooth_9_3", ambient_co2)
add_ratio_error(csv_file, "CO2 / ppm_smooth_9_3_rt_corrected_40_shifted_11_smooth_9_3", "CO2 / ppm_smooth_9_3_staticerror_0.00364_4.4_with_complete_rt_error",
                "SO2 / ppm_smooth_9_3", "SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06", ambient_co2)

add_ratio(csv_file, "CO2 (smartGAS) / ppm_smooth_9_3", "SO2 / ppm_smooth_9_3", ambient_co2)
add_ratio_error(csv_file, "CO2 (smartGAS) / ppm_smooth_9_3", "CO2 (smartGAS) / ppm_smooth_9_3_staticerror_0.075_2.12",
                "SO2 / ppm_smooth_9_3", "SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06", ambient_co2)

add_ratio(csv_file, "CO2 (smartGAS) / ppm_smooth_9_3", "SO2 / ppm_smooth_9_3_rt_corrected_8", ambient_co2)
add_ratio_error(csv_file, "CO2 (smartGAS) / ppm_smooth_9_3", "CO2 (smartGAS) / ppm_smooth_9_3_staticerror_0.075_2.12",
                "SO2 / ppm_smooth_9_3_rt_corrected_8", "SO2 / ppm_smooth_9_3_staticerror_0.0323_0.06_with_complete_rt_error", ambient_co2)



