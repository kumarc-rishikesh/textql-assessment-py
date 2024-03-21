from condition_eval import Result, conds_operator, res_operator, convert_to_postfix, eval_data

def run_where(inferred_schema, data_c,tq):
    # print(inferred_schema)
    if len(tq['conditions'])==0:
        return Result(data_c)
    elif len(tq['conditions'])==1:
        cond=tq['conditions'][0]
        op, rej = conds_operator(data_c,cond[1],cond[0],cond[2],inferred_schema)
        return Result(op)
    tokens=convert_to_postfix(tq['conditions'])
    mark = {"AND","OR"}
    stk = []
    f=0
    for x in tokens:
        if isinstance(x,str):
            if x in mark:
                b = stk.pop()
                a = stk.pop()

                res = eval_data(inferred_schema, data_c.copy(), x.upper() , a, b)
                stk.append(res)
                
        else:
            stk.append(x)
    return stk.pop()

def run_select(where_results,tq):
    op_arr=[]
    select_fields=tq['columns']
    if select_fields[0] == "*":
        return where_results
    for row in where_results.data:
        op_json={}
        for field in select_fields:
            op_json[field] = row[field]
        op_arr.append(op_json)
    op = Result(op_arr)
    return(op)

def run_limit(select_results,tq):
    op_arr=[]
    limit=tq['limit']
    if limit==0:
        return select_results
    else:
        if len(select_results.data)<=limit:
            return select_results
        else:
            data = select_results.data
            i=0
            while i<limit:
                op_arr.append(data[i])
                i+=1
    op=Result(op_arr)
    return Result

def get_query_results( data, query, inf_schema ):
    #Following applicable SQL order of execution FWGHSOL : WHERE->SELECT->LIMIT 
    # print(data, query, inf_schema)
    tq = query
    data_copy = data.copy()
    # print(data_copy)
    where_results = run_where(inf_schema, data_copy, tq)
    select_results = run_select(where_results, tq)
    limit_results = run_limit(select_results, tq)

    return limit_results
