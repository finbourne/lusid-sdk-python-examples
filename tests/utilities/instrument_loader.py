from collections import namedtuple

import lusid
import lusid.models as models


class InstrumentLoader:
    __InstrumentSpec = namedtuple("InstrumentSpec", ["Figi", "Name"])

    __instruments = [
        __InstrumentSpec("BBG000PG14G9", "YOUGOV PLC"),
        __InstrumentSpec("BBG003FZ2QK7", "SYNCONA LTD"),
        __InstrumentSpec("BBG0058ZH3C4", "RENEWABLES INFRASTRUCTURE GR"),
        __InstrumentSpec("BBG000GRLN26", "SPECTRIS PLC"),
        __InstrumentSpec("BBG0027KC0S9", "RHI MAGNESITA INDIA LTD")
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
