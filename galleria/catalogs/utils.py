from datetime import datetime
from hashids import Hashids


def generate_hash_id(id, salt='catalog', len=16):
	"""
	Generates youtube like hashes with
	"""
	timestamp = str(datetime.now())
	hashids = Hashids(salt=timestamp+salt, min_length=len)
	generated_hash = hashids.encode(id)
	return generated_hash
