import os
import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter, test


@data_exporter
def export_data(df, *args, **kwargs):
    output_path = os.path.abspath('iris_predictions.csv')
    df.to_csv(output_path, index=False)

    print("Results saved:", output_path)
    print("Rows exported:", len(df))

    return df


@test
def test_output(output, *args):
    assert output is not None
    assert len(output) == 30
    assert os.path.exists(os.path.abspath('iris_predictions.csv'))