import csv
import os
import time




if __name__ == '__main__':
    the_all_data = ""
    the_all_data_list = []
    File_name_list = os.listdir(os.path.join(os.getcwd(),"option_csv"))
    # File_name_list= ['2018_opt_01.csv']
    for File_name in File_name_list:
        File_name = File_name.replace(".csv","")
        result_dict = {}
        print(File_name)
        with open('option_csv\\'+File_name+'.csv', newline='') as csvfile:
            rows = csv.reader(csvfile)
            for index,row in enumerate(rows):
                if index > 0 :
                    temp_date_list = row[0].split("/")
                    temp_date=""
                    for aa in temp_date_list:
                        if int(aa)<10 and len(aa)<2:
                            aa = '0'+aa
                        temp_date+=aa
                    row[0] = temp_date

                    now_month = str(int(temp_date[:6]))
                    if int(temp_date[4:6]) == 12:
                        nxt_month = str(int(temp_date[0:4]) + 1) + "01"
                    else:
                        nxt_month = str(int(temp_date[:6]) + 1)
                    if row[10] == '-':
                        row[10] = '0';
                    if ' ' in row[2]:
                        row[2] = row[2].replace(" ", "")
                    if '.000' in row[3]:
                        row[3] = row[3].split('.')[0]


                    if row[0] in result_dict:
                        pass
                    elif len(row) > 17: ##篩掉夜盤
                        # print("row" + str(row))

                        if float(row[10]) > 1 and row[1] == 'TXO' and row[4] == '買權' and now_month in row[2] and row[17] == '一般':
                            temp_list = []
                            temp_list.append("Date:" + row[0])
                            temp_list.append("Maturity:" + row[2])
                            temp_list.append("Strike_price:" + row[3])
                            if row[4] == '買權':
                                temp_list.append("CallPut:call")
                            elif row[4] == '賣權':
                                temp_list.append("CallPut:put")
                            temp_list.append("close:" + row[10])
                            result_dict[row[0]+row[2]+row[3]] = temp_list
                        elif float(row[10]) > 1  and row[1] == 'TXO' and row[4] == '買權' and nxt_month in row[2] and row[17] == '一般':
                            temp_list = []
                            temp_list.append("Date:" + row[0])
                            temp_list.append("Maturity:" + row[2])
                            temp_list.append("Strike_price:" + row[3])
                            if row[4] == '買權':
                                temp_list.append("CallPut:call")
                            elif row[4] == '賣權':
                                temp_list.append("CallPut:put")

                            temp_list.append("close:" + row[10])
                            result_dict[row[0] + row[2] + row[3]] = temp_list

                    elif len(row) <= 17:
                        # print("row" + str(row))

                        if float(row[10]) > 1  and row[1] == 'TXO' and row[4] == '買權' and now_month in row[2] :
                            temp_list = []
                            temp_list.append("Date:" + row[0])
                            temp_list.append("Maturity:" + row[2])
                            temp_list.append("Strike_price:" + row[3])
                            if row[4] == '買權':
                                temp_list.append("CallPut:call")
                            elif row[4] == '賣權':
                                temp_list.append("CallPut:put")
                            temp_list.append("close:" + row[10])
                            result_dict[row[0] + row[2] + row[3]] = temp_list
                        elif float(row[10]) > 1 and row[1] == 'TXO' and row[4] == '買權' and nxt_month in row[2] :
                            temp_list = []
                            temp_list.append("Date:" + row[0])
                            temp_list.append("Maturity:" + row[2])
                            temp_list.append("Strike_price:" + row[3])
                            if row[4] == '買權':
                                temp_list.append("CallPut:call")
                            elif row[4] == '賣權':
                                temp_list.append("CallPut:put")

                            temp_list.append("close:" + row[10])
                            result_dict[row[0] + row[2] + row[3]] = temp_list
        final_str = ""
        for key, value in result_dict.items():
            final_str += str(value)+'\r'
            the_all_data_list.append(value)
        with open('option_txt\\'+File_name+'.txt', 'w') as txt:
            txt.write(final_str)



    Maturity_Date_Dict ={}
    for i in the_all_data_list:
        Date = i[0].replace('Date:','')
        Maturity = i[1].replace('Maturity:','')
        if Maturity in Maturity_Date_Dict:
            if not Date in Maturity_Date_Dict[Maturity]:
                Maturity_Date_Dict[Maturity][Date] = len(Maturity_Date_Dict[Maturity])+1
        else:
            Temp_Date_idx_Dict = {Date:1}
            Maturity_Date_Dict[Maturity] = Temp_Date_idx_Dict

    for key, value in Maturity_Date_Dict.items():
        Temp_Date_idx_Dict = value
        Temp_New_Date_idx_Dict = {}
        for s_key,s_value in Temp_Date_idx_Dict.items():
            Temp_New_Date_idx_Dict[s_key] = len(Temp_Date_idx_Dict) - s_value
        Maturity_Date_Dict[key] = Temp_New_Date_idx_Dict

    for i in the_all_data_list:
        Date = i[0].replace('Date:', '')
        Maturity = i[1].replace('Maturity:','')
        i.append('Day_To_Finish:'+str(Maturity_Date_Dict[Maturity][Date]))

    for i in the_all_data_list:
        the_all_data += str(i) + '\r'

    with open('option_txt\\' + "option_all_data" + '.txt', 'w') as txt:
        txt.write(the_all_data)