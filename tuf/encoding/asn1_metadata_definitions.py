"""
These are the pyasn1-compatible ASN.1 definitions for TUF metadata. Please also
see tuf_metadata_definitions.asn1

This file is in part automatically generated by asn1ate (v.0.6.0), from
tuf_metadata_definitions.asn1


It is then hand-modified to do the following:

  - remove unneeded subtyping (almost all subtyping)

  - add MAX value

  - when providing a default value, rather than a subtyped object constrained to
     only have one value, provide a specific value (both seem to work, but I
     think this has the right semantics)
     e.g. use:   DefaultedNamedType('terminating', univ.Boolean(0))
     instead of: DefaultedNamedType('terminating', univ.Boolean().subtype(value=0))

  - Move superclass value overrides into bodies of classes
     e.g. use:
       class Positive(univ.Integer):
         subtypeSpec = constraint.ValueRangeConstraint(1, MAX)
     instead of:
       class Positive(univ.Integer):
         pass
       Positive.subtypeSpec = constraint.ValueRangeConstraint(1, MAX)

  - changed imports for style and readability

  - tab length 2, not 4 (per PEP 8)

  - re-ordered to better match order in tuf_metadata_definitions.asn1 for
    readability (but they must still appear such that depended-on classes appear
    before the classes that use them).

  - This comment is added to the top of the auto-generated file.

"""

import pyasn1.type.univ as univ
import pyasn1.type.char as char
import pyasn1.type.constraint as constraint
import pyasn1.type.namedtype as namedtype
# Likely imports for later:
# import pyasn1.type.namedval as namedval
# import pyasn1.type.tag as tag
from pyasn1.type.namedtype import NamedType, NamedTypes, DefaultedNamedType

# Maximum integer value when bounding integer values below.
# It does not seem possible to place a minimum without placing a maximum.
# For thresholds, versions, timestamps, etc., we want only non-negative
# integers, so we're stuck setting a maximum (or not placing any constraints
# at all in the ASN.1 metadata definition itself, would would also be fine).
MAX = 2**32-1


## Common types, for use in the various metadata types

# String types
class SignatureMethod(char.VisibleString): pass
class RoleName(char.VisibleString): pass
class Filename(char.VisibleString): pass
class HashFunction(char.VisibleString): pass
class KeyType(char.VisibleString): pass


# Binary data types
class KeyID(univ.OctetString): pass
class Path(char.VisibleString): pass


# Integer types
class Length(univ.Integer):
  subtypeSpec = constraint.ValueRangeConstraint(0, MAX)

class Threshold(univ.Integer):
  subtypeSpec = constraint.ValueRangeConstraint(0, MAX)

class Version(univ.Integer):
    subtypeSpec = constraint.ValueRangeConstraint(0, MAX)

class UTCDateTime(univ.Integer):
  subtypeSpec = constraint.ValueRangeConstraint(0, MAX)


# More complex common types follow.
class Signature(univ.Sequence):
  componentType = NamedTypes(
      NamedType('keyid', KeyID()),
      NamedType('method', SignatureMethod()),
      NamedType('value', univ.OctetString()))

class Hash(univ.Sequence):
  componentType = NamedTypes(
      NamedType('function', HashFunction()),
      NamedType('digest', univ.OctetString()))

class PublicKey(univ.Sequence):
  componentType = NamedTypes(
      NamedType('publicKeyID', KeyID()),
      NamedType('publicKeyType', KeyType()),
      NamedType('publicKeyValue', univ.OctetString()))




## Types used only in Root metadata
class RootMetadata(univ.Sequence):
  componentType = NamedTypes(
      NamedType('type', RoleName()),
      NamedType('expires', UTCDateTime()),
      NamedType('version', Version()),
      NamedType('consistent-snapshot', univ.Boolean()),
      NamedType('num-keys', Length()),
      NamedType('keys', univ.SequenceOf(componentType=PublicKey())),
      NamedType('num-roles', Length()),
      NamedType('roles', univ.SequenceOf(componentType=TopLevelDelegation())))

class TopLevelDelegation(univ.Sequence):
  componentType = NamedTypes(
      NamedType('role', RoleName()),
      NamedType('num-keyids', Length()),
      NamedType('keyids', univ.SequenceOf(componentType=KeyID())),
      NamedType('threshold', Threshold()))




## Types used only in Timestamp metadata
class HashOfSnapshot(univ.Sequence):
  componentType = NamedTypes(
      NamedType('filename', FileName()),
      NamedType('num-hashes', Length()),
      NamedType('hashes', univ.SequenceOf(componentType=Hash())))

class TimestampMetadata(univ.Sequence):
  componentType = NamedTypes(
      NamedType('type', RoleName()),
      NamedType('expires', UTCDateTime()),
      NamedType('version', Version()),
      NamedType('num-role-hashes', Length()),
      NamedType('meta', univ.SequenceOf(componentType=HashOfSnapshot()))
  )




## Types used only in Snapshot metadata
class RoleInfo(univ.Sequence):
  componentType = NamedTypes(
      NamedType('filename', Filename()),
      NamedType('version', Version()))

class SnapshotMetadata(univ.Sequence):
  componentType = NamedTypes(
      NamedType('type', RoleName()),
      NamedType('expires', UTCDateTime()),
      NamedType('version', Version()),
      NamedType('num-meta', Length()),
      NamedType('role-infos', univ.SequenceOf(componentType=RoleInfo())))




## Types used only in Targets (and delegated targets) metadata
class Delegation(univ.Sequence):
  componentType = NamedTypes(
      NamedType('name', RoleName()),
      NamedType('num-keyids', Length()),
      NamedType('keyids', univ.SequenceOf(componentType=KeyID())),
      NamedType('num-paths', Length()),
      NamedType('paths', univ.SequenceOf(componentType=Path())),
      NamedType('threshold', Threshold()),
      DefaultedNamedType('terminating', univ.Boolean(0)))

class Custom(univ.Sequence):
  componentType = NamedTypes(
      NamedType('key', char.VisibleString()),
      NamedType('value', char.VisibleString()))

class Target(univ.Sequence):
  componentType = NamedTypes(
      NamedType('target-name', Filename()),
      NamedType('length', Length()),
      NamedType('num-hashes', Length()),
      NamedType('hashes', univ.SequenceOf(componentType=Hash())),
      OptionalNamedType('num-custom', Length()),
      OptionalNamedType('custom', univ.SequenceOf(componentType=Custom())))

class TargetsMetadata(univ.Sequence):
  componentType = NamedTypes(
      NamedType('type', RoleName()),
      NamedType('expires', UTCDateTime()),
      NamedType('version', Version()),
      NamedType('num-targets', Length()),
      NamedType('targets', univ.SequenceOf(componentType=Target())),
      NamedType('delegations', univ.Sequence(componentType=NamedTypes(
          NamedType('num-keys', Length()),
          NamedType('keys', univ.SequenceOf(componentType=PublicKey())),
          NamedType('num-roles', Length()),
          NamedType('roles', univ.SequenceOf(componentType=Delegation()))
      ))) # tagFormatConstructed
  )