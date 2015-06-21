import unittest

from xsvm.parser import parse_line
from xsvm.instructions import Operand

class ParserTestCase(unittest.TestCase):
    def test_instruction_no_operands_no_label(self):
        parsed = parse_line("nop")

        self.assertEqual(parsed.mnemonic, "nop")
        self.assertIsNone(parsed.label)
        self.assertIsNone(parsed.operands)

    def test_instruction_single_operand(self):
        parsed = parse_line("b halt")

        self.assertEqual(parsed.mnemonic, "b")
        self.assertEqual(parsed.operands[0].type, Operand.TYPE_LABEL)
        self.assertEqual(parsed.operands[0].value, "halt")
        self.assertIsNone(parsed.label)

    def test_mov_without_label_constant_to_register(self):
        parsed = parse_line("mov r1, #5")

        self.assertEqual(parsed.label, None)
        self.assertEqual(parsed.mnemonic, "mov")
        self.assertEqual(parsed.operands[0].type, Operand.TYPE_REGISTER)
        self.assertEqual(parsed.operands[0].value, "r1")
        self.assertEqual(parsed.operands[1].type, Operand.TYPE_CONSTANT)
        self.assertEqual(parsed.operands[1].value, "#5")
        self.assertEqual(len(parsed.operands), 2)

    def test_mov_with_label_constant_to_register(self):
        parsed = parse_line("hello mov r1, #5")

        self.assertEqual(parsed.label, "hello")
        self.assertEqual(parsed.mnemonic, "mov")
        self.assertEqual(parsed.operands[0].type, Operand.TYPE_REGISTER)
        self.assertEqual(parsed.operands[0].value, "r1")
        self.assertEqual(parsed.operands[1].type, Operand.TYPE_CONSTANT)
        self.assertEqual(parsed.operands[1].value, "#5")
        self.assertEqual(len(parsed.operands), 2)

    def test_store_register_to_memory(self):
        parsed = parse_line("str r0, [r1]")

        self.assertIsNone(parsed.label)
        self.assertEqual(parsed.mnemonic, "str")
        self.assertEqual(len(parsed.operands), 2)
        self.assertEqual(parsed.operands[0].type, Operand.TYPE_REGISTER)
        self.assertEqual(parsed.operands[0].value, "r0")
        self.assertEqual(parsed.operands[1].type, Operand.TYPE_INDIRECT_ADDRESS)
        self.assertEqual(parsed.operands[1].value, "[r1]")

if __name__ == '__main__':
    unittest.main()