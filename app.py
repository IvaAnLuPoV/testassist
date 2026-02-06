import streamlit as st
import pandas as pd
from testassist import TestAssist

st.set_page_config(page_title="Test Generator GUI", page_icon="🧪")

st.title("🚀 Test Generator Preview")

st.sidebar.header("Settings")
seed = st.sidebar.number_input("Seed", value=1)
num_tests = st.sidebar.slider("Preview tests", 1, 50, 10)

ta = TestAssist(seed=seed)

ta.make_batch(num_tests, {'testgen': 'dummy.py', 'n': 100})

st.subheader("Preview of tests")

df = pd.DataFrame(ta.task_container) 

if not df.empty:
    st.dataframe(df, use_container_width=True)
    st.info(f"{len(df)} tests are ready for finalization.")
else:
    st.warning("No generated tests.")

if st.button("Finalize and save tests"):
    
    with st.spinner('Generating tests...'):
        ta.finalize()
    st.success("Files are succesfully generated and saved in /tests!")