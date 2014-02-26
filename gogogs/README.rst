=========
gogogs.py
=========

ガソリンの平均価格を gogo.gs から取得して munin にてグラフにする
----------------------------------------------------------------
Wildcard munin plugin to monitor price gasoline(petrol) and diesel oil in Japan by http://gogo.gs



.. image:: https://github.com/tinbotu/munin-plugins-misc/raw/master/gogogs/gogogs_13-month.png

.. image:: https://github.com/tinbotu/munin-plugins-misc/raw/master/gogogs/gogogs_13-year.png

- 赤: レギュラー
- 黄: ハイオク(プレミアム)
- 緑: 軽油
- 青: 灯油


使いかた
--------

1. どこかに gogogs.py を置く
2. munin/plugins/gogogs_13 とかの名前で symlink する

   名前の例

   ::

        gogogs_13      レギュラーとハイオクと軽油と灯油 東京都
        gogogs_pr_13   レギュラーとハイオク 東京都
        gogogs_r_40    レギュラー 福岡県
        gogogs_k       灯油 全国
        gogogs_        レギュラーとハイオクと軽油と灯油 全国


    r: レギュラー
    p: ハイオク
    d: 軽油
    k: 灯油

    0: 全国
    1: 北海道
    2: 青森県
    3: 岩手県
    4: 宮城県
    5: 秋田県
    6: 山形県
    7: 福島県
    8: 茨城県
    9: 栃木県
    10: 群馬県
    11: 埼玉県
    12: 千葉県
    13: 東京都
    14: 神奈川県
    15: 新潟県
    16: 富山県
    17: 石川県
    18: 福井県
    19: 山梨県
    20: 長野県
    21: 岐阜県
    22: 静岡県
    23: 愛知県
    24: 三重県
    25: 滋賀県
    26: 京都府
    27: 大阪府
    28: 兵庫県
    29: 奈良県
    30: 和歌山県
    31: 鳥取県
    32: 島根県
    33: 岡山県
    34: 広島県
    35: 山口県
    36: 徳島県
    37: 香川県
    38: 愛媛県
    39: 高知県
    40: 福岡県
    41: 佐賀県
    42: 長崎県
    43: 熊本県
    44: 大分県
    45: 宮崎県
    46: 鹿児島県
    47: 沖縄県

----
BUGS
----

- gogo.gs のブログパーツと同じ所を見に行っています


----
NOTE
----

- この勝手プラグインについて gogo.gs へ問い合わせはやめてください

- gogo.gs さん API 申請再開をお待ちしております


--------
SEE ALSO
--------

    `gogo.gs
    <http://gogo.gs/>`_

-------
History
-------

