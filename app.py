import streamlit as st
import pandas as pd
import plotly.express as px
from typing import List, Dict

# Define constants for the categories (English) - Keep these as a fallback or for reference if needed, but we'll prioritize reading from data.
MAIN_CATEGORIES = [
    "Energy-related", "Cleaning Factory", "Sewage-related",
    "Chemical Product Factory", "Chemical Plant", "Machinery Manufacturing", "Industrial Waste", "Commercial Facility",
    "Food Manufacturing", "Paper Manufacturing", "Textile Products", "Livestock", "Power Plant", "Public Sewage"
]

SUB_CATEGORIES = [
    "Glass", "Waste Treatment Facility", "Mechanical Pencil Lead Factory", "Shopping Mall",
    "Night Soil Treatment Plant", "Biogas", "Biomass", "Building", "Hotel",
    "Methane Fermentation Residue", "Leisure Facility", "Rendering", "Mobile Dewatering Vehicle", "Beverage",
    "Sewage Treatment Plant", "Cosmetics", "Dining Out", "School", "School Lunch Center", "Fishing Village Sewage",
    "Metal", "Health Food", "Automobile/Motorcycle", "Resin", "Septic Tank", "Meat Processing",
    "Food Processing", "Foodstuffs", "Marine Product Processing", "Rice Polishing", "Bread Manufacturing", "Confectionery",
    "Noodle Manufacturing", "Pharmaceutical", "Detergent", "Dye", "Textile/Clothing", "Textile Products", "Seasoning",
    "Pickles", "Electric/Electronic Parts", "Electric Power", "Painting", "Painting Wastewater Treatment", "Paint",
    "Beef Cattle", "Dairy Cattle (Dairy Farming)", "Agricultural Village Sewage",
    "Waste Plastic", "Plastic Recycling Plant", "Power Plant", "Hospital", "Chemicals", "Oil Field", "Solvent",
    "Poultry", "Pig Farming", "Frozen/Chilled/Prepared Food", "OD Direct Dewatering"
]

DEWATERING_MACHINE_TYPES = [
    "Multi-disc Dewatering Machine", "Multi-plate Screw Press Dewatering Machine", "Multi-plate Screw Press Dewatering Machine (Small-scale Sewage)"
]

# Define column names in English
COLUMN_MAIN_CATEGORY = "Main Category"
COLUMN_SUB_CATEGORY = "Sub Category"
COLUMN_ORDER_STATUS = "Order Status"
COLUMN_MACHINE_TYPE = "Dewatering Machine Type"
COLUMN_SLUDGE_CONCENTRATION = "Sludge Concentration TS%"
COLUMN_VTS_TS = "VTS%/TS"
COLUMN_CAKE_MOISTURE = "Dewatered Cake Moisture %"
COLUMN_SOLID_RECOVERY = "Solid Recovery Rate %"

def load_and_process_data(uploaded_file) -> pd.DataFrame:
    """Load and process the uploaded Excel file."""
    try:
        df = pd.read_excel(uploaded_file)

        # Data Cleaning: Convert non-numeric, empty strings, or whitespace to NaN for specific columns
        columns_to_clean = [COLUMN_SOLID_RECOVERY, COLUMN_CAKE_MOISTURE, COLUMN_SLUDGE_CONCENTRATION, COLUMN_VTS_TS]
        for col in columns_to_clean:
            if col in df.columns:
                # Convert all non-numeric values (including blank strings) to NaN
                df[col] = pd.to_numeric(df[col], errors='coerce')
                # Also replace any remaining whitespace-only strings with NaN
                df[col] = df[col].replace(r'^s*$', pd.NA, regex=True)

        return df
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def create_boxplot(df: pd.DataFrame, value_col: str, category_col: str, show_outliers: bool = True) -> None:
    """Create and display a boxplot for the specified value column, grouped by a specified category.
       Optionally hide outliers."""
    if df is not None and not df.empty:
        points_mode = 'all' if show_outliers else False
        fig = px.box(
            df,
            x=category_col,
            y=value_col,
            points=points_mode,
            title=f"Boxplot of {value_col} by {category_col}"
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

def create_summary_chart(df: pd.DataFrame, group_by: str) -> None:
    """Create and display a bar chart for the specified grouping (count)."""
    if df is not None and not df.empty:
        # Group by the primary category and then by machine type for color splitting
        if group_by in [COLUMN_MAIN_CATEGORY, COLUMN_SUB_CATEGORY]:
            df_to_chart = df
            if COLUMN_MACHINE_TYPE in df_to_chart.columns:
                 summary = df_to_chart.groupby([group_by, COLUMN_MACHINE_TYPE]).size().reset_index(name='Count')
                 summary = summary.sort_values(by=[group_by, 'Count'], ascending=[True, False])
                 color_col = COLUMN_MACHINE_TYPE
            else:
                 summary = df_to_chart.groupby([group_by]).size().reset_index(name='Count')
                 color_col = None
        else:
            summary = df[group_by].value_counts().reset_index()
            summary.columns = [group_by, 'Count']
            color_col = None

        if group_by in summary.columns:
             total_counts = summary.groupby(group_by)['Count'].sum().reset_index()
             sorted_categories = total_counts.sort_values('Count', ascending=False)[group_by].tolist()
        else:
             sorted_categories = summary[group_by].tolist() if group_by in summary.columns else []

        fig = px.bar(
            summary,
            x=group_by,
            y='Count',
            title=f'Count by {group_by}',
            labels={group_by: '', 'Count': 'Count'},
            color=color_col,
            text='Count',
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            category_orders={group_by: sorted_categories}
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(page_title="📊 Inquiry Data Analysis APP", layout="wide")
    st.title("📊 Dewatering Machine Inquiry Analysis APP")

    # File upload
    uploaded_file = st.file_uploader("Please upload an Excel file", type=['xlsx', 'xls'])

    if uploaded_file is not None:
        df = load_and_process_data(uploaded_file)

        if df is not None:
            # Get unique values from category columns for dynamic filtering
            main_categories_from_data = sorted(df[COLUMN_MAIN_CATEGORY].dropna().unique().tolist()) if COLUMN_MAIN_CATEGORY in df.columns else []
            sub_categories_from_data = sorted(df[COLUMN_SUB_CATEGORY].dropna().unique().tolist()) if COLUMN_SUB_CATEGORY in df.columns else []
            machine_types_from_data = sorted(df[COLUMN_MACHINE_TYPE].dropna().unique().tolist()) if COLUMN_MACHINE_TYPE in df.columns else []

            # Filter settings
            st.header("Filter Settings")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                order_status = st.multiselect(
                    "Order Status",
                    options=[True, False],
                    default=[True, False]
                )
            with col2:
                selected_main_categories = st.multiselect(
                    "Main Category",
                    options=main_categories_from_data, # Use dynamic options
                    default=[]
                )
            with col3:
                selected_sub_categories = st.multiselect(
                    "Sub Category",
                    options=sub_categories_from_data, # Use dynamic options
                    default=[]
                )
            with col4:
                selected_machine_types = st.multiselect(
                    "Dewatering Machine Type",
                    options=machine_types_from_data, # Use dynamic options
                    default=[]
                )

            filtered_df = df.copy()
            if order_status:
                # Filter based on English column name
                if COLUMN_ORDER_STATUS in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df[COLUMN_ORDER_STATUS].isin(order_status)]
                else:
                    st.warning(f"Column '{COLUMN_ORDER_STATUS}' not found in data.")
                    # If column is missing, filter out everything to be safe
                    filtered_df = filtered_df[filtered_df[COLUMN_ORDER_STATUS].isnull()]

            if selected_main_categories:
                # Filter based on English column name
                if COLUMN_MAIN_CATEGORY in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df[COLUMN_MAIN_CATEGORY].isin(selected_main_categories)]
                else:
                    st.warning(f"Column '{COLUMN_MAIN_CATEGORY}' not found in data.")
                    filtered_df = filtered_df[filtered_df[COLUMN_MAIN_CATEGORY].isnull()]

            if selected_sub_categories:
                # Filter based on English column name
                if COLUMN_SUB_CATEGORY in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df[COLUMN_SUB_CATEGORY].isin(selected_sub_categories)]
                else:
                    st.warning(f"Column '{COLUMN_SUB_CATEGORY}' not found in data.")
                    filtered_df = filtered_df[filtered_df[COLUMN_SUB_CATEGORY].isnull()]

            if selected_machine_types:
                # Filter based on English column name
                if COLUMN_MACHINE_TYPE in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df[COLUMN_MACHINE_TYPE].isin(selected_machine_types)]
                else:
                    st.warning(f"Column '{COLUMN_MACHINE_TYPE}' not found in data. Filter will not be applied.")

            # Analysis result (count)
            st.header("Analysis Result")
            st.write(f"Total Count After Filtering: {len(filtered_df)}")

            st.subheader("Count Chart")
            chart_type_options = [
                COLUMN_MAIN_CATEGORY,
                COLUMN_SUB_CATEGORY,
                COLUMN_ORDER_STATUS
            ]
            chart_type = st.radio(
                "Select Chart Type:",
                chart_type_options
            )
            # Ensure the selected chart_type column exists in the dataframe before charting
            if chart_type in filtered_df.columns: # Check against filtered_df as options might be limited after filtering
                create_summary_chart(filtered_df, chart_type)
            else:
                st.warning(f"Column '{chart_type}' not found in data. Count chart will not be displayed.")

            # Numeric analysis (boxplot & summary stats)
            st.header("Numeric Analysis (Boxplot & Summary Stats)")
            # Use the filtered dataframe to get numeric columns
            numeric_columns = filtered_df.select_dtypes(include='number').columns.tolist()

            # Define the preferred order of columns
            preferred_columns = [COLUMN_SLUDGE_CONCENTRATION, COLUMN_VTS_TS, COLUMN_CAKE_MOISTURE, COLUMN_SOLID_RECOVERY]

            # Create the ordered list for selectbox options
            # Start with preferred columns that are present in numeric_columns
            ordered_numeric_columns = [col for col in preferred_columns if col in numeric_columns]

            # Add the remaining numeric columns that are not in the preferred list, maintaining their original relative order
            ordered_numeric_columns.extend([col for col in numeric_columns if col not in preferred_columns])

            if ordered_numeric_columns:
                # Create 2 columns for boxplot and summary stats side by side
                col_box1, col_box2 = st.columns(2)

                with col_box1:
                    # Boxplot 1: by Main Category
                    st.subheader("Boxplot 1: Main Category")
                    # Use the ordered list for options
                    value_col_main = st.selectbox("Select Numeric Column", ordered_numeric_columns, key="boxplot1_value")
                    show_outliers_main = st.checkbox("Show Outliers", value=False, key="outliers_main")
                    show_zeros_main = st.checkbox("Show Zeros", value=False, key="show_zeros_main")

                    # Ensure 'Main Category' column exists before creating the boxplot
                    if COLUMN_MAIN_CATEGORY in filtered_df.columns:
                        if value_col_main:
                            # Filter out 0 and NaN values for specific columns if selected
                            df_for_analysis_main = filtered_df.copy()
                            columns_to_filter_zero_and_nan = [COLUMN_SOLID_RECOVERY, COLUMN_CAKE_MOISTURE]
                            if value_col_main in columns_to_filter_zero_and_nan and not show_zeros_main:
                                df_for_analysis_main = df_for_analysis_main[df_for_analysis_main[value_col_main].notna() & (df_for_analysis_main[value_col_main] != 0)]
                            elif value_col_main in columns_to_filter_zero_and_nan and show_zeros_main:
                                df_for_analysis_main = df_for_analysis_main[df_for_analysis_main[value_col_main].notna()] # Just filter NaNs if show_zeros is true

                            # Sort categories by count for boxplot
                            # Use the filtered dataframe for counts to reflect the current view
                            category_counts_main = df_for_analysis_main[COLUMN_MAIN_CATEGORY].value_counts().reset_index()
                            category_counts_main.columns = [COLUMN_MAIN_CATEGORY, 'count']
                            sorted_categories_main = category_counts_main.sort_values('count', ascending=False)[COLUMN_MAIN_CATEGORY].tolist()

                            # Create boxplot with sorted categories
                            fig_main = px.box(
                                df_for_analysis_main,
                                x=COLUMN_MAIN_CATEGORY,
                                y=value_col_main,
                                points='all' if show_outliers_main else False,
                                title=f"Boxplot of {value_col_main} by {COLUMN_MAIN_CATEGORY}",
                                category_orders={COLUMN_MAIN_CATEGORY: sorted_categories_main}
                            )
                            fig_main.update_layout(
                                xaxis_tickangle=-45,
                                height=600
                            )
                            st.plotly_chart(fig_main, use_container_width=True, config={'scrollZoom': True})

                            st.markdown("---") # Add a separator

                            # Summary stats: by Main Category
                            st.subheader(f"📊 Summary Stats of {value_col_main} (by {COLUMN_MAIN_CATEGORY})")
                            try:
                                # Ensure the column exists before grouping
                                if COLUMN_MAIN_CATEGORY in df_for_analysis_main.columns:
                                     grouped_stats_main = df_for_analysis_main.groupby(COLUMN_MAIN_CATEGORY)[value_col_main].describe()
                                     st.dataframe(grouped_stats_main)
                                else:
                                     st.warning(f"Column '{COLUMN_MAIN_CATEGORY}' not found. Summary stats by {COLUMN_MAIN_CATEGORY} will not be displayed.")

                            except Exception as e:
                                st.error(f"An error occurred while calculating summary stats by {COLUMN_MAIN_CATEGORY}: {str(e)}")
                    else:
                         st.warning(f"Column '{COLUMN_MAIN_CATEGORY}' not found. Boxplot 1 will not be displayed.")


                with col_box2:
                    # Boxplot 2: by Sub Category
                    st.subheader("Boxplot 2: Sub Category")
                    # Use the ordered list for options
                    value_col_sub = st.selectbox("Select Numeric Column", ordered_numeric_columns, key="boxplot2_value")
                    show_outliers_sub = st.checkbox("Show Outliers", value=False, key="outliers_sub")
                    show_zeros_sub = st.checkbox("Show Zeros", value=False, key="show_zeros_sub")

                    # Ensure 'Sub Category' column exists before creating the boxplot
                    if COLUMN_SUB_CATEGORY in filtered_df.columns:
                        if value_col_sub:
                            # Filter out 0 and NaN values for specific columns if selected
                            df_for_analysis_sub = filtered_df.copy()
                            columns_to_filter_zero_and_nan = [COLUMN_SOLID_RECOVERY, COLUMN_CAKE_MOISTURE]
                            if value_col_sub in columns_to_filter_zero_and_nan and not show_zeros_sub:
                                df_for_analysis_sub = df_for_analysis_sub[df_for_analysis_sub[value_col_sub].notna() & (df_for_analysis_sub[value_col_sub] != 0)]
                            elif value_col_sub in columns_to_filter_zero_and_nan and show_zeros_sub:
                                df_for_analysis_sub = df_for_analysis_sub[df_for_analysis_sub[value_col_sub].notna()] # Just filter NaNs if show_zeros is true

                            # Sort categories by count for boxplot
                            # Use the filtered dataframe for counts to reflect the current view
                            category_counts_sub = df_for_analysis_sub[COLUMN_SUB_CATEGORY].value_counts().reset_index()
                            category_counts_sub.columns = [COLUMN_SUB_CATEGORY, 'count']
                            sorted_categories_sub = category_counts_sub.sort_values('count', ascending=False)[COLUMN_SUB_CATEGORY].tolist()

                            # Create boxplot with sorted categories
                            fig_sub = px.box(
                                df_for_analysis_sub,
                                x=COLUMN_SUB_CATEGORY,
                                y=value_col_sub,
                                points='all' if show_outliers_sub else False,
                                title=f"Boxplot of {value_col_sub} by {COLUMN_SUB_CATEGORY}",
                                category_orders={COLUMN_SUB_CATEGORY: sorted_categories_sub}
                            )
                            fig_sub.update_layout(
                                xaxis_tickangle=-45,
                                height=600
                            )
                            st.plotly_chart(fig_sub, use_container_width=True, config={'scrollZoom': True})

                            st.markdown("---") # Add a separator

                            # Summary stats: by Sub Category
                            st.subheader(f"📊 Summary Stats of {value_col_sub} (by {COLUMN_SUB_CATEGORY})")
                            try:
                                # Ensure the column exists before grouping
                                if COLUMN_SUB_CATEGORY in df_for_analysis_sub.columns:
                                     grouped_stats_sub = df_for_analysis_sub.groupby(COLUMN_SUB_CATEGORY)[value_col_sub].describe()
                                     st.dataframe(grouped_stats_sub)
                                else:
                                     st.warning(f"Column '{COLUMN_SUB_CATEGORY}' not found. Summary stats by {COLUMN_SUB_CATEGORY} will not be displayed.")

                            except Exception as e:
                                st.error(f"An error occurred while calculating summary stats by {COLUMN_SUB_CATEGORY}: {str(e)}")
                    else:
                         st.warning(f"Column '{COLUMN_SUB_CATEGORY}' not found. Boxplot 2 will not be displayed.")

            else:
                st.warning("No numeric columns found for boxplot and summary stats.")

            # Display filtered data
            st.header("Filtered Data")
            st.dataframe(filtered_df)

if __name__ == "__main__":
    main()
