import streamlit as st
import pandas as pd

from src.ocr import extract_text_from_image
from src.checks import run_all_checks, overall_status


st.set_page_config(
    page_title="Alcohol Label Verification App",
    page_icon="🍾",
    layout="wide"
)


st.title("AI-Powered Alcohol Label Verification App")

st.write(
    "Upload alcohol label artwork and compare the extracted label text against application data. "
    "This prototype is designed to assist compliance reviewers by flagging likely matches, mismatches, "
    "and items needing human review."
)


with st.sidebar:
    st.header("Application Data")

    brand_name = st.text_input("Brand Name", value="OLD TOM DISTILLERY")
    class_type = st.text_input("Class/Type", value="Kentucky Straight Bourbon Whiskey")
    alcohol_content = st.text_input("Alcohol Content", value="45")
    net_contents = st.text_input("Net Contents", value="750 mL")

    st.divider()

    st.write("Expected values are compared against OCR text extracted from the uploaded label image.")


uploaded_files = st.file_uploader(
    "Upload one or more label images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)


expected_data = {
    "brand_name": brand_name,
    "class_type": class_type,
    "alcohol_content": alcohol_content,
    "net_contents": net_contents
}


if uploaded_files:
    all_summary_rows = []

    for uploaded_file in uploaded_files:
        st.divider()
        st.subheader(f"Results for: {uploaded_file.name}")

        with st.spinner("Reading label text and running checks..."):
            extracted_text = extract_text_from_image(uploaded_file)
            check_results = run_all_checks(expected_data, extracted_text)
            final_status = overall_status(check_results)

        if final_status == "PASS":
            st.success("Overall Status: PASS")
        elif final_status == "REVIEW":
            st.warning("Overall Status: REVIEW")
        else:
            st.error("Overall Status: FAIL")

        results_df = pd.DataFrame(check_results)
        st.dataframe(results_df, use_container_width=True)

        for result in check_results:
            all_summary_rows.append({
                "file": uploaded_file.name,
                "overall_status": final_status,
                "field": result["field"],
                "status": result["status"],
                "expected": result["expected"],
                "found": result["found"],
                "score": result["score"],
                "notes": result["notes"]
            })

        with st.expander("View extracted OCR text"):
            st.text_area(
                label="OCR Text",
                value=extracted_text,
                height=250,
                key=f"ocr_{uploaded_file.name}"
            )

    summary_df = pd.DataFrame(all_summary_rows)

    st.divider()
    st.header("Batch Summary")

    st.dataframe(summary_df, use_container_width=True)

    csv_data = summary_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV Report",
        data=csv_data,
        file_name="label_verification_report.csv",
        mime="text/csv"
    )

else:
    st.info("Upload at least one label image to begin.")
    