# coding=UTF-8
import csv, json, operator

trans = {
    '土耳其共和國': 792,
    '大陸地區': 156,
    '大韓民國(南韓)': 410,
    '丹麥王國': 208,
    '厄瓜多共和國': 218,
    '巴西聯邦共和國': 76,
    '巴拿馬共和國': 591,
    '日本': 392,
    '比利時王國': 56,
    '牙買加': 388,
    '以色列': 376,
    '加拿大': 124,
    '卡達': 634,
    '史瓦濟蘭王國': 748,
    '甘比亞共和國': 270,
    '白俄羅斯共和國': 112,
    '立陶宛共和國': 440,
    '伊朗伊斯蘭共和國': 364,
    '冰島共和國': 352,
    '列支敦斯登侯國': 438,
    '匈牙利共和國': 348,
    '印度尼西亞共和國': 360,
    '印度共和國': 356,
    '西班牙王國': 724,
    '克羅埃西亞共和國': 191,
    '希臘共和國': 300,
    '汶萊和平之國': 96,
    '沙烏地阿拉伯王國': 682,
    '貝里斯': 84,
    '邦交國吉里巴斯共和國': 296,
    '邦交國帛琉共和國': 585,
    '邦交國索羅門群島': 90,
    '拉脫維亞共和國': 428,
    '法國': 250,
    '波蘭共和國': 616,
    '芬蘭共和國': 246,
    '阿曼王國': 512,
    '阿富汗伊斯蘭國': 4,
    '俄羅斯聯邦': 643,
    '南非共和國': 710,
    '柬埔寨王國': 116,
    '科威特': 414,
    '科索沃共和國': -2,
    '突尼西亞共和國': 788,
    '約旦哈什米王國': 400,
    '美國': 840,
    '英國': 826,
    '香港': 344,
    '哥倫比亞共和國': 170,
    '哥斯大黎加共和國': 188,
    '埃及阿拉伯共和國': 818,
    '挪威王國': 578,
    '格瑞那達': 308,
    '泰王國(泰國)': 764,
    '紐西蘭': 554,
    '馬來西亞': 458,
    '馬爾他共和國': 470,
    '捷克共和國': 203,
    '荷蘭王國': 528,
    '莫三比克共和國': 508,
    '斐濟群島共和國': 242,
    '斯里蘭卡民主社會主義共和國': 144,
    '斯洛伐克共和國': 703,
    '斯洛維尼亞共和國': 705,
    '智利': 152,
    '朝鮮民主主義人民共和國(北韓)': 408,
    '菲律賓共和國': 608,
    '越南社會主義共和國': 704,
    '塞席爾共和國': 690,
    '奧地利共和國': 40,
    '愛沙尼亞共和國': 233,
    '愛爾蘭共和國': 372,
    '新加坡共和國': 702,
    '瑞士聯邦': 756,
    '瑞典王國': 752,
    '義大利共和國': 380,
    '聖多美普林西比民主共和國': 678,
    '葡萄牙共和國': 620,
    '蒙古國': 496,
    '墨西哥合眾國': 484,
    '德意志聯邦共和國': 276,
    '摩洛哥王國': 504,
    '緬甸聯邦共和國': 104,
    '澳大利亞': 36,
    '澳門': 446,
    '盧森堡大公國': 442,
    '羅馬尼亞': 642
}

out = {}

reader = csv.reader(open('exchange.csv', 'r', encoding='big5-hkscs'))
for row in reader:
    if row[7] in trans:
        country_id = trans[row[7]]
        school = row[9].upper()
        if country_id in out:
            out[country_id]['number'] += 1
            if school in out[country_id]['school']:
                out[country_id]['school'][school] += 1
            else:
                out[country_id]['school'][school] = 1
        else:
            out[country_id] = {
                'number': 1,
                'school': {school: 1}
            }

for country in out:
    school = out[country]['school']
    out[country]['school'] = sorted(school.items(), key=operator.itemgetter(1), reverse=True)

with open('out.json', 'w') as outfile:
    json.dump(out, outfile)
