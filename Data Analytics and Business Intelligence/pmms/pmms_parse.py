# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 18:25:11 2019

@author: Wu
"""

from datetime import datetime, date
import json
import requests
import xlwings as xw


def get_dic(rng, col1, col2):
    return dict(zip(rng.columns(col1).value, rng.columns(col2).value))

def fetch_block(ftype, pos, offset_idx=0):
    '''
    fetch tabular-like range. PARTIAL blank cell tolerance
    `fetch_type`: fetching mode. `string`
    `pos`: upper-left corner of the target range. `range` object
    `offset_idx`: Additional number of columns/rows need to fetch
                  used by fetch_type of "col_offset"/"col_offset".
    return: `range` object
    '''
    ws = pos.sheet
    if ftype == 'col_block':
        end = pos.end('down').end('right')
    elif ftype == 'row_block':
        end = pos.end('right').end('down')
    elif ftype == 'col_offset':
        end = ws.range(pos.end('down').row, pos.column + offset_idx)
    elif ftype == 'row_offset':
        end = ws.range(pos.row + offset_idx, pos.end('right').column)
    return ws.range(pos, end)


def main(config_path, master_path, txdate, dump_rng):

    # prepa job setting
    with open(config_path,'rb') as pfile:
        master_format=json.load(pfile)
        
    # downdload file
    pmms_file_path = 'PMMS_history.xls'
    with open(pmms_file_path,'wb') as pmfile:
        rep = requests.get(master_format['PMMS_URI'])
        pmfile.write(rep.content)

    # read history file and fetch the correspondent weekly data
    pmms_wb = xw.Book(pmms_file_path)
    pmms = pmms_wb.sheets(1)
    txdate = datetime.strptime(txdate, '%Y%m%d')
    for i in range(pmms.used_range.rows.count,0,-1):
        tmp_date = pmms.range(i,1).value
        if isinstance(tmp_date, date) and tmp_date <= txdate:
            break
    data = pmms.used_range.rows(i).value
    pmms_wb.close()

    # write back to the master excel, exit
    wb = xw.Book(master_path)
    name, rng = dump_rng.split('!')
    wb.sheets(name).range(rng).value = data[:8]
    

import sys
try:
    # directly get txdate, r_pmms through cmd arg
    main(*sys.argv[1:])
except Exception as e:
    print(e)
    end = input('Press enter to close')
