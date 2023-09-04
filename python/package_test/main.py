# -*- coding:UTF-8 -*-
import src_test as st

handle = st.ZMCWrapper()
st.connect(handle)
#st.set_parameter(handle, 6, 5)

st.src_move(handle, 6, 5, 10)
#handle.func_test()

#st.test(handle)