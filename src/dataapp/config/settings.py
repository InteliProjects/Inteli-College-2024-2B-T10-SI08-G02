 # Valida as configurações de ambiente usando Pydantic
 
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from typing import Optional


#Revisar se as tags de substituição de nulos estão corretas e se falata alguma outra coluna
class ReqMatParquetDataSchema(BaseModel):

    REQMATNUM: int
    DT_CARGA: int
    REQMATDESCR: str
    REQMATDATA: int
    TIPOREQMATCOD: float = Field(default=-1.0, description="Tag de substituição para valores nulos") 
    REQMATOPER: str
    REQMATSTAT: str
    FUNCCODCONFECCAO: int
    FUNCNOMECONFECCAO: str
    CCTRLCODESTR: str
    LOCARMAZCODESTR: float
    LOCARMAZCODALT: str
    LOCARMAZNOME: str
    PRODCODESTR: str
    FUNCCOD: int
    FUNCNOME: str
    ITREQMATQTDCALC: float
    ITREQMATQTD: float
    ITREQMATUNIDMEDPOS: float
    ITREQMATDATAHORAATEND: str
    ITREQMATUNIDMEDCOD: str
    ITREQMATQTDATEND: float
    ITREQMATQTDATENDCALC: float
    REQMATDATAENTREGA: str
    REQMATDATAAPROV: str
    ITREQMATOBS: str = Field(default='-1', description="Tag de substituição para valores nulos")
    USUCOD: str
    REQMATORIG: str
    REQMATFUNCCODAPROV: float
    REQMATDATASEPARAC: str
    REQMATFUNCCODSEPARAC: float
    REQMATFUNCCODENTREGOU: float
    REQMATFUNCCODRETIROU: float
    REQMATDATACANC: str = Field(default='-1', description="Tag de substituição para valores nulos")
    REQMATUSUCODCANC: str = Field(default='-1', description="Tag de substituição para valores nulos")
    MOTCANCCODESTR: str = Field(default='-1', description="Tag de substituição para valores nulos")
    ITREQMATSEQ: float
    ITREQMATATENDDATA: int
    ITREQMATCANC: str = Field(default='-1', description="Tag de substituição para valores nulos")
    ITREQMATCANCDATA:  str = Field(default='-1', description="Tag de substituição para valores nulos")
    ITREQMATCANCUSUCOD:  str = Field(default='-1', description="Tag de substituição para valores nulos")
    REQMATTEXTOCANC: str = Field(default='-1', description="Tag de substituição para valores nulos")
    REQMATTEXTOCANC2: float = Field(default=-1.0, description="Tag de substituição para valores nulos")
    REQMATTEXTOCANC3: float = Field(default=-1.0, description="Tag de substituição para valores nulos")
    REQMATTEXTO: str 
    REQMATTEXTO2: str = Field(default='-1', description="Tag de substituição para valores nulos")
    REQMATTEXTO3: float = Field(default=-1.0, description="Tag de substituição para valores nulos")


# class ConsumoParquetDataSchema(BaseModel):
    
