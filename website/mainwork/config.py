from website import basedir
data_dir = f'{basedir}/static/problem'
work_dir = f'{basedir}/static/work'
database=f"{basedir}/online_judge.db"#数据库db文件路径
auto_clean=False
result_sig = {
    0: "waiting",
    1: "AC",
    2: "TLE",
    3: "MLE",
    4: "WA",
    5: "RE",
    6: "OLE",
    7: "CE",
    8: "PE",
    11: "SE",
    12: "judging",
}
