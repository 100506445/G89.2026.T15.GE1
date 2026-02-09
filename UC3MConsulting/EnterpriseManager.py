import json
from .EnterpriseManagementException import EnterpriseManagementException
from .EnterpriseRequest import EnterpriseRequest

class EnterpriseManager:
    def __init__(self):
        pass

    def ValidateCIF( self, CiF ):
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE
        if (
                len(CiF) != 9
                or CiF[0] not in ["A", "B", "E", "H", "K", "P", "Q", "S"]
                or not CiF[1:8].isdigit()):
            return False

        letter = CiF[0]
        number = CiF[1:8]
        control = CiF[-1]
        even = int(number[1]) + int(number[3]) + int(number[5])

        odd = 0
        for i in [0, 2, 4, 6]:
            double = int(number[i]) * 2
            if double >= 10:
                double = (double // 10) + (double % 10)
            odd += double

        total = even + odd
        if (total % 10) == 0:
            base_digit = 0
        else:
            base_digit = 10 - (total % 10)

        table = ["J", "A", "B", "C", "D", "E", "F", "G", "H", "I"]

        if letter in ["A", "B", "E", "H"]:
            if base_digit == int(control):
                return True
            else:
                return False
        elif letter in ["K", "P", "Q", "S"]:
            if control == table[base_digit]:
                return True
            else:
                return False

    def ReadproductcodefromJSON( self, fi ):

        try:
            with open(fi) as f:
                DATA = json.load(f)
        except FileNotFoundError as e:
            raise EnterpriseManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from e


        try:
            T_CIF = DATA["cif"]
            T_PHONE = DATA["phone"]
            E_NAME = DATA["enterprise_name"]
            req = EnterpriseRequest(T_CIF, T_PHONE,E_NAME)
        except KeyError as e:
            raise EnterpriseManagementException("JSON Decode Error - Invalid JSON Key") from e
        if not self.ValidateCIF(T_CIF) :
            raise EnterpriseManagementException("Invalid FROM IBAN")
        return req