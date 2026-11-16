
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer, test

@transformer
def validate(df, *args, **kwargs):
    assert len(df) == 150
    assert df.isnull().sum().sum() == 0
    assert 'target' in df.columns
    assert df['target'].nunique() == 3

    print("Custom Iris validation successful!")
    return df

@test
def test_output(output, *args):
    assert len(output) == 150
    assert output['target'].nunique() == 3
