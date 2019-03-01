import avida_converters as ac
import pandas as pd
import json

def test_Convert_AvidaSpop_To_stdPhylogeny_Sexual():
    ac.Convert_AvidaSpop_To_StdPhylogeny("example_data/example-avida-sexual.spop",
                                         "sexual_phylogeny_test.csv")
    data = pd.read_csv("sexual_phylogeny_test.csv", index_col="id")

    assert json.loads(data.loc[1524187, "ancestor_list"]) == [1520248,1523080]
    assert data.loc[1524187, "merit"] == 200704