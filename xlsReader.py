import xlrd
# xlrd模块读取xls文件
# 调用read方法返回以姓和名为key的字典组成的列表
def read():
    data = xlrd.open_workbook('1.xls')
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    ctype = 1
    xf = 0
    Namelist=[]

    for i in range(72,nrows):
        Namedict={}
        FirstName=table.cell(i,2).value
        LastName=table.cell(i,3).value
        mail=table.cell(i,6).value
        Namedict["Firstname"]=FirstName
        Namedict["Lastname"]=LastName
        Namedict["mail"]=mail
        #print("FirstName:"+FirstName+"  LastName:"+LastName)
        # table.put_cell(i, 9, ctype, i, xf)
        # print(table.cell(i,9))
        # print(table.cell(i,9).value)
        Namelist.append(Namedict)
    return Namelist
if __name__ == '__main__':
    Namelist=read()
    print(Namelist)
    print(len(Namelist))
