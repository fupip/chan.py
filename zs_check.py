from Common.CEnum import AUTYPE, DATA_SRC, KL_TYPE
from DataAPI.csvAPI import CSV_API
from Chan import CChan
from ChanConfig import CChanConfig

config = CChanConfig({  
        "bi_strict": True,
        "trigger_step": False,
        "skip_step": 0,
        "divergence_rate": float("inf"),
        "bsp2_follow_1": False,
        "bsp3_follow_1": False,
        "min_zs_cnt": 0,
        "bs1_peak": False,
        "macd_algo": "peak",
        "bs_type": '1,2,3a,1p,2s,3b',
        "print_warning": True,
        "zs_algo": "normal",
    })

def read_stock_list():
	stock_list_file = r"C:\国金证券QMT交易端\bin.x64\stock_list.txt"
	stock_list = []
	with open(stock_list_file,'r') as f:
		for line in f:
			stock_list.append(line.strip())
	return stock_list	

def check_zs(stock_code,config):
    # code = "002714.SZ"
    begin_time = "2024-09-01"
    end_time = None
    data_src = DATA_SRC.CSV
    lv_list = [KL_TYPE.K_5M]
    # csv_api = CSV_API(code, KL_TYPE.K_5M, begin_time, "", AUTYPE.QFQ)
    chan = CChan(
        code=stock_code,
        begin_time=begin_time,
        end_time=end_time,
        data_src=data_src,
        lv_list=lv_list,     
        config=config,
        autype=AUTYPE.QFQ,    # 前复权
    )
    if len(chan[KL_TYPE.K_5M]) >0 and len(chan[KL_TYPE.K_5M].segzs_list) >0:
        seg_zs = chan[KL_TYPE.K_5M].segzs_list[-1]
        return seg_zs.high,seg_zs.low
    
    return None,None

if __name__ == "__main__":
    stock_list = read_stock_list()
    zs_check_file = r"C:\国金证券QMT交易端\bin.x64\zs_check.txt"
    with open(zs_check_file,'w+') as f:
        for stock_code in stock_list:
            zs_high,zs_low = check_zs(stock_code,config)
            zs_json = {"stock_code":stock_code,"zs_high":zs_high,"zs_low":zs_low}
            f.write(json.dumps(zs_json))
            f.write("\n")



