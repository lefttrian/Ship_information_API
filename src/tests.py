import unittest

class AdisFileTestCase(unittest.TestCase):
    def setUp(self):
        # Define sample data for testing
        entity_number = "123456"
        status = "N"
        field_definitions = [
            AdisFieldDefinition("FIELD001", 10, 0),
            AdisFieldDefinition("FIELD002", 5, 2),
            AdisFieldDefinition("FIELD003", 8, 3)
        ]
        data_rows = [
            [AdisValue("FIELD001", "Value 1"), AdisValue("FIELD002", 3.14), AdisValue("FIELD003", 123.456)],
            [AdisValue("FIELD001", "Value 2"), AdisValue("FIELD002", 2.71), AdisValue("FIELD003", 789.123)]
        ]
        self.adis_block = AdisBlock(entity_number, status, field_definitions, data_rows)
        self.adis_file = AdisFile([self.adis_block])

    def test_get_blocks(self):
        blocks = self.adis_file.get_blocks()
        self.assertEqual(len(blocks), 1)
        self.assertIs(blocks[0], self.adis_block)

    def test_from_lines(self):
        lines = [
            DefinitionLine("D" + self.adis_block.status + self.adis_block.entity_number + "FIELD001100"),
            ValueLine("V" + self.adis_block.status + self.adis_block.entity_number + "Value 1   3.14  123.456"),
            ValueLine("V" + self.adis_block.status + self.adis_block.entity_number + "Value 2   2.71  789.123")
        ]
        adis_file = AdisFile.from_lines(lines)
        blocks = adis_file.get_blocks()
        self.assertEqual(len(blocks), 1)
        self.assertEqual(len(blocks[0].get_field_definitions()), 1)
        self.assertEqual(len(blocks[0].get_data_rows()), 2)

    def test_to_dict(self):
        file_dict = self.adis_file.to_dict()
        self.assertEqual(len(file_dict), 1)
        self.assertIn(self.adis_block.get_entity_number(), file_dict)
        block_dict = file_dict[self.adis_block.get_entity_number()]
        self.assertIn("definitions", block_dict)
        self.assertIn("data", block_dict)
        self.assertEqual(len(block_dict["definitions"]), 3)
        self.assertEqual(len(block_dict["data"]), 2)

    def test_dumps(self):
        adis_text = self.adis_file.dumps()
        expected_header = f"DN{self.adis_block.entity_number}"
        self.assertTrue(adis_text.startswith(expected_header), f"ADIS text does not start with the expected header: {expected_header}")
        self.assertIn("FIELD001100FIELD002052FIELD003083", adis_text)
        self.assertIn("Value 1     314  123456", adis_text)
        self.assertIn("Value 2     271  789123", adis_text)


if __name__ == '__main__':
    unittest.main()
