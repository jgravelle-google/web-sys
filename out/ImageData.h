#pragma once

#include "em_import.h"

EM_IMPORT_STRUCT("ImageData", ImageData, {
  EM_IMPORT_CONSTRUCTOR ImageData(unsigned long sw, unsigned long sh);
  EM_IMPORT_CONSTRUCTOR ImageData(Uint8Array data, unsigned long sw, unsigned long sh);
  EM_IMPORT_FIELD_GETTER("width", unsigned long, width);
  EM_IMPORT_FIELD_GETTER("data", Uint8Array, data);
  EM_IMPORT_FIELD_GETTER("height", unsigned long, height);
});
