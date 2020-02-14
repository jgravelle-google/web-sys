# Copyright 2019 The Emscripten Authors.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

from __future__ import print_function
import os, sys

import WebIDL

to_generate = sys.argv[1:]

p = WebIDL.Parser()

builtin_types = [
  'DOMApplication',
]
for ty in builtin_types:
  p.parse('[Exposed=(Window)] interface %s { };\n' % ty)

script_dir = os.path.abspath(os.path.dirname(__file__))
idl_dir = os.path.join(script_dir, 'idl')
counts = {}
files = []
for filename in os.listdir(idl_dir):
  if filename.endswith('.webidl'):
    files.append(filename)
files.sort() # ???? whyyy
for filename in files:
  path = os.path.join(idl_dir, filename)
  p.parse(open(path).read(), filename)

all_idl_defs = p.finish()

def c(ty):
  builtin = {
    'Void': 'void',
    'Boolean': 'bool',
    'UnsignedShort': 'unsigned short',
    'Long': 'long',
    'UnsignedLong': 'unsigned long',
    'Float': 'float',
    'Double': 'double',
    'UnrestrictedDouble': 'double',
    'String': 'const char*',
    'DOMString': 'const char*',
    'USVString': 'const char*',
    'Uint8ClampedArray': 'Uint8Array',
  }
  if ty in builtin:
    return builtin[ty]
  if ty in to_generate:
    return ty
  return 'JSObject'

def decl(arg):
  ty = c(arg.type.name)
  if not ty:
    return None
  keywords = {
    'namespace': 'ns',
  }
  return ty + ' ' + keywords.get(arg.identifier.name, arg.identifier.name)

structs = {}
for idl in all_idl_defs:
  if hasattr(idl, 'identifier') and idl.identifier.name in to_generate:
    struct = structs.get(idl.identifier.name)
    if not struct:
      struct = {
        'name': idl.identifier.name,
        'constructors': [],
        'attrs': {},
        'methods': {},
      }
      structs[idl.identifier.name] = struct
    if hasattr(idl, 'ctor'):
      ct = idl.ctor()
      if ct:
        for (ret, args) in ct.signatures():
          struct['constructors'].append({
            'args': [decl(arg) for arg in args]
          })
    for member in idl.members:
      ident = member.identifier.name
      if isinstance(member, WebIDL.IDLAttribute):
        ty = c(member.type.name)
        if ty:
          if ident in struct['attrs']:
            # TODO: do something more interesting with multiply-defind attributes?
            continue
          struct['attrs'][ident] = {
            'type': ty,
            'readonly': member.readonly,
          }
      elif isinstance(member, WebIDL.IDLMethod):
        for (ret, args) in member.signatures():
          ret_ty = c(ret.name)
          arg_decls = [decl(arg) for arg in args]
          if ret_ty and all(arg_decls):
            if ident not in struct['methods']:
              struct['methods'][ident] = []
            can_add = True
            for method in struct['methods'][ident]:
              if arg_decls == method['args']:
                can_add = False
                break
            if can_add:
              struct['methods'][ident].append({
                'ret': ret_ty,
                'args': arg_decls,
              })

# Write them out
out_dir = os.path.join(script_dir, 'out')
try:
  os.mkdir(out_dir)
except:
  pass

for struct in structs.values():
  with open(os.path.join(out_dir, struct['name'] + '.h'), 'w') as f:
    f.write('#pragma once\n\n')
    f.write('#include "em_import.h"\n\n')
    f.write('EM_IMPORT_STRUCT("{0}", {0}, {{\n'.format(struct['name']))
    for ctor in struct['constructors']:
      f.write('  EM_IMPORT_CONSTRUCTOR {0}({1});\n'.format(
        struct['name'], ', '.join(ctor['args'])))
    for name, attr in struct['attrs'].iteritems():
      if attr['readonly']:
        kind = 'EM_IMPORT_FIELD_GETTER'
      else:
        kind = 'EM_IMPORT_FIELD'
      f.write('  {0}("{1}", {2}, {1});\n'.format(
        kind, name, attr['type']))
    for name, methods in struct['methods'].iteritems():
      for method in methods:
        f.write('  EM_IMPORT_METHOD("{0}") {1} {0}({2});\n'.format(
          name, method['ret'], ', '.join(method['args'])))
    f.write('});\n')
