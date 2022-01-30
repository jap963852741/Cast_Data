import csv
import os
import time

File_name = '2014_fut'


def update_date():
    temp_date_list = row[0].split("/")

    year_str = temp_date_list[0]
    month_str = change_date_format(temp_date_list[1])
    day_str = change_date_format(temp_date_list[2])

    row[0] = year_str + month_str + day_str


def change_date_format(temp_date):
    if temp_date == '\x1a':
        temp_date = str(ord(temp_date))
    if int(temp_date) < 10:
        temp_date = '0' + temp_date
    return temp_date


def get_next_month(time_str):
    if int(time_str[4:6]) == 12:
        nxt_month = str(int(time_str[0:4]) + 1) + "01"
    else:
        nxt_month = str(int(time_str[:6]) + 1)
    return nxt_month


if __name__ == '__main__':
    the_all_data = ""
    File_name_list = os.listdir(os.path.join(os.getcwd(), "csv_to_txt"))
    for File_name in File_name_list:
        File_name = File_name.replace(".csv", "")
        result_dict = {}
        print('begin to cast ' + os.path.join('csv_to_txt', File_name + '.csv'))
        # [time:1600963200000, tradeDate:1600963200000, open:12168.00000, high:12234.00000, low:12157.00000,
        # close:12206.00000, volume:9865, millionAmount:0.00]

        # 1999/1/5,TX,199901,6430,6430,6074,6120,-411,-6.29%,5058,6120,6441,-,-,7640,6074

        with open(os.path.join('csv_to_txt', File_name + '.csv')) as csvfile:
            rows = csv.reader(csvfile)
            for index, row in enumerate(rows):
                if index > 0:
                    update_date()

                    my_date = row[0]
                    if row[0] in result_dict:
                        pass
                    elif len(my_date) > 3:
                        # just look moth
                        if my_date[:6] == row[2] and row[1] == "TX" and not "/" in row[2]:
                            temp_list = []
                            timeArray = time.strptime(row[0], "%Y%m%d")
                            # change to time stamp
                            timeStamp = str(int(time.mktime(timeArray))) + "000"
                            temp_list.append("time:" + timeStamp)
                            temp_list.append("tradeDate:" + timeStamp)
                            temp_list.append("open:" + row[3])
                            temp_list.append("high:" + row[4])
                            temp_list.append("low:" + row[5])
                            temp_list.append("close:" + row[6])
                            temp_list.append("volume:" + row[9])
                            result_dict[row[0]] = temp_list
                        elif get_next_month(my_date) == row[2] and row[1] == "TX" and not "/" in row[2]:
                            temp_list = []
                            timeArray = time.strptime(row[0], "%Y%m%d")
                            # change to time stamp
                            timeStamp = str(int(time.mktime(timeArray))) + "000"
                            temp_list.append("time:" + timeStamp)
                            temp_list.append("tradeDate:" + timeStamp)
                            temp_list.append("open:" + row[3])
                            temp_list.append("high:" + row[4])
                            temp_list.append("low:" + row[5])
                            temp_list.append("close:" + row[6])
                            temp_list.append("volume:" + row[9])
                            result_dict[row[0]] = temp_list

        final_str = ""
        for key, value in result_dict.items():
            # print(key + ':' + str(value))
            final_str += str(value) + '\r'
            the_all_data += str(value) + '\r'
        with open(os.path.join('txt', File_name + '.txt'), 'w') as txt:
            txt.write(final_str)

    with open(os.path.join('txt', "all_data" + '.txt'), 'w') as txt:
        txt.write(the_all_data)
