import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer, test


@transformer
def transform(df, *args, **kwargs):
    from sklearn.model_selection import train_test_split

    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df['target']
    )

    train_df = train_df.copy()
    test_df = test_df.copy()
    train_df['split'] = 'train'
    test_df['split'] = 'test'

    result = pd.concat([train_df, test_df])
    print("Train:", len(train_df), "Test:", len(test_df))
    return result


@test
def test_output(output, *args):
    assert len(output) == 150
    assert (output['split'] == 'train').sum() == 120
    assert (output['split'] == 'test').sum() == 30