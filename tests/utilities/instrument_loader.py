import uuid
from collections import namedtuple

import lusid
import lusid.models as models


class InstrumentLoader:
    __InstrumentSpec = namedtuple("InstrumentSpec", ["Figi", "Name"])

    __instruments = [
        __InstrumentSpec(f"BBG000FD8G46_{uuid.uuid4()}", "HISCOX LTD"),
        __InstrumentSpec(f"BBG000DW76R4_{uuid.uuid4()}", "ITV PLC"),
        __InstrumentSpec(f"BBG000PQKVN8_{uuid.uuid4()}", "MONDI PLC"),
        __InstrumentSpec(f"BBG000BDWPY0_{uuid.uuid4()}", "NEXT PLC"),
        __InstrumentSpec(f"BBG000BF46Y8_{uuid.uuid4()}", "TESCO PLC")
    ]

    def __init__(self, instruments_api: lusid.InstrumentsApi):
        self.instruments_api = instruments_api

    def load_instruments(self):
        instruments_to_create = {
            i.Figi: models.InstrumentDefinition(
                name=i.Name,
                identifiers={
                    "Figi": models.InstrumentIdValue(value=i.Figi)
                }
            ) for i in self.__instruments
        }

        response = self.instruments_api.upsert_instruments(request_body=instruments_to_create)

        assert (len(response.failed) == 0)

        return sorted([i.lusid_instrument_id for i in response.values.values()])

    def delete_instruments(self):
        for i in self.__instruments:
            self.instruments_api.delete_instrument("Figi", i.Figi)
