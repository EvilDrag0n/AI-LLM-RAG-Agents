import numpy as np
"""

计算两个向量的余弦相似度（衡量方向相似性，剔除长度影响）
参数：
    vec_a(np.array):向量A
    vec_b (np.array)：向量B
返回：
    float：余弦相似度结果（范围[-1,1]，越接近1方向越一致）
公式：
    cos_sim = (vec_a · vec_b) / (||vec_al|| × ||vec_b||)
拆解：
    1. 点积: vec_a· vec_b =vec_a[o]xvec_b[o] +vec_a[1]×vec_b[1]+... + vec_a[n]xvec_b[n]
    2. 模长:||vec_al|| = ⩗(vec_a[0]² + vec_a[1]² +..+ vec_a[n]²）
    3. 模长: ||vec_b|| = ⩗(vec_b[o]² + vec_b[1]² + .. + vec_b[n]²）
A:[0.5,0.5]
B:[0.7,0.7]
C:[0.7,0.5]
D:[-0.6,-0.5]

"""


def get_dot(vec_a, vec_b):
    """计算两个向量的点积，2个向量同纬度数字之和"""
    if len(vec_a) != len(vec_b):
        raise ValueError("两个向量必须维度相同")
    sum_dot = 0
    for a, b in zip(vec_a, vec_b):
        sum_dot += a * b

    return sum_dot


def get_norm(vec):
    """计算向量的模长"""
    norm = 0
    for point in vec:
        norm += point * point
    return np.sqrt(norm)


def cos_sim(vec_a, vec_b):
    cos_sim = get_dot(vec_a, vec_b) / (get_norm(vec_a) * get_norm(vec_b))
    # print(cos_sim)
    return cos_sim


if __name__ == '__main__':
    vec_a = [0.5, 0.5]
    vec_b = [0.7, 0.7]
    vec_c = [0.7, 0.5]
    vec_d = [-0.6, -0.5]
    print(cos_sim(vec_a, vec_b))
    print(cos_sim(vec_a, vec_c))
    print(cos_sim(vec_a, vec_d))
    print(cos_sim(vec_c, vec_d))
