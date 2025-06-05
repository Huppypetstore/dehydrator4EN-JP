LANGUAGES = {
    "ja": {
        "app_title": "📊 引き合い情報分析 APP",
        "upload_label": "Excelファイルをアップロードしてください",
        "filter_header": "フィルター設定",
        "order_status": "受注の有無",
        "main_category": "業種大分類",
        "sub_category": "業種中分類",
        "machine_type": "脱水機種別",
        "analysis_header": "分析結果",
        "total_count": "フィルター適用後の総件数",
        "chart_subheader": "件数グラフ",
        "chart_type_select": "グラフの種類を選択してください:",
        "boxplot_header": "数値分析（箱ひげ図と要約統計量）",
        "boxplot1": "箱ひげ図 1：業種大分類",
        "boxplot2": "箱ひげ図 2：業種中分類",
        "select_numeric": "数値項目を選択してください",
        "show_outliers": "外れ値を表示",
        "show_zeros": "0を表示",
        "summary_stats": "📊 {col} の要約統計量 ({group}別)",
        "filtered_data": "フィルター後のデータ",
        "error": "エラーが発生しました: {msg}",
        "warning_missing_col": "データに「{col}」列が見つかりませんでした。",
        "no_numeric": "箱ひげ図と要約統計量を作成できる数値項目が見つかりません。",
    },
    "en": {
        "app_title": "📊 Inquiry Data Analysis APP",
        "upload_label": "Please upload an Excel file",
        "filter_header": "Filter Settings",
        "order_status": "Order Status",
        "main_category": "Main Category",
        "sub_category": "Sub Category",
        "machine_type": "Dewatering Machine Type",
        "analysis_header": "Analysis Results",
        "total_count": "Total after filtering",
        "chart_subheader": "Count Chart",
        "chart_type_select": "Select chart type:",
        "boxplot_header": "Numerical Analysis (Boxplot & Summary Stats)",
        "boxplot1": "Boxplot 1: Main Category",
        "boxplot2": "Boxplot 2: Sub Category",
        "select_numeric": "Select numeric column",
        "show_outliers": "Show outliers",
        "show_zeros": "Show zeros",
        "summary_stats": "📊 Summary statistics of {col} (by {group})",
        "filtered_data": "Filtered Data",
        "error": "An error occurred: {msg}",
        "warning_missing_col": "Column '{col}' not found in data.",
        "no_numeric": "No numeric columns found for boxplot and summary stats.",
    }
}

MAIN_CATEGORIES = {
    "ja": [
        "エネルギー関連", "クリーニング工場", "下水関連",
        "化学製品工場", "化学薬品工場", "機械製造業", "産業廃棄物", "商業施設",
        "食品製造", "製紙", "繊維製品", "畜産", "発電所", "公共下水"
    ],
    "en": [
        "Energy", "Cleaning Factory", "Sewage", "Chemical Product Factory", "Chemical Plant",
        "Machinery Manufacturing", "Industrial Waste", "Commercial Facility", "Food Manufacturing",
        "Paper Manufacturing", "Textile Products", "Livestock", "Power Plant", "Public Sewage"
    ]
}

SUB_CATEGORIES = {
    "ja": [
        "ガラス", "ごみ処理施設", "シャーペンの芯製造工場", "ショッピングモール",
        "し尿処理場", "バイオガス", "バイオマス", "ビル", "ホテル",
        "メタン発酵残渣", "レジャー施設", "レンダリング", "移動脱水車", "飲料",
        "下水処理場", "化粧品", "外食", "学校", "給食センター", "漁業集落排水",
        "金属", "健康食品", "自動車・二輪", "樹脂", "浄化槽", "食肉加工",
        "食品加工", "食料品", "水産加工", "精米", "製パン", "製菓",
        "製麵", "製薬", "洗剤", "染料", "繊維・衣料", "繊維製品", "調味料",
        "漬物", "電気・電子部品", "電力", "塗装", "塗装系排水処理", "塗料",
        "肉牛", "乳牛（酪農）", "農業集落排水",
        "廃プラ", "プラ再生工場", "発電所", "病院", "薬品", "油田", "溶剤",
        "養鶏", "養豚", "冷凍・チルド・中食", "OD直脱"
    ],
    "en": [
        "Glass", "Waste Treatment Facility", "Mechanical Pencil Lead Factory", "Shopping Mall",
        "Night Soil Treatment Plant", "Biogas", "Biomass", "Building", "Hotel",
        "Methane Fermentation Residue", "Leisure Facility", "Rendering", "Mobile Dewatering Vehicle", "Beverage",
        "Sewage Treatment Plant", "Cosmetics", "Dining Out", "School", "School Lunch Center", "Fishing Village Drainage",
        "Metal", "Health Food", "Automobile/Motorcycle", "Resin", "Septic Tank", "Meat Processing",
        "Food Processing", "Groceries", "Marine Product Processing", "Rice Milling", "Bread Making", "Confectionery",
        "Noodle Making", "Pharmaceuticals", "Detergent", "Dye", "Textile/Clothing", "Textile Products", "Seasoning",
        "Pickles", "Electric/Electronic Parts", "Electric Power", "Painting", "Painting Wastewater Treatment", "Paint",
        "Beef Cattle", "Dairy Cattle (Dairy Farming)", "Agricultural Village Drainage",
        "Waste Plastic", "Plastic Recycling Plant", "Power Plant", "Hospital", "Chemicals", "Oil Field", "Solvent",
        "Poultry", "Pig Farming", "Frozen/Chilled/Prepared Food", "OD Direct Dewatering"
    ]
}

DEWATERING_MACHINE_TYPES = {
    "ja": [
        "多重円板型脱水機", "多重板型スクリュープレス脱水機", "多重板型スクリュープレス脱水機小規模下水"
    ],
    "en": [
        "Multi-disc Dewatering Machine", "Multi-plate Screw Press Dewatering Machine", "Multi-plate Screw Press Dewatering Machine (Small-scale Sewage)"
    ]
}

COLUMN_MAP = {
    "ja": {
        "受注の有無": "受注の有無",
        "業種大分類": "業種大分類",
        "業種中分類": "業種中分類",
        "脱水機種別": "脱水機種別",
        "汚泥濃度 TS%": "汚泥濃度 TS%",
        "VTS%/TS": "VTS%/TS",
        "脱水ケーキ含水率 %": "脱水ケーキ含水率 %",
        "固形物回収率 %": "固形物回収率 %",
    },
    "en": {
        "受注の有無": "Order Status",
        "業種大分類": "Main Category",
        "業種中分類": "Sub Category",
        "脱水機種別": "Dewatering Machine Type",
        "汚泥濃度 TS%": "Sludge Concentration TS%",
        "VTS%/TS": "VTS%/TS",
        "脱水ケーキ含水率 %": "Cake Moisture %",
        "固形物回収率 %": "Solid Recovery %",
    }
}
