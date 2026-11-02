import ast
import math
import operator
import streamlit as st
from calculator import evaluate_expression, convert_units, CONSTANTS

st.set_page_config(page_title="Advanced Calculator", page_icon="🧮", layout="wide")
st.title("🧮 Advanced Calculator")
st.caption("Scientific • Unit conversion • Constants • Calculation history")

if "history" not in st.session_state:
    st.session_state.history = []
if "memory" not in st.session_state:
    st.session_state.memory = 0.0

tabs = st.tabs(["Calculator", "Unit converter", "Constants", "History"])

with tabs[0]:
    st.subheader("Scientific calculator")
    st.markdown("Use `+ - * / // % **`, parentheses, and functions such as `sin`, `cos`, `tan`, `sqrt`, `log`, `ln`, `factorial`, `abs`, `round`, `exp`, `asin`, `acos`, `atan`, `degrees`, and `radians`.")
    st.info("Angles are interpreted in radians. Use `degrees(x)` or `radians(x)` to convert.")
    expression = st.text_input("Expression", placeholder="e.g. sqrt(144) + sin(pi / 2) * 5")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Calculate", type="primary", use_container_width=True):
            try:
                result = evaluate_expression(expression)
                st.session_state.history.insert(0, {"expression": expression, "result": result})
                st.success(f"Result: {result:.12g}" if isinstance(result, float) else f"Result: {result}")
            except Exception as exc:
                st.error(str(exc))
    with c2:
        if st.button("Use memory", use_container_width=True):
            st.session_state.memory = st.session_state.history[0]["result"] if st.session_state.history else st.session_state.memory
            st.toast(f"Memory = {st.session_state.memory}")
    with c3:
        if st.button("Clear memory", use_container_width=True):
            st.session_state.memory = 0.0
            st.toast("Memory cleared")
    st.metric("Memory (M)", f"{st.session_state.memory:.12g}")
    st.caption("Available constants: pi, e, tau, phi, inf")

with tabs[1]:
    st.subheader("Unit converter")
    categories = {
        "Length": ["m", "km", "cm", "mm", "mi", "ft", "in"],
        "Mass": ["kg", "g", "mg", "lb", "oz"],
        "Time": ["s", "min", "h", "day"],
        "Temperature": ["C", "F", "K"],
        "Speed": ["m/s", "km/h", "mph"]
    }
    category = st.selectbox("Category", list(categories))
    left, right = st.columns(2)
    with left:
        value = st.number_input("Value", value=1.0, format="%.8f")
        from_unit = st.selectbox("From", categories[category], key="from")
    with right:
        to_unit = st.selectbox("To", categories[category], index=min(1, len(categories[category])-1), key="to")
    if st.button("Convert", key="convert", type="primary"):
        try:
            converted = convert_units(value, from_unit, to_unit, category)
            st.success(f"{value:g} {from_unit} = {converted:.12g} {to_unit}")
        except Exception as exc:
            st.error(str(exc))

with tabs[2]:
    st.subheader("Mathematical constants")
    for name, value in CONSTANTS.items():
        st.write(f"**{name}** — `{value:.15g}`")

with tabs[3]:
    st.subheader("Recent calculations")
    if st.button("Clear history"):
        st.session_state.history = []
    if not st.session_state.history:
        st.caption("No calculations yet.")
    for item in st.session_state.history:
        st.code(f'{item["expression"]} = {item["result"]}')
