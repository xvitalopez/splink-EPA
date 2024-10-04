from datetime import datetime
print(f"Start: {datetime.now()}")

from splink.duckdb.duckdb_linker import DuckDBLinker
from splink.duckdb.duckdb_comparison_library import (
    exact_match,
    levenshtein_at_thresholds,
)
import splink.duckdb.duckdb_comparison_level_library as cll
import splink.duckdb.duckdb_comparison_library as cl

comparison_first_name=cl.exact_match("first_name")
comparison_first_name = {
    'output_column_name': 'first_name',
    'comparison_description': 'First name jaro dmeta',
    'comparison_levels': [
        cll.null_level("first_name"),
        cll.exact_match_level("first_name"),
        cll.levenshtein_level("first_name",2),
 ],

}
comparison_surname=cl.exact_match("surname")
comparison_surname = {
    'output_column_name': 'surname',
    'comparison_description': 'surname jaro dmeta',
    'comparison_levels': [
        cll.null_level("surname"),
        cll.exact_match_level("surname"),
        cll.levenshtein_level("surname",2),
    ],
}
comparison_dob = {
    "output_column_name": "dob",
    "comparison_description": "dob",
    "comparison_levels": [
        cll.null_level("dob"),
        cll.exact_match_level("dob"),
        cll.levenshtein_level("dob", 2),
        cll.else_level()
    ],
}

from splink.comparison import Comparison

import pandas as pd
from sqlalchemy import create_engine
df= pd.read_csv("3_1_10kyes.csv")
print(df)

splink_settings = {
    "link_type": "dedupe_only",
    "blocking_rules_to_generate_predictions": [
    "l.pnc_id=r.pnc_id",
    "l.ni_number=r.ni_number", 
    "l.first_name=r.first_name AND l.surname=r.surname AND l.dob=r.dob",
    "l.first_name=r.first_name AND l.surname=r.surname AND l.phone_number=r.phone_number",
    ],

    "comparisons": [
        levenshtein_at_thresholds("first_name",2),
        levenshtein_at_thresholds("surname", 2),
        levenshtein_at_thresholds("dob",2),
        levenshtein_at_thresholds("phone_number",2),
        levenshtein_at_thresholds("address",2),
        levenshtein_at_thresholds("birth_place",2),
        exact_match("Gender"),
        exact_match("pnc_id"),
        exact_match("ni_number"),
        
    ],
    "retain_intermediate_calculation_columns": True,
    "unique_id_column_name": 'id'
}
linker = DuckDBLinker(df, splink_settings)
comparison_first_name = {
    "output_column_name": "first_name",
    "comparison_description": "First name jaro dmeta",
    "comparison_levels": [
        {
            "sql_condition": "first_name_l IS NULL OR first_name_r IS NULL",
            "label_for_charts": "Null",
            "is_null_level": True,
        },
        {
            "sql_condition": "first_name_l = first_name_r",
            "label_for_charts": "Exact match",
            "tf_adjustment_column": "first_name",
            "tf_adjustment_weight": 1.0,
            "tf_minimum_u_value": 0.001,
        },
        {
            "sql_condition": "dmeta_first_name_l = dmeta_first_name_r",
            "label_for_charts": "Exact match",
            "tf_adjustment_column": "dmeta_first_name",
            "tf_adjustment_weight": 1.0,
        },
        {
            "sql_condition": "jaro_winkler_sim(first_name_l, first_name_r) > 0.8",
            "label_for_charts": "Exact match",
            "tf_adjustment_column": "first_name",
            "tf_adjustment_weight": 0.5,
            "tf_minimum_u_value": 0.001,
        },
        {"sql_condition": "ELSE", "label_for_charts": "All other comparisons"},
    ],

}

comparison_first_name = {
    "output_column_name": "surname",
    "comparison_description": "surname jaro dmeta",
    "comparison_levels": [
        {
            "sql_condition": "fsurname_l IS NULL OR surname_r IS NULL",
            "label_for_charts": "Null",
            "is_null_level": True,
        },
        {
            "sql_condition": "surname_l = surname_r",
            "label_for_charts": "Exact match",
            "tf_adjustment_column": "surname",
            "tf_adjustment_weight": 1.0,
            "tf_minimum_u_value": 0.001,
        },
        {
            "sql_condition": "dmeta_surname_l = dmeta_surname_r",
            "label_for_charts": "Exact match",
            "tf_adjustment_column": "dmeta_surname",
            "tf_adjustment_weight": 1.0,
        },
        {
            "sql_condition": "jaro_winkler_sim(surname_l, surname_r) > 0.8",
            "label_for_charts": "Exact match",
            "tf_adjustment_column": "surname",
            "tf_adjustment_weight": 0.5,
            "tf_minimum_u_value": 0.001,
        },
        {"sql_condition": "ELSE", "label_for_charts": "All other comparisons"},
    ],

}


deterministic_rules = [
"l.first_name=r.first_name and levenshtein(r.dob,l.dob)<=1",
"l.surname=r.surname and levenshtein(r.dob,l.dob)<=1",
"l.first_name=r.first_name and levenshtein(r.surname,l.surname)<=2",
"l.pnc_id=r.pnc_id",
"l.ni_number=r.ni_number"
]
linker.estimate_probability_two_random_records_match(deterministic_rules, recall=0.7)
try:
    linker.estimate_u_using_random_sampling(target_rows=1e6)

    blocking_rule_for_training = "l.address = r.address"
    linker.estimate_parameters_using_expectation_maximisation(blocking_rule_for_training)

    blocking_rule_for_training = "l.dob = r.dob"
    training_session = linker.estimate_parameters_using_expectation_maximisation(blocking_rule_for_training)

    df_predict = linker.predict(threshold_match_probability=0.3)
    df_e = df_predict.as_pandas_dataframe(limit=10)

    from splink.charts import waterfall_chart
    records_to_plot = df_e.to_dict(orient="records")
    linker.waterfall_chart(records_to_plot, filter_nulls=False)

    clusters = linker.cluster_pairwise_predictions_at_threshold(df_predict, threshold_match_probability=0.9)

    df_predictions = linker.predict(threshold_match_probability=0.2)
    records_to_view=df_predictions.as_record_dict(limit=5)
    linker.waterfall_chart(records_to_view, filter_nulls=False)

    df_clusters = linker.cluster_pairwise_predictions_at_threshold(df_predictions, threshold_match_probability=0.5)

    linker.cluster_studio_dashboard(df_predictions, df_clusters, "cluster_studio.html", sampling_method="by_cluster_size", overwrite=True)
    df_e.to_csv("results.csv")
    from IPython.display import IFrame
    IFrame(
        src="./cluster_studio.html", width="100%", height=1200
    )
    linker.comparison_viewer_dashboard(df_predictions, "scv.html", overwrite=True)
    from IPython.display import IFrame
    IFrame(
        src="scv.html", width="100%", height=1200
    )
    #in new cell
    df_clusters.as_pandas_dataframe().to_csv("V16.csv")
except:
    print(f"Failed: {datetime.now()}")
    raise

print(f"End: {datetime.now()}")
