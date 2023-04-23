import pandas as pd
from sklearn.linear_model import LinearRegression

data = pd.read_csv(r'C:\Users\harry\OneDrive\桌面\Summary.csv')
# print(data.columns)

print(data['10/2022'])
company_market = []  # 為各因子創建空白list準備塞進資料
company_HML = []
company_SMB = []
company_ESG = []
for col in data.columns:  # 利用for迴圈讀取資料，從data的col開始
    if col == 'Unnamed: 0' or col == '10/2021':continue # 如果col往下讀遇到na值，或是日期(因為資料的排版)，就執行下一個迴圈
    company_market.append(float(data[col][0]))  # 第一個中括號=哪一欄  第二個中括號 = 那欄第幾個
    company_HML.append(float(data[col][1]))
    company_SMB.append(float(data[col][2]))
    company_ESG.append(float(data[col][3]))

factors = [company_market, company_HML, company_SMB, company_ESG]
company = []
names = []
for num in range(7, 37):
    tmp = []
    if num == 22: continue
    names.append(data['Unnamed: 0'][num])
    for col in data.columns:
        if col =='Unnamed: 0' or col == '10/2021':continue
        tmp.append(float(data[col][num]))   # 把欄的資料輸入到列表裡 num剛好代表整個row
    # print(tmp)
    company.append(tmp)
print(company[0])
print(len(company), len(company[0]))

model = LinearRegression()
print(factors[0])
print(company[0])
# model.fit(np.array(factors[0]).reshape(-1,1), company[0])
# model.fit(np.(factors[0:5]), company[0])
data = {'factor':company_market, 'hml':company_HML, 'smb':company_SMB,'esg':company_ESG} #創建一個資料集放因子
data = pd.DataFrame(data)

inter = []
x1 = []
x2 = []
x3 = []
x4 = []
x5 = []
for i in range(30):
    if i == 29:  # 晉宏那家公司只跑四個月的資料
        tmp = {'factor': company_market[:4], 'hml': company_HML[:4], 'smb': company_SMB[:4], 'esg': company_ESG[:4]}
        tmp = pd.DataFrame(tmp)
        model.fit(tmp, company[i][:4])
        inter.append(model.intercept_)
        x1.append(model.coef_[0])
        x2.append(model.coef_[1])
        x3.append(model.coef_[2])
        x4.append(model.coef_[3])
        x5.append(model.score(tmp, company[i][:4]))
    else:
        model.fit(data , company[i])                                                # 後面每間不同公司報酬率(y) 對因子資料集跑回歸
        inter.append(model.intercept_)
        x1.append(model.coef_[0])
        x2.append(model.coef_[1])
        x3.append(model.coef_[2])
        x4.append(model.coef_[3])
        x5.append(model.score(data, company[i]))
    # print(model.intercept_, model.coef_)
    # 新開一個資料及存進係數的資料
coefficient_table = pd.DataFrame({'intercept': inter, 'Market': x1, 'HML': x2, 'SMB': x3, 'ESG': x4, 'R square': x5}, index=names)

    # 將df輸出成一個csv檔
coefficient_table.to_csv(r'C:\Users\harry\OneDrive\桌面\Regression.csv', encoding='utf_8_sig')

