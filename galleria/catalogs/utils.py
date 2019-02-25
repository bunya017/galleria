import io
from PIL import Image
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


def generate_photo(filename):
		file = io.BytesIO()
		image = Image.new('RGBA', size=(640, 640), color=(155,0,0))
		image.save(file, 'png')
		file.name = '%s.png' % filename
		file.seek(0)
		return file