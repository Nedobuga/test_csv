import csv
from tabulate import tabulate
import argparse
import operator
from statistics import mean


def splitter(value):
    operators = [ "=", "<=", ">=", "<", ">"]
    for op in operators:
        if op in value:
            col, val = value.split(op)
            return col, val, op
    raise ValueError("Invalid condition format")

def get_col_number(header, col_name):
    for i, name in enumerate(header):
        if name == col_name:
            return i
    raise ValueError(f"Column {col_name} not found in header")

ops_map = {
        "=": operator.eq,
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
    }        
def compare(value1, op, value2):
    if op not in ops_map:
        raise ValueError(f"Unsupported operator: {op}")
    try:
        value1 = float(value1)
        value2 = float(value2)
    except ValueError:
        pass
    return ops_map[op](value1, value2)


def get_filtred_data(data, header, filter_cortege):
    column_index = get_col_number(header, filter_cortege[0])
    filtred_data = []
    for row in data:
        if compare(row[column_index], filter_cortege[2], filter_cortege[1]):
            filtred_data.append(row)
    return filtred_data


        
agg_func = {
    "min": min,
    "max": max,
    "avg": mean
}
def aggregate(func_name, values):    
    if func_name not in agg_func:
        raise ValueError(f"Unsupported aggregate function: {func_name}")
    return agg_func[func_name](values)

def get_agg_data(data, header, agg_cortege):
    agg_col = []
    for row in data:
        agg_col.append(float(row[get_col_number(header, agg_cortege[0])]))
    resault = aggregate(agg_cortege[1], agg_col)
    return [[resault]]



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--file',
        type=str
    )

    parser.add_argument(
        '--where',
        type=str
    )
    parser.add_argument(
        '--aggregate',
        type=str
    )

    pars_name = parser.parse_args()


    with open(pars_name.file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        data = list(reader)

    if pars_name.where:
        filter_cortege = splitter(pars_name.where)
        data = get_filtred_data(data, header, filter_cortege)

    if pars_name.aggregate:
        agg_cortege = splitter(pars_name.aggregate)
        data = get_agg_data(data, header, agg_cortege)
        header = [agg_cortege[1]]
    print(tabulate(data, headers=header, tablefmt="grid"))
