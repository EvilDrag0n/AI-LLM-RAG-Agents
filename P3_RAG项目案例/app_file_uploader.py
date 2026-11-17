"""
知识库上传服务
基于streamlit
从国内清华安装
pip install streamlit -i https://pypi.tuna.tsinghua.edu.cn/simple

"""
import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

st.title("知识库更新")

upload_file = st.file_uploader(
    label="请上传TXT文件",
    type=["txt"],  # 上传文件类型
    accept_multiple_files=False,  # 不支持多文件上传
    max_upload_size=1
)


if "knowledgeService" not in st.session_state:
    st.session_state["knowledgeService"] = KnowledgeBaseService()


if upload_file is not None:
    file_name = upload_file.name
    file_type = upload_file.type
    file_size = upload_file.size / 1024

    file_context = upload_file.getvalue().decode("utf-8")

    with st.spinner("内容上传中。。。。。"):
        time.sleep(2)   #模拟大文件
        result = st.session_state["knowledgeService"].upload_by_str(file_context, file_name)
        if result["isSuccess"]:
            st.success(result)
        else:
            st.warning(result)

    st.subheader(f"文件名：{file_name}")
    st.write(f"文件类型：{file_type}")
    st.write(f"文件大小：{file_size:.2f} KB")
    st.write("内容")
    st.write(file_context)