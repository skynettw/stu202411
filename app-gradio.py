import gradio as gr
import pandas as pd

# Read the CSV data
def load_data():
    df = pd.read_csv('data.csv')
    
    # Get unique values for each column for dropdowns
    unique_values = {
        '縣市': sorted(['全部'] + df['縣市'].unique().tolist()),
        '醫療院所': sorted(['全部'] + df['醫療院所'].dropna().unique().tolist()),
        '科別': sorted(['全部'] + df['科別'].dropna().unique().tolist()),
        '學歷': sorted(['全部'] + df['學歷'].dropna().unique().tolist())
    }
    
    return df, unique_values

# Search function
def search(city, hospital, department, education):
    df, _ = load_data()
    
    # Apply filters
    if city != '全部':
        df = df[df['縣市'] == city]
    if hospital != '全部':
        df = df[df['醫療院所'] == hospital]
    if department != '全部':
        df = df[df['科別'] == department]
    if education != '全部':
        df = df[df['學歷'] == education]
    
    # Convert results to string format for display
    if len(df) == 0:
        return "查無資料！請調整搜尋條件後重試。"
    
    # Format results as a string with proper alignment
    result_lines = []
    result_lines.append("縣市\t醫療院所\t科別\t姓名\t學歷")
    result_lines.append("-" * 80)  # Separator line
    
    for _, row in df.iterrows():
        result_lines.append(f"{row['縣市']}\t{row['醫療院所']}\t{row['科別']}\t{row['姓名']}\t{row['學歷']}")
    
    return "\n".join(result_lines)

# Create Gradio interface
def create_interface():
    df, unique_values = load_data()
    
    interface = gr.Interface(
        fn=search,
        inputs=[
            gr.Dropdown(choices=unique_values['縣市'], label="縣市", value='全部'),
            gr.Dropdown(choices=unique_values['醫療院所'], label="醫療院所", value='全部'),
            gr.Dropdown(choices=unique_values['科別'], label="科別", value='全部'),
            gr.Dropdown(choices=unique_values['學歷'], label="學歷", value='全部')
        ],
        outputs=gr.Textbox(label="搜尋結果", lines=20),
        title="醫護人員查詢系統",
        description="請選擇搜尋條件（選擇「全部」表示不限制該條件）",
        theme=gr.themes.Soft(),
        css="""
            .gradio-container {
                font-family: "Microsoft JhengHei", sans-serif;
            }
            .output-textbox {
                font-family: monospace;
            }
        """
    )
    return interface

# Launch the application
if __name__ == "__main__":
    interface = create_interface()
    interface.launch(share=True, server_name="0.0.0.0", server_port=7860)
