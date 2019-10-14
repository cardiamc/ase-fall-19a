from flakon import JsonBlueprint
from flask import Flask, request, jsonify
import numpy as np

calc = JsonBlueprint('calc', __name__)

'''
Compute the sum
endpoint: http://127.0.0.1:5000/calc/sum?m=_&n=_
'''
@calc.route('/calc/sum', methods=['GET'])
def sum():
    m = int(request.args.get('m'))
    n = int(request.args.get('n'))

    result = compute_sum(m,n)

    return jsonify({'result':str(result)})

'''
Compute the difference
endpoint: http://127.0.0.1:5000/calc/diff?m=_&n=_
'''
@calc.route('/calc/diff', methods=['GET'])
def diff():
    m = int(request.args.get('m'))
    n = int(request.args.get('n'))

    result = compute_sum(m,-1*n)

    return jsonify({'result':str(result)})

@calc.route('/calc/prod', methods=['GET'])
def prod():
    m = int(request.args.get('m'))
    n = int(request.args.get('n'))

    sum_value=0
    m_sign = np.sign(m)
    n_sign = np.sign(n)
    for x in range(abs(n)):
        sum_value += abs(m)
    result = sum_value * m_sign * n_sign

    return jsonify({'result':str(result)})

@calc.route('/calc/div',methods=['GET'])
def div():
    m = int(request.args.get('m'))
    n = int(request.args.get('n'))

    to_sub = abs(n)
    start_val = abs(m)

    m_sign = np.sign(m)
    n_sign = np.sign(n)

    result = 0

    while start_val > 0:
        start_val -= to_sub
        result += 1
    
    if start_val < 0:
        result -= 1
    
    result = result * n_sign * m_sign

    return jsonify({'result':str(result)})


def compute_sum(m, n):
    result = m
    if n < 0:
        for i in range(abs(n)):
            result -= 1
    else:
        for i in range(n):
            result += 1
    return result
