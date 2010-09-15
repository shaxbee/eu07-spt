from binwriter import BinaryWriter
from sctwriter import SECTOR_SIZE

VARIANT_FILE_VERSION = "1.0"

def write_variant(writer, id, sectors):
	writer.beginChunk("VRNT")
	
	writer.beginChunk("HEAD")
	writer.writeVersion(VARIANT_FILE_VERSION)
	writer.writeUInt(id)
	writer.endChunk("HEAD")
	
	writer.beginChunk("STLS")
	writer.writeUInt(len(sectors))
	
	data = ((sector[0] / SECTOR_SIZE, sector[1] / SECTOR_SIZE, sector[2]) for sector in sectors)
	writer.writeArray(struct.Struct("<II I"), data, len(sectors))
	
	writer.endChunk("STLS")
	
	writer.endChunk("VRNT")