import avida_converters as ac
import pandas as pd
import ast
import pytest
import os

def test_Convert_AvidaSpop_To_stdPhylogeny_Sexual():
    ac.Convert_AvidaSpop_To_StdPhylogeny("example_data/example-avida-sexual.spop",
                                         "sexual_phylogeny_test.csv")
    data = pd.read_csv("sexual_phylogeny_test.csv", index_col="id")

    assert ast.literal_eval(data.loc[1524187, "ancestor_list"]) == ["1520248","1523080"]
    assert data.loc[1524187, "merit"] == 200704

def test_Convert_AvidaSpop_To_StdPhylogeny_InvalidInputPath():
    input_fpath = "this_file_does_not_actually_exist.spop"
    assert not os.path.isfile(input_fpath), "{} needs to not exist for this test to pass".format(input_fpath)
    with pytest.raises(ValueError):
        ac.Convert_AvidaSpop_To_StdPhylogeny(input_fpath)

def test_Convert_AvidaSpop_To_StdPhylogeny_InvalidOutputFormat():
    output_format = "this_should_never_be_a_valid_format_ever"
    assert output_format not in ac.VALID_OUT_FORMATS, "{} should not be a valid output format for this test to pass".format(output_format)
    with pytest.raises(ValueError):
        ac.Convert_AvidaSpop_To_StdPhylogeny("example_data/example-avida-sexual.spop",
                                             output_format=output_format)