# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ngame.proto\x12\x04game\"\x06\n\x04void\"?\n\x0csoldier_info\x12\n\n\x02id\x18\x01 \x01(\x05\x12\t\n\x01x\x18\x02 \x01(\x05\x12\t\n\x01y\x18\x03 \x01(\x05\x12\r\n\x05speed\x18\x04 \x01(\x05\"@\n\x0cmissile_info\x12\t\n\x01x\x18\x01 \x01(\x05\x12\t\n\x01y\x18\x02 \x01(\x05\x12\x0c\n\x04time\x18\x03 \x01(\x05\x12\x0c\n\x04type\x18\x04 \x01(\t\"\x17\n\x06status\x12\r\n\x05query\x18\x01 \x01(\t\"$\n\x08hit_info\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04\x66lag\x18\x02 \x01(\x08\"-\n\tpositions\x12\x0f\n\x07x_value\x18\x01 \x01(\x05\x12\x0f\n\x07y_value\x18\x02 \x01(\x05\"I\n\x0esoldier_id_pos\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x1c\n\x03pos\x18\x02 \x01(\x0b\x32\x0f.game.positions\x12\r\n\x05speed\x18\x03 \x01(\x05\";\n\x13\x41live_solier_values\x12$\n\x06values\x18\x01 \x03(\x0b\x32\x14.game.soldier_id_pos2\x8e\x02\n\x04Game\x12:\n\x10Join_Battlefield\x12\x12.game.soldier_info\x1a\x12.game.soldier_info\x12=\n\x13missile_approaching\x12\x12.game.missile_info\x1a\x12.game.missile_info\x12(\n\nstatus_all\x12\x0c.game.status\x1a\x0c.game.status\x12%\n\x07was_hit\x12\x0e.game.hit_info\x1a\n.game.void\x12:\n\x11get_alive_soldier\x12\n.game.void\x1a\x19.game.Alive_solier_valuesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'game_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_VOID']._serialized_start=20
  _globals['_VOID']._serialized_end=26
  _globals['_SOLDIER_INFO']._serialized_start=28
  _globals['_SOLDIER_INFO']._serialized_end=91
  _globals['_MISSILE_INFO']._serialized_start=93
  _globals['_MISSILE_INFO']._serialized_end=157
  _globals['_STATUS']._serialized_start=159
  _globals['_STATUS']._serialized_end=182
  _globals['_HIT_INFO']._serialized_start=184
  _globals['_HIT_INFO']._serialized_end=220
  _globals['_POSITIONS']._serialized_start=222
  _globals['_POSITIONS']._serialized_end=267
  _globals['_SOLDIER_ID_POS']._serialized_start=269
  _globals['_SOLDIER_ID_POS']._serialized_end=342
  _globals['_ALIVE_SOLIER_VALUES']._serialized_start=344
  _globals['_ALIVE_SOLIER_VALUES']._serialized_end=403
  _globals['_GAME']._serialized_start=406
  _globals['_GAME']._serialized_end=676
# @@protoc_insertion_point(module_scope)