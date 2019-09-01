
import re
import math


def read_file(filename):
    ret = []
    with open(filename, 'r') as f:
        for l in f.readlines():
            ret.append(l.strip())
    return ret

class Beats():
    def __init__(me, timing, chart):
        me.timing = timing
        me.charts = []
        if chart != '': 
            me.charts.append(chart)
    def same_time(me, other):
        return abs(me.timing - other.timing) < 1e-6
    def add_beat(me, other):
        for c in other.charts:
            me.charts.append(c)
    def chart(me):
        return '/'.join(me.charts)


"""
Format: `{{"{8},,,,,,{4}," "{6},,,,,," "{3},,,"}}`
"""
def get_beats(s):
    # print(f'get_beats, s = {s}')
    aa = re.split("(\{\d+.?\d*\})", s)
    beats = []
    timing = 0
    for i in range(1, len(aa), 2):
        beat = float(aa[i][1:-1])
        this_time = 1 / beat
        i = i + 1
        aaa = aa[i].split(',')[:-1]
        for j in aaa:
            beats.append(Beats(timing, j))
            timing += this_time
    return beats, timing

def unique_beats(beats):
    result = []
    for b in beats:
        if len(result) == 0 or not result[-1].same_time(b):
            result.append(b)
        else:
            result[-1].add_beat(b)
    return result


def trans_part(s):
    # print(f'trans_part, s = {s}')
    sz = len(s)
    L, R = 0, 0
    all_beats = []
    while R < sz:
        while R < sz and s[R] != '"': R = R + 1
        if R >= sz: break
        L, R = R, R + 1
        while s[R] != '"': R = R + 1
        beats, final_timing = get_beats(s[L+1:R])
        for b in beats: all_beats.append(b)
        R = R + 1
    all_beats.sort(key=lambda x: x.timing)
    all_beats = unique_beats(all_beats)
    result = ''
    for i in range(len(all_beats)):
        now_timing = all_beats[i].timing
        next_timing = final_timing if i == len(all_beats) - 1 else all_beats[i + 1].timing
        result += '{' + str(round(1.0/(next_timing - now_timing), 4)) + '}' + all_beats[i].chart() + ','
    return result
        

def trans_line(s):
    # print(f'trans_line, s = {s}')
    sz = len(s)
    L, R = 0, 0
    while R < sz:
        while R + 1 < sz and s[R:R+2] != '{{': R = R + 1
        if R + 1 >= sz: break
        L = R
        R = L + 1
        while s[R:R+2] != '}}': R = R + 1
        s = s[:L] + trans_part(s[L+2:R]) + s[R+2:]
    return s
        
    

def trans_full_file(full_chart, be_trans):
    sz = len(full_chart)
    i, j = 0, 0
    while j < sz:
        while j < sz and len(full_chart[j]) == 0 or full_chart[j][0] != '&': j = j + 1
        if j >= sz: break
        i, j = j, j + 1
        while j < sz and (len(full_chart[j]) == 0 or full_chart[j][0] != '&'): j = j + 1
        if full_chart[i][0:7] == f'&inote_' and full_chart[i][8] == '=':
            if full_chart[i][7] in be_trans:
                for k in range(i, j):
                    full_chart[k] = trans_line(full_chart[k])
    return full_chart

def write_to_new_file(chart, filename):
    with open(filename, 'w') as f:
        f.write('\n'.join(chart))

def main():
    # filename = input('請輸入要被轉換的檔名：').strip()
    filename = 'maidata.txt'
    full_chart = read_file(filename)
    be_trans = input('請輸入要被轉換的難度（例：2,3,7）：').strip().split(',')
    full_chart = trans_full_file(full_chart, be_trans)
    write_to_new_file(full_chart, 'translated_' + filename)

if __name__ == '__main__':
    main()
