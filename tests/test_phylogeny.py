import avida_converters as ac
import pandas as pd
import json, pytest, os

def test_Convert_AvidaSpop_To_stdPhylogeny_Sexual():
    ac.Convert_AvidaSpop_To_StdPhylogeny("example_data/example-avida-sexual.spop",
                                         "sexual_phylogeny_test.csv")
    data = pd.read_csv("sexual_phylogeny_test.csv", index_col="id")

    assert json.loads(data.loc[1524187, "ancestor_list"]) == [1520248,1523080]
    assert data.loc[1524187, "merit"] == 200704

def test_Convert_AvidaSpop_To_StdPhylogeny_InvalidInputPath():
    input_fpath = "this_file_does_not_actually_exist.spop"
    assert not os.path.isfile(input_fpath), "{} needs to not exist for this test to pass".format(input_fpath)
    with pytest.raises(ValueError):
        ac.Convert_AvidaSpop_To_StdPhylogeny(input_fpath)