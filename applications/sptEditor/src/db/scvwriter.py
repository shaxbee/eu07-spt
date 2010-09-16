from binwriter import BinaryWriter
from sctwriter import SECTOR_SIZE

VARIANT_FILE_VERSION = "1.0"

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
    writer.writeUInt(id)
    writer.endChunk("HEAD")
    
    writer.beginChunk("STLS")
    writer.writeUInt(len(sectors))
    
    data = ((int(sector.position.x) / SECTOR_SIZE, int(sector.position.y) / SECTOR_SIZE) for sector in sectors)
    writer.writeArray(struct.Struct("<II"), data, len(sectors))
    
    writer.endChunk("STLS")
    
    writer.endChunk("VRNT")