from sklearn.datasets import load_iris

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader, test


@data_loader
def load_data(*args, **kwargs):
    iris = load_iris(as_frame=True)
    df = iris.frame

    print("Rows loaded:", len(df))
    print("Columns:", list(df.columns))

    return df


@test
def test_output(output, *args):
    assert output is not None
    assert len(output) == 150
    assert 'target' in output.columns
    assert output.isnull().sum().sum() == 0