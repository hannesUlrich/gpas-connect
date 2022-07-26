import zeep
import logging
import sys
from enum import Enum


class Client:

    def __init__(self, base_url, port, domain):
        self.base_url = base_url
        self.port = port
        self.domain = domain
        wsdl = base_url + ':' + str(port) + '/gpas/gpasService?wsdl'
        self.client = None
        try:
            self.client = zeep.Client(wsdl=wsdl)
        except Exception as e:
            logging.error("gPAS.Client.init: Could not retrieve WSDL. Check connection.")
            sys.exit()

    def get_pseudonym(self, value):
        try:
            return self.client.service.getOrCreatePseudonymFor(value, self.domain)
        except Exception as e:
            logging.error("{0}".format(e))
            return None

    def get_name(self, psn):
        try:
            return self.client.service.getValueFor(psn, self.domain)
        except Exception as e:
            logging.error("{0}".format(e))
            return None


class AdminClient:
    class Alphabets(Enum):
        Hex = "org.emau.icmvc.ganimed.ttp.psn.alphabets.Hex",
        Numbers = "org.emau.icmvc.ganimed.ttp.psn.alphabets.Numbers",
        NumbersWithoutZero = "org.emau.icmvc.ganimed.ttp.psn.alphabets.NumbersWithoutZero",
        NumbersX = "org.emau.icmvc.ganimed.ttp.psn.alphabets.NumbersX",
        Symbol31 = "org.emau.icmvc.ganimed.ttp.psn.alphabets.Symbol31",
        Symbol32 = "org.emau.icmvc.ganimed.ttp.psn.alphabets.Symbol32",

    class Generators(Enum):
        NoCheckDigits = "org.emau.icmvc.ganimed.ttp.psn.generator.NoCheckDigits",
        HammingCode = "org.emau.icmvc.ganimed.ttp.psn.generator.HammingCode",
        Verhoeff = "org.emau.icmvc.ganimed.ttp.psn.generator.Verhoeff",
        VerhoeffGumm = "org.emau.icmvc.ganimed.ttp.psn.generator.VerhoeffGumm",
        Damm = "org.emau.icmvc.ganimed.ttp.psn.generator.Damm",
        ReedSolomonLagrange = "org.emau.icmvc.ganimed.ttp.psn.generator.ReedSolomonLagrange",

    def __init__(self, base_url, port):
        self.base_url = base_url
        self.port = port
        wsdl = base_url + ':' + str(port) + '/gpas/DomainService?wsdl'
        self.admin_client = None
        try:
            self.admin_client = zeep.Client(wsdl=wsdl)
        except Exception as e:
            logging.error("gPAS.Client.init: Could not retrieve WSDL. Check connection.")
            sys.exit()

    def create_domain(self, name, alphabet: Alphabets, generator: Generators, comment="", parent_domain=""):
        payload = {"name": name, "alphabet": alphabet.value[0],
                   "checkDigitClass": generator.value[0], "comment": comment,
                   "parentDomainName": parent_domain}
        try:
            self.admin_client.service.addDomain(payload)
        except Exception as e:
            logging.error("{0}".format(e))