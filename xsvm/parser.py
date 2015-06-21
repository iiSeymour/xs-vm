from pyparsing import *
from instructions import supported_instructions, Instruction, Operand

label_definition = Word(alphanums + "_")
mnemonic_definition = oneOf(" ".join(supported_instructions), caseless=True)
register_definition = Combine(CaselessLiteral("r") + Word(nums))
indirectly_addressed_register = Combine(Literal("[") + register_definition + Literal("]"))
constant_definition = Combine(Literal("#") + Word(nums))

operand_definitions = register_definition | indirectly_addressed_register | label_definition | constant_definition


def parse_line(source_code_line):
    instruction_definition = Forward()

    instruction_definition << Optional(label_definition.setResultsName("label") + FollowedBy(mnemonic_definition)) + mnemonic_definition.setResultsName("mnemonic") \
                              + Optional(Group(delimitedList(operand_definitions, ","))).setResultsName("operands")

    parsed_line = instruction_definition.parseString(source_code_line)

    label = parsed_line.label
    if label == "":
        label = None

    mnemonic = parsed_line.mnemonic
    if mnemonic == "":
        mnemonic = None

    if parsed_line.operands == "":
        operands = None
    else:
        operands_raw = parsed_line.operands[0]
        operands = process_operands(operands_raw)

    parsed_instruction = Instruction(label=label, mnemonic=mnemonic, operands=operands)

    return parsed_instruction


def process_operands(operands_raw):
    operands = []
    for operand_raw in operands_raw:
        try:
            register_definition.parseString(operand_raw)
            new_operand = Operand(type=Operand.TYPE_REGISTER, value=operand_raw)
            operands.append(new_operand)
            continue
        except:
            pass

        try:
            indirectly_addressed_register.parseString(operand_raw)
            new_operand = Operand(type=Operand.TYPE_INDIRECT_ADDRESS, value=operand_raw)
            operands.append(new_operand)
            continue
        except:
            pass

        try:
            label_definition.parseString(operand_raw)
            new_operand = Operand(type=Operand.TYPE_LABEL, value=operand_raw)
            operands.append(new_operand)
            continue
        except:
            pass

        try:
            constant_definition.parseString(operand_raw)
            new_operand = Operand(type=Operand.TYPE_CONSTANT, value=operand_raw)
            operands.append(new_operand)
            continue
        except:
            pass

    return operands