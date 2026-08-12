import ast
import unittest
from pathlib import Path

from ...Locations import coin_count_check_location_table, individual_coin_location_table, location_table


class TestDeclarativeLocationCoverage(unittest.TestCase):
    def test_every_non_coin_count_check_location_has_a_declarative_test(self):
        expected_locations = set(location_table).difference(
            coin_count_check_location_table, individual_coin_location_table)
        tested_locations: set[str] = set()
        test_directory = Path(__file__).parent

        for test_file in test_directory.glob("test_*.py"):
            if test_file == Path(__file__):
                continue
            syntax_tree = ast.parse(test_file.read_text(encoding="utf-8"), filename=str(test_file))
            tested_locations.update(
                node.value
                for node in ast.walk(syntax_tree)
                if isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and node.value in expected_locations
            )

        self.assertSetEqual(
            tested_locations,
            expected_locations,
            "Every fixed location must be named in an ALttP-style declarative location test.",
        )
