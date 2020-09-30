import csv
import os
import time

File_name = '2014_fut'



if __name__ == '__main__':
    the_all_data = ""
    File_name_list = os.listdir(os.path.join(os.getcwd(),"csv_to_txt"))
    for File_name in File_name_list:
        File_name = File_name.replace(".csv","")
        result_dict = {}
        # [time:1600963200000, tradeDate:1600963200000, open:12168.00000, high:12234.00000, low:12157.00000, close:12206.00000, volume:9865, millionAmount:0.00]
        with open('csv_to_txt\\'+File_name+'.csv', newline='') as csvfile:
            rows = csv.reader(csvfile)
            for index,row in enumerate(rows):
                if index > 0 :
                    temp_date_list = row[0].split("/")
                    temp_date=""
                    for aa in temp_date_list:
                        if int(aa)<10:
                            aa = '0'+aa
                        temp_date+=aa
                    row[0] = temp_date

                    if row[0] in result_dict:
                        pass
                    else:
                        # 只看月契約
                        if int(temp_date[4:6]) == 12:
                            nxt_month = str(int(temp_date[0:4])+1)+"01"
                        else:
                            nxt_month = str(int(temp_date[:6]) + 1)

                        if temp_date[:6] == row[2] and row[1] == "TX" and not "/" in row[2]:
                            temp_list = []
                            timeArray = time.strptime(row[0], "%Y%m%d")
                            # 轉換為時間戳:
                            timeStamp = str(int(time.mktime(timeArray)))+"000"
                            temp_list.append("time:"+timeStamp)
                            temp_list.append("tradeDate:"+timeStamp)
                            temp_list.append("open:"+row[3])
                            temp_list.append("high:"+row[4])
                            temp_list.append("low:"+row[5])
                            temp_list.append("close:"+row[6])
                            temp_list.append("volume:"+row[9])
                            result_dict[row[0]] = temp_list
                        elif nxt_month == row[2] and row[1] == "TX" and not "/" in row[2]:
                            temp_list = []
                            timeArray = time.strptime(row[0], "%Y%m%d")
                            # 轉換為時間戳:
                            timeStamp = str(int(time.mktime(timeArray))) + "000"
                            temp_list.append("time:" + timeStamp)
                            temp_list.append("tradeDate:" + timeStamp)
                            temp_list.append("open:" + row[3])
                            temp_list.append("high:" + row[4])
                            temp_list.append("low:" + row[5])
                            temp_list.append("close:" + row[6])
                            temp_list.append("volume:" + row[9])
                            result_dict[row[0]] = temp_list
                # else:
                #     print(row)
        final_str = ""
        for key, value in result_dict.items():
            print(key + ':' + str(value))
            final_str += str(value)+'\r'
            the_all_data += str(value)+'\r'
        with open('txt\\'+File_name+'.txt', 'w') as txt:
            txt.write(final_str)

    with open('txt\\' + "all_data" + '.txt', 'w') as txt:
        txt.write(the_all_data)