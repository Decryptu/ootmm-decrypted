import json
import os
import tempfile
import unittest
from unittest.mock import patch

from .test_options import OOTxMMTestBase
from ..cosmetics import Cosmetics


class TestCosmeticsOutput(OOTxMMTestBase):
    options = {"cosmetics": {"defaultHold": True, "dpad": "goronred"}}

    def test_output_carries_cosmetics(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch(f"{self.world.__module__}.display_item", return_value=["OOT_RUPEE_GREEN", True]):
                self.world.generate_output(directory)
            with open(os.path.join(directory, os.listdir(directory)[0])) as file:
                output = json.load(file)
        self.assertEqual(output["cosmetics"], {"defaultHold": True, "dpad": "goronred"})


class TestCosmeticsValidation(unittest.TestCase):
    def test_rejects_bad_values(self) -> None:
        with self.assertRaises(ValueError):
            Cosmetics({"defaultHold": "yes"})
        with self.assertRaises(ValueError):
            Cosmetics({"dpad": "#ff0000"})
