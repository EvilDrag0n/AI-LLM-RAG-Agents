"""
知识库上传服务
基于streamlit
从国内清华安装
pip install streamlit -i https://pypi.tuna.tsinghua.edu.cn/simple

"""

import streamlit as st

st.title("知识库更新")

upload_file = st.file_uploader(
    label="请上传TXT文件",
    type=["txt"],  # 上传文件类型
    accept_multiple_files=False,  # 不支持多文件上传
    max_upload_size=1
)

if upload_file is not None:
    file_name = upload_file.name
    file_type = upload_file.type
    file_size = upload_file.size / 1024

    st.subheader(f"文件名：{file_name}")
    st.write(f"文件类型：{file_type}")
    st.write(f"文件大小：{file_size:.2f} KB")

    file_context = upload_file.getvalue().decode("utf-8")
    st.write("内容")
    st.write(file_context)