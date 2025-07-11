import os
import tempfile
import warnings

import pytest

# import pysal_examples
from .... import examples as pysal_examples
from ...fileio import FileIO
from ..weight_converter import WeightConverter, weight_convert


@pytest.mark.skip("This function is deprecated.")
class TesttestWeightConverter:
    def setup_method(self):
        test_files = [
            "arcgis_ohio.dbf",
            "arcgis_txt.txt",
            "ohio.swm",
            "wmat.dat",
            "wmat.mtx",
            "sids2.gal",
            "juvenile.gwt",
            "geobugs_scot",
            "stata_full.txt",
            "stata_sparse.txt",
            "spat-sym-us.mat",
            "spat-sym-us.wk1",
        ]
        self.test_files = [pysal_examples.get_path(f) for f in test_files]
        dataformats = [
            "arcgis_dbf",
            "arcgis_text",
            None,
            None,
            None,
            None,
            None,
            "geobugs_text",
            "stata_text",
            "stata_text",
            None,
            None,
        ]
        ns = [88, 3, 88, 49, 49, 100, 168, 56, 56, 56, 46, 46]
        self.dataformats = dict(list(zip(self.test_files, dataformats, strict=True)))
        self.ns = dict(list(zip(self.test_files, ns, strict=True)))
        self.fileformats = [
            ("dbf", "arcgis_dbf"),
            ("txt", "arcgis_text"),
            ("swm", None),
            ("dat", None),
            ("mtx", None),
            ("gal", None),
            ("", "geobugs_text"),
            ("gwt", None),
            ("txt", "stata_text"),
            ("mat", None),
            ("wk1", None),
        ]

    def test__set_w(self):
        for f in self.test_files:
            with warnings.catch_warnings(record=True):
                # note: we are just suppressing the warnings here;
                # individual warnings are tested in their specific readers
                warnings.simplefilter("always")
                wc = WeightConverter(f, dataFormat=self.dataformats[f])
            assert wc.w_set() is True
            assert wc.w.n == self.ns[f]

    def test_write(self):
        for f in self.test_files:
            with warnings.catch_warnings(record=True):
                # note: we are just suppressing the warnings here;
                # individual warnings are tested in their specific readers
                warnings.simplefilter("always")
                wc = WeightConverter(f, dataFormat=self.dataformats[f])

            for ext, dataformat in self.fileformats:
                if f.lower().endswith(ext):
                    continue
                with tempfile.NamedTemporaryFile(suffix=f".{ext}") as temp_f:
                    temp_fname = temp_f.name

                with warnings.catch_warnings(record=True):
                    # note: we are just suppressing the warnings here;
                    # individual warnings are tested in their specific readers
                    warnings.simplefilter("always")
                    if ext == "swm":
                        wc.write(temp_fname, useIdIndex=True)
                    elif dataformat is None:
                        wc.write(temp_fname)
                    elif dataformat in ["arcgis_dbf", "arcgis_text"]:
                        wc.write(temp_fname, dataFormat=dataformat, useIdIndex=True)
                    elif dataformat == "stata_text":
                        wc.write(temp_fname, dataFormat=dataformat, matrix_form=True)
                    else:
                        wc.write(temp_fname, dataFormat=dataformat)

                with warnings.catch_warnings(record=True):
                    # note: we are just suppressing the warnings here;
                    # individual warnings are tested in their specific readers
                    warnings.simplefilter("always")
                    if dataformat is None:
                        wnew = FileIO(temp_fname, "r").read()
                    else:
                        wnew = FileIO(temp_fname, "r", dataformat).read()

                if (
                    ext in ["dbf", "swm", "dat", "wk1", "gwt"]
                    or dataformat == "arcgis_text"
                ):
                    assert wnew.n == wc.w.n - len(wc.w.islands)
                else:
                    assert wnew.n == wc.w.n
                os.remove(temp_fname)

    def test_weight_convert(self):
        for f in self.test_files:
            in_file = f
            in_data_format = self.dataformats[f]
            with warnings.catch_warnings(record=True):
                # note: we are just suppressing the warnings here; individual warnings
                #       are tested in their specific readers
                warnings.simplefilter("always")
                if in_data_format is None:
                    in_file = FileIO(in_file, "r")
                else:
                    in_file = FileIO(in_file, "r", in_data_format)
                wold = in_file.read()
                in_file.close()

            for ext, dataformat in self.fileformats:
                if f.lower().endswith(ext):
                    continue
                with tempfile.NamedTemporaryFile(suffix=f".{ext}") as temp_f:
                    out_file = temp_f.name
                out_data_format, use_id_index, matrix_form = dataformat, False, False
                if ext == "swm" or dataformat in ["arcgis_dbf", "arcgis_text"]:
                    use_id_index = True
                elif dataformat == "stata_text":
                    matrix_form = True

                with warnings.catch_warnings(record=True):
                    # note: we are just suppressing the warnings here;
                    # individual warnings are tested in their specific readers
                    warnings.simplefilter("always")
                    weight_convert(
                        in_file,
                        out_file,
                        in_data_format,
                        out_data_format,
                        use_id_index,
                        matrix_form,
                    )

                with warnings.catch_warnings(record=True):
                    # note: we are just suppressing the warnings here;
                    # individual warnings are tested in their specific readers
                    warnings.simplefilter("always")
                    if dataformat is None:
                        wnew = FileIO(out_file, "r").read()
                    else:
                        wnew = FileIO(out_file, "r", dataformat).read()

                if (
                    ext in ["dbf", "swm", "dat", "wk1", "gwt"]
                    or dataformat == "arcgis_text"
                ):
                    assert wnew.n == wold.n - len(wold.islands)
                else:
                    assert wnew.n == wold.n
                os.remove(out_file)
