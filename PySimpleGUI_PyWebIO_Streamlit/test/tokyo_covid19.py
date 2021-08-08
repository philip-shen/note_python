
url = 'https://raw.githubusercontent.com/tokyo-metropolitan-gov/covid19/development/data/daily_positive_detail.json'
df_covid = get_covid_df(url)

diagnosed_date_list = df_covid['diagnosed_date'].values
str_maxdate = diagnosed_date_list[len(diagnosed_date_list)-1]
mindate = datetime.datetime.strptime(diagnosed_date_list[0], '%Y-%m-%d')
maxdate = datetime.datetime.strptime(str_maxdate, '%Y-%m-%d')

selected_date = st.sidebar.date_input(
    "表示したい期間を入力してください",
    [mindate, maxdate],
    min_value=mindate,
    max_value=maxdate
)

str_startdate = selected_date[0].strftime('%Y-%m-%d')
str_enddate = selected_date[1].strftime(
    '%Y-%m-%d') if len(selected_date) == 2 else str_maxdate

"""
# 東京都のCOVID-19感染者数
東京都 新型コロナウイルス感染症対策サイトの[Github](https://github.com/tokyo-metropolitan-gov/covid19)からデータを取得
"""

df_selected = df_covid.query(
    f'"{str_startdate}" <= diagnosed_date <= "{str_enddate}"')
st.write(df_selected)


"""
# 日毎の感染者数
"""


x = [
    datetime.datetime.strptime(diagnosed_date, '%Y-%m-%d')
    for diagnosed_date in df_selected['diagnosed_date'].values
]
y_count = df_selected['count'].values

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y_count)

wac_shown = st.sidebar.checkbox('週毎の平均感染者数も表示する')
if wac_shown:
    y_weekly_average_count = df_selected['weekly_average_count'].values
    ax.plot(x, y_weekly_average_count)

xfmt = mdates.DateFormatter('%m/%d')
xloc = mdates.DayLocator(interval=20)

ax.xaxis.set_major_locator(xloc)
ax.xaxis.set_major_formatter(xfmt)
st.write(fig)
