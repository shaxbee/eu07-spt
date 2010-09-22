import struct

from binwriter import BinaryWriter
from sctwriter import SECTOR_SIZE

VARIANT_FILE_VERSION = "1.1"

class VariantError(RuntimeError):
    pass

def __writeVariantSectors(writer, sectors):
    writer.writeUInt(len(sectors))
    
    data = ((int(sector.position.x) / SECTOR_SIZE, int(sector.position.y) / SECTOR_SIZE) for sector in sectors)
    writer.writeArray(struct.Struct("<ii"), data, len(sectors))

def writeVariant(fout, id, sectors):
    """
    Write variant information.
    
    :param fout: output file object.
    :param id: unique variant id.
    :param sectors: list of sectors
    """
    
    writer = BinaryWriter(fout)
    
    writer.beginChunk("VRNT")
    
    writer.beginChunk("HEAD")
    writer.writeVersion(VARIANT_FILE_VERSION)
    writer.writeUShort(id)
    writer.endChunk("HEAD")
    
    writer.beginChunk("STLS")
    
    defaultSectors = [sector for sector in sectors if sector.variant == 0]
    variantSectors = list() if id == 0 else [sector for sector in sectors if sector.variant == id]

    if len(defaultSectors) + len(variantSectors) < len(sectors):
        raise VariantError("Sector(s) with invalid variantId found.")

    __writeVariantSectors(writer, defaultSectors)
    __writeVariantSectors(writer, variantSectors)
   
    writer.endChunk("STLS")
    
    writer.endChunk("VRNT")