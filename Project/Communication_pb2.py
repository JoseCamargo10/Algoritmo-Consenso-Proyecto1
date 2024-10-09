# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: Communication.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'Communication.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13\x43ommunication.proto\x1a\x1bgoogle/protobuf/empty.proto\"\x1a\n\x07Request\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1b\n\x08Response\x12\x0f\n\x07message\x18\x01 \x01(\t\"-\n\x11UpdateInfoRequest\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04role\x18\x02 \x01(\t\"~\n\x12UpdateInfoResponse\x12\x36\n\nnodes_info\x18\x01 \x03(\x0b\x32\".UpdateInfoResponse.NodesInfoEntry\x1a\x30\n\x0eNodesInfoEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x1c\n\x0cWriteRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\" \n\rWriteResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1a\n\x0bReadRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"\x1c\n\x0cReadResponse\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\'\n\x14\x44isconnectionRequest\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\"(\n\x15\x44isconnectionResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2\xcb\x02\n\x14\x63ommunicationHandler\x12#\n\x0c\x43lient_Proxy\x12\x08.Request\x1a\t.Response\x12\x36\n\x0bUpdateNodes\x12\x12.UpdateInfoRequest\x1a\x13.UpdateInfoResponse\x12>\n\rDisconnection\x12\x15.DisconnectionRequest\x1a\x16.DisconnectionResponse\x12-\n\x0cWriteProcess\x12\r.WriteRequest\x1a\x0e.WriteResponse\x12*\n\x0bReadProcess\x12\x0c.ReadRequest\x1a\r.ReadResponse\x12;\n\tHeartbeat\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'Communication_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_UPDATEINFORESPONSE_NODESINFOENTRY']._loaded_options = None
  _globals['_UPDATEINFORESPONSE_NODESINFOENTRY']._serialized_options = b'8\001'
  _globals['_REQUEST']._serialized_start=52
  _globals['_REQUEST']._serialized_end=78
  _globals['_RESPONSE']._serialized_start=80
  _globals['_RESPONSE']._serialized_end=107
  _globals['_UPDATEINFOREQUEST']._serialized_start=109
  _globals['_UPDATEINFOREQUEST']._serialized_end=154
  _globals['_UPDATEINFORESPONSE']._serialized_start=156
  _globals['_UPDATEINFORESPONSE']._serialized_end=282
  _globals['_UPDATEINFORESPONSE_NODESINFOENTRY']._serialized_start=234
  _globals['_UPDATEINFORESPONSE_NODESINFOENTRY']._serialized_end=282
  _globals['_WRITEREQUEST']._serialized_start=284
  _globals['_WRITEREQUEST']._serialized_end=312
  _globals['_WRITERESPONSE']._serialized_start=314
  _globals['_WRITERESPONSE']._serialized_end=346
  _globals['_READREQUEST']._serialized_start=348
  _globals['_READREQUEST']._serialized_end=374
  _globals['_READRESPONSE']._serialized_start=376
  _globals['_READRESPONSE']._serialized_end=404
  _globals['_DISCONNECTIONREQUEST']._serialized_start=406
  _globals['_DISCONNECTIONREQUEST']._serialized_end=445
  _globals['_DISCONNECTIONRESPONSE']._serialized_start=447
  _globals['_DISCONNECTIONRESPONSE']._serialized_end=487
  _globals['_COMMUNICATIONHANDLER']._serialized_start=490
  _globals['_COMMUNICATIONHANDLER']._serialized_end=821
# @@protoc_insertion_point(module_scope)
