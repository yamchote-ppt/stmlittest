import pandas as pd
from tabulate import tabulate
import streamlit as st
import numpy as np

st.sidebar.title('กี่ปีเงินหมด')

def time_to_exhaust(growth_r, withdraw_r):
    """
    คำนวณว่าใช้เวลากี่ปีเงินต้นจะหมด ถ้าถอนเงินมาใช้เท่าๆกันทุกปี

    growth_r = อัตราการเติบโตของเงินต้นที่หักเงินเฟ้อแล้ว หน่วยเป็น %
    (เช่นถ้าลงทุนได้ 5% ต่อปีและเงินเฟ้อ = 3% ต่อปี, growth_r = 5 - 3 = 2)

    เงินที่ถอนออกมาเท่าๆกันทุกปี = เงินต้นปีแรก * withdraw_r/100
    """
    years = 0 #จำนวนปี
    asset = 1.0 #เงินต้น
    withdraw = asset * withdraw_r/100 #เงินที่ถอนออกมาเท่าๆกันทุกปี
    asset_change = 0
    while asset > 0: #เราจะวนไปเรื่อยๆจนเงินหมด
        new_asset = asset - withdraw #ถอนเงินมาใช้ต้นปี เหลือเงิน = new_asset
        years += 1 #เวลาเพิ่มอีกหนึ่งปี
        new_asset = new_asset * (1 + growth_r/100) #เงินเติบโตด้วยอัตรา growth_r เปอร์เซ็นต์
        asset_change = new_asset - asset #คำนวณว่าเงินเปลี่ยนไปเท่าไร
        #print(year, asset)
        if asset_change > 0: #ถ้าเงินระหว่างปีเพิ่ม เงินจะไม่มีวันหมด
            return 'inf'
        asset = new_asset #เงินที่เหลือสำหรับปีต่อไป
    return years #คำนวณปีที่เงินหมด

def create_table(f, a_range, b_range):
    # Create a table to store the results
    results = []

    # Nested loop to iterate through a and b
    for a in a_range:
        row = []
        for b in b_range:
            result = f(a, b)
            row.append(result)
        results.append(row)

    # Convert the list to a DataFrame for better representation
    df = pd.DataFrame(results, columns=[f'{b}' for b in b_range], index=[f'{a}' for a in a_range])
    
    # Pretty print the DataFrame
    def color_survived(val):
        color = 'rgb(0, 254,0)' if val=='inf' else 'red' if val<10 else 'yellow'
        return f'background-color: {color}'
    
    st.table(df.style.applymap(color_survived))
    # st.write(tabulate(df, headers='keys', tablefmt='pretty'))

mina,maxa = st.sidebar.slider('Select a range of g',-20, 20, (-4, 10),step=1)
minb,maxb = st.sidebar.slider('Select a range of w',0, 40, (0, 15),step=1)


create_table(time_to_exhaust, range(mina,maxa + 1), range(maxb, minb, -1))