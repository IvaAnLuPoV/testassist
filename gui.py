import streamlit as st
import pandas as pd
import unittest.mock as mock
from testassist import TestAssist, Choice, Range

st.set_page_config(page_title="TestAssist GUI")

st.title("🚀 testassist preview")
st.markdown("GUI preview of loaded tests")

st.sidebar.header("Settings")
seed = st.sidebar.number_input("Seed", value=42)
workers = st.sidebar.slider("Parallel workers", 1, 8, 4)

ta = TestAssist(seed=seed)

ta.begin_subtask()
ta.make_batch(6, {
        'testgen': 'demo/testgens/py_gen.py',
        'n': Choice([5, 10]),
        'm': Choice([2, 6, 12])
    })

if ta.task_container:
    df = pd.DataFrame(ta.task_container)

    # Опционално: Пренареждане на колоните за по-добра четимост
    # Преместваме subtask_id и testgen най-отпред
    cols = ['subtask_index', 'gen_file'] + [c for c in df.columns if c not in ['subtask_index', 'gen_file']]
    df = df[cols]

    st.dataframe(df, use_container_width=True) 
else:
    st.warning("Task container is currently empty.")

if st.button("Finalize"):
    try:
        with mock.patch('builtins.input', return_value='y'):
            with st.spinner("Generating tests."):
                ta.finalize(workers=workers)

        st.success("Generation finished!")
    except Exception as e:
        st.error(f"ERROR: {e}")